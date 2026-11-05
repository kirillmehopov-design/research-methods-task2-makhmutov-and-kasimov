# Analysis Protocol

## Inputs

Use the original `PRODa-expert.csv` and `PRODa-novice.csv` from the source replication package. Record provenance and verify SHA-256 hashes before parsing. No new participant recruitment or Copilot sessions are needed.

## Processing

1. Read the decimal-comma values and normalize the two time-column spellings.
2. Keep the source participant IDs, group, task and assignment labels.
3. Check finite values, completion between 0 and 100, positive time and agreement with published productivity.
4. Require exactly one automatic and one manual observation for each participant, consistent metadata and different tasks. Stop on invalid input rather than silently dropping records.
5. Calculate productivity as completed task fraction/hour. Preserve zero-completion observations.
6. Compute automatic-minus-manual changes for each participant.
7. Report group/mode means, medians and p95, paired mean changes and the primary between-group contrast.
8. Use 10,000 percentile-bootstrap repetitions, seed 42, sampling complete pairs within each experience group. Do not bootstrap individual sessions independently.

## Interpretation

The script provides unadjusted estimates and 95% intervals, not the source authors' exact hypothesis-test replication. It does not run their scripts. Results are exploratory because the dataset and published findings were already inspected. A bootstrap interval is not a guarantee of population representativeness. No causal effect of experience itself is claimed.

Both conditions allow Copilot. Time is recorded session time, including partially completed work; it is not always time to a fully correct solution. Completion is a task score and should not be relabeled test accuracy or security. The five-percentage-point completion guardrail is a reporting threshold chosen for this project.

## Task 3 implementation

The completed notebook is `notebooks/01_data_analysis.ipynb`. It runs in a fresh kernel and retains visible outputs. `src/task3_analysis.py` adds sample SD, quartiles, participant leave-one-out checks, and equal-task-weight sensitivity. The primary estimate remains unadjusted. Order adjustment is not supported by confirmed first/second-period labels in the available CSVs; this limitation is retained rather than guessing a mapping.

`src/visualize.py` exports four vector PDFs and 300-DPI PNGs. `src/report.py` generates the report from saved outputs. The C4 model in `docs/domain_model.md` marks data acquisition and metric-calculation points. Exact dependencies are pinned in `requirements.lock.txt`.

A separate technical collector, `src/runtime_benchmark.py`, times parsing preloaded source text and validating pairs. It records 20 warm-up and 100 evaluation attempts per input size as JSONL. All errors count in the denominator; successful timings supply latency statistics. IQR flags retain all records. Bootstrap intervals over runtime attempts are descriptive of one local run, not independent hardware trials. Human sessions and technical attempts are never pooled.

Use `python -m src.run_task3` for the full rebuild, then `python -m src.check_submission` for artifact checks.
