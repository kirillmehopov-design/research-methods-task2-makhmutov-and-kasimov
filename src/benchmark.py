"""Validated benchmark pipeline for an AI-assisted programming experience study.

This analyzes recorded human-task measurements; it does not run GitHub Copilot,
generate research observations, or draw statistical conclusions from demo data.
Python standard library only.
"""
import argparse
import csv
import datetime as dt
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DataError(ValueError):
    pass


def load_csv(path, required):
    if not path.is_file():
        raise DataError(f"Missing file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(c not in reader.fieldnames for c in required):
            raise DataError(f"Bad columns in {path}; required: {', '.join(required)}")
        rows = list(reader)
    if not rows:
        raise DataError(f"No records in {path}")
    return rows


def numeric(row, key, *, minimum=0.0):
    try:
        value = float(row[key])
    except (ValueError, KeyError, TypeError) as exc:
        raise DataError(f"Invalid numeric {key} in participant {row.get('participant_id')}") from exc
    if not math.isfinite(value) or value < minimum:
        raise DataError(f"Out of bounds {key} in participant {row.get('participant_id')}")
    return value


def validate_participants(trials, surveys, reviews):
    trial_ids={r["participant_id"].strip() for r in trials}
    survey_ids={r["participant_id"].strip() for r in surveys}
    review_ids={r["participant_id"].strip() for r in reviews}
    if trial_ids != survey_ids or trial_ids != review_ids:
        raise DataError("Participant sets must match in trials, survey, and review data")
    groups = {}
    for rows in (trials, surveys, reviews):
        for row in rows:
            pid = row["participant_id"].strip()
            group = row["experience_group"].strip().lower()
            if not pid or group not in {"novice", "experienced"}:
                raise DataError(f"Bad participant/group: {pid!r}/{group!r}")
            if pid in groups and groups[pid] != group:
                raise DataError(f"Inconsistent experience group for {pid}")
            groups[pid] = group
    return groups


def analyze_trials(trials, config):
    paired = {}
    for row in trials:
        pid = row["participant_id"].strip()
        condition = row["condition"].strip().lower()
        task_id = row["task_id"].strip()
        if not task_id:
            raise DataError(f"Missing matched task identifier for {pid}")
        if condition not in {"ai", "no_ai"}:
            raise DataError(f"Invalid condition {condition} for {pid}")
        if condition in paired.setdefault(pid, {}):
            raise DataError(f"Duplicate {condition} trial for {pid}")
        time = numeric(row, "completion_seconds", minimum=0.001)
        passed = numeric(row, "tests_passed")
        total = numeric(row, "tests_total", minimum=1)
        defects = numeric(row, "static_analysis_defects")
        critical = numeric(row, "critical_defects")
        prompts = numeric(row, "prompt_count")
        accepted = numeric(row, "accepted_suggestions")
        verified = numeric(row, "verification_actions")
        if passed > total or any(not x.is_integer() for x in [passed,total,defects,critical,prompts,accepted,verified]):
            raise DataError(f"Invalid count/test values for {pid}")
        if condition == "no_ai" and (prompts or accepted):
            raise DataError(f"No-AI trial contains AI events for {pid}")
        paired[pid][condition] = {
            "group":row["experience_group"].lower().strip(),
            "task_id":task_id,
            "seconds":time,"pass_rate":passed/total,
            "static_analysis_defects":int(defects),"critical_defects":int(critical),
            "prompt_count":int(prompts),"accepted_suggestions":int(accepted),
            "verification_actions":int(verified)
        }
    participant_results=[]
    for pid,condition_data in sorted(paired.items()):
        if set(condition_data) != {"ai", "no_ai"}:
            raise DataError(f"Participant {pid} needs exactly one AI and one no-AI trial")
        ai=condition_data["ai"]
        base=condition_data["no_ai"]
        if ai["group"] != base["group"]:
            raise DataError(f"Experience group differs for {pid}")
        if ai["task_id"] == base["task_id"]:
            raise DataError(f"Repeated task for {pid}; use matched alternative tasks in crossover")
        participant_results.append({
            "participant_id":pid,"experience_group":ai["group"],
            "time_reduction_pct":round(100*(base["seconds"]-ai["seconds"])/base["seconds"],3),
            "pass_rate_difference_ai_minus_baseline":round(ai["pass_rate"]-base["pass_rate"],4),
            "ai_critical_defects":ai["critical_defects"],
            "ai_static_analysis_defects":ai["static_analysis_defects"],
            "prompt_count":ai["prompt_count"],"verification_actions":ai["verification_actions"]
        })
    by_group={}
    max_drop=config["metrics"]["guardrails"]["max_unit_test_pass_rate_drop_fraction"]
    max_crit=config["metrics"]["guardrails"]["max_critical_defects_in_ai_condition"]
    for group in ("novice","experienced"):
        people=[p for p in participant_results if p["experience_group"]==group]
        if not people:
            raise DataError(f"No paired participants in group {group}")
        reduction=statistics.mean(p["time_reduction_pct"] for p in people)
        drop=statistics.mean(p["pass_rate_difference_ai_minus_baseline"] for p in people)
        max_critical=max(p["ai_critical_defects"] for p in people)
        by_group[group]={
            "n_participants":len(people),
            "mean_time_reduction_pct":round(reduction,3),
            "mean_test_pass_rate_change_fraction":round(drop,4),
            "max_ai_critical_defects":max_critical,
            "guardrails_satisfied":drop >= -max_drop and max_critical <= max_crit
        }
    difference=by_group["experienced"]["mean_time_reduction_pct"]-by_group["novice"]["mean_time_reduction_pct"]
    return {
        "paired_participants":len(participant_results),
        "by_group":by_group,
        "primary_effect_experienced_minus_novice_percentage_points":round(difference,3),
        "interpretation":"Positive means the experienced group received a larger relative time benefit; negative means the novice group benefited more.",
        "participant_details":participant_results,
    }


def analyze_reviews(rows):
    group_metrics={"novice":[],"experienced":[]}
    seen=set()
    for row in rows:
        pid=row["participant_id"].strip()
        if pid in seen:
            raise DataError(f"Duplicate review for {pid}")
        seen.add(pid)
        group=row["experience_group"].strip().lower()
        total=numeric(row,"seeded_defects_total",minimum=1)
        detected=numeric(row,"defects_detected")
        fixed=numeric(row,"defects_correctly_fixed")
        seconds=numeric(row,"review_seconds",minimum=0.001)
        if detected>total or fixed>detected or any(not x.is_integer() for x in [total,detected,fixed]):
            raise DataError(f"Invalid review counts for {pid}")
        group_metrics[group].append({"detected_fraction":detected/total,"fixed_fraction":fixed/total,"seconds":seconds})
    results={}
    for group, recs in group_metrics.items():
        if not recs:raise DataError(f"Missing reviews for {group}")
        results[group]={
            "n_reviews":len(recs),
            "mean_detection_rate":round(statistics.mean(x["detected_fraction"] for x in recs),4),
            "mean_correct_fix_rate":round(statistics.mean(x["fixed_fraction"] for x in recs),4),
            "mean_review_seconds":round(statistics.mean(x["seconds"] for x in recs),2)
        }
    return results


def analyze_survey(rows):
    by_group={"novice":[],"experienced":[]}
    seen=set()
    for row in rows:
        pid=row["participant_id"].strip()
        if pid in seen:raise DataError(f"Duplicate survey for {pid}")
        seen.add(pid)
        group=row["experience_group"].strip().lower()
        frequency=numeric(row,"ai_uses_per_week")
        if not frequency.is_integer():raise DataError(f"Non-integer use frequency for {pid}")
        by_group[group].append({"weekly_uses":int(frequency),"primary_use":row["primary_ai_use"].strip()})
    res={}
    for group,recs in by_group.items():
        if not recs:raise DataError(f"Missing survey data for {group}")
        uses={}
        for item in recs:
            uses[item["primary_use"]]=uses.get(item["primary_use"],0)+1
        res[group]={"n_responses":len(recs),"mean_uses_per_week":round(statistics.mean(r["weekly_uses"] for r in recs),2),"purposes":uses}
    return res


def run(config_path:Path):
    with config_path.open(encoding="utf-8") as file:
        config=json.load(file)
    paths={key: ROOT/path for key,path in config["input_files"].items()}
    trials=load_csv(paths["trials"],["participant_id","experience_group","condition","task_id","completion_seconds","tests_passed","tests_total","static_analysis_defects","critical_defects","prompt_count","accepted_suggestions","verification_actions"])
    reviews=load_csv(paths["reviews"],["participant_id","experience_group","seeded_defects_total","defects_detected","defects_correctly_fixed","review_seconds"])
    survey=load_csv(paths["survey"],["participant_id","experience_group","ai_uses_per_week","primary_ai_use"])
    validate_participants(trials,survey,reviews)
    sample=bool(config.get("sample_is_synthetic",False))
    result={
        "status":"SMOKE_TEST_SYNTHETIC_NOT_RESEARCH" if sample else "DESCRIPTIVE_ANALYSIS_NOT_HYPOTHESIS_PROOF",
        "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "research_title":config["study_title"],
        "python_version":sys.version.split()[0],
        "source_files":{k:str(v.relative_to(ROOT)) for k,v in paths.items()},
        "rq1_survey":analyze_survey(survey),
        "rq2_paired_task_results":analyze_trials(trials,config),
        "rq3_code_review":analyze_reviews(reviews),
        "limitations":["Synthetic sample must never be reported as findings.","Statistical significance requires a prespecified test and sufficient real participants.","Github Copilot interactions and task execution are recorded externally; not activated by this script."]
    }
    out=ROOT/config["output_dir"]
    out.mkdir(parents=True,exist_ok=True)
    report=out/"benchmark_results.json"
    report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (out/"benchmark.log").write_text(f"{result['generated_utc']} | {result['status']} | participants={result['rq2_paired_task_results']['paired_participants']} | generated={report.name}\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"primary_effect_pp":result["rq2_paired_task_results"]["primary_effect_experienced_minus_novice_percentage_points"],"guardrails":{g:v["guardrails_satisfied"] for g,v in result["rq2_paired_task_results"]["by_group"].items()},"results_file":str(report.relative_to(ROOT))},ensure_ascii=False,indent=2))
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Research Methods Task 2 paired-task smoke-test benchmark")
    parser.add_argument("--config",default="configs/config.json",type=Path)
    args=parser.parse_args()
    try:
        run(args.config if args.config.is_absolute() else ROOT/args.config)
    except (DataError, ValueError, KeyError, OSError, json.JSONDecodeError) as err:
        print(f"Benchmark failed: {err}",file=sys.stderr)
        sys.exit(1)
