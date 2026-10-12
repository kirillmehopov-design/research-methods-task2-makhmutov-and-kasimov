# Task 2 — Methodology Passport Card

**Project title:** The Influence of Programmer Experience Level on the Effectiveness of AI Tools in Programming  
**Authors:** Makhmutov Damir; Kasimov Amir  
**GitHub repository:** https://github.com/kirillmehopov-design/research-methods-task2-makhmutov-and-kasimov

## 1. Research type

**Mixed-methods, with a quantitative experimental core.** A brief questionnaire and analysis of interaction patterns describe how programmers use AI (RQ1). A controlled, counterbalanced within-participant comparison of matched programming tasks with GitHub Copilot versus without AI produces numeric performance measures (RQ2). A standardized review of the same AI-generated defective code measures verification ability (RQ3). Qualitative descriptions of AI-use purpose supplement logged counts; sample outputs are not research findings.

## 2. Hypotheses

**RQ1 — Patterns of AI-tool use**  
- **H0_1:** Novice and experienced programmers do not differ significantly in frequency, purposes, prompting, suggestion acceptance, or verification patterns of AI use.
- **H1_1:** They differ significantly in at least one of these AI-use patterns.

**RQ2 — Experience as a moderator of AI assistance**  
- **H0_2:** The effect of AI assistance on task completion time, functional correctness, and code quality does not differ by programmer experience group.
- **H1_2:** The benefit or cost of AI assistance on at least one of these outcomes differs by programmer experience group.

**RQ3 — Review of AI-generated code**  
- **H0_3:** Novice and experienced programmers do not differ significantly in detection and correct repair of known defects in AI-generated code.
- **H1_3:** Experienced programmers detect and correctly repair a greater proportion of seeded defects and/or complete review more efficiently than novices.

**Interpretation constraint:** experience level is observed rather than randomly assigned; causal claims about experience itself are not warranted. AI/no-AI task order is counterbalanced; the analysis examines moderation and group associations.

## 3. Variable matrix

| RQ | Independent variables | Dependent variables (measurement) | Controlled / confounding variables |
|---|---|---|---|
| RQ1 | Experience group: novice/experienced | Uses of AI per week; purposes; prompt count; accepted suggestions; verification actions | AI access, language, task category, questionnaire interval and definitions |
| RQ2 | Experience group; AI condition: GitHub Copilot vs no AI | Completion time (seconds); unit-test pass rate (0–1); static-analysis defect count; critical-defect count | Task difficulty, matched A/B assignments, tool and IDE version, language, hardware class, test suites, time limit, counterbalanced order |
| RQ3 | Experience group | Defects found (count and rate), correct fixes (count and rate), code-review time (seconds) | Identical AI-generated sample, seeded defect inventory, IDE, language, instructions, tests, time limit |

**Group definitions (from Task 1):** novice: at most 2 total years of programming and at most 6 months of professional experience. Experienced: at least 3 total years and at least 1 professional year. Exclude the middle experience band for clean groups in this pilot design.

## 4. Metrics and baseline

**Primary metric:** the *between-group difference in mean within-participant percentage reduction in programming task completion time due to AI*. For participant `i`, `benefit_i = 100 × (T_noAI,i − T_AI,i) / T_noAI,i`. Calculate the mean benefit within each group; the primary contrast is `mean_benefit_experienced − mean_benefit_novice` (percentage points). Its direction and confidence interval will be examined when real data are available. The included script provides descriptive summaries only.

**Guardrail metrics:** (1) AI assistance must not lower a group's average unit-test pass rate by more than **0.05** on the 0–1 scale, i.e., five percentage points, relative to the corresponding no-AI baseline; (2) AI-assisted outputs must have **zero critical defects**, defined using the predetermined defect-severity rubric. Both criteria are proposed decision thresholds, not observed outcomes.

**Secondary metrics:** static-analysis defects, functional pass rate, use frequency, prompt count, verification events, fraction of seeded review errors detected, fraction correctly fixed, and review time. Report outcomes separately, not as a single unvalidated quality score.

**Baseline (fair control):** each participant solves one matched task **without any AI assistant**, in the same environment and time limit. In the other condition the same person solves the alternative matched task with one fixed GitHub Copilot version; task assignments and condition order are counterbalanced to limit learning and task effects. RQ3 directly compares novice and experienced groups on *identical seeded-defect review material*.

## 5. Execution and deliverables

**Pipeline:** Python 3.12.12 in a digest-pinned Docker image; standard library only; `configs/config.json` holds paths, conditions and thresholds; `src/benchmark.py` validates sample inputs and writes `outputs/benchmark_results.json` plus `outputs/benchmark.log`. Eight synthetic trial observations (four paired participants) in `data/sample/trials.csv` exercise the end-to-end pipeline; separate review and survey micro-samples demonstrate RQ1/RQ3. Unit tests validate pairing and input errors.

**Reproducibility:** `docker build -t ai-experience-benchmark .` and `docker run --rm ai-experience-benchmark`. A successful synthetic smoke test proves the *pipeline is runnable*, not that the research hypotheses are supported. The environment has no external pip dependencies; no API keys, protected datasets, human identities or model weights are committed.

**Data integrity:** actual research will require participant consent, matched-task pilot evaluation, consistent test suites, recorded GitHub Copilot version, predefined statistical tests, and anonymized storage. Synthetic fixtures are not admissible as experimental findings.
