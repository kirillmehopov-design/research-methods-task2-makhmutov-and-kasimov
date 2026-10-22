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

## Task 3 plan

- Add `notebooks/01_data_analysis.ipynb`, run top to bottom with saved outputs.
- Add adjustment for task and order using the source assignment scheme; compare adjusted and unadjusted estimates. Check the assignment coding against the paper before modeling.
- Check sensitivity to individual participants and report all planned comparisons, including weak or opposite results.
- Export productivity comparisons, paired changes and completion summaries to vector PDF and 300-DPI PNG with units, colorblind-safe styles and uncertainty.
- Add `src/visualize.py`, processed summaries and Results & Discussion in README.
- Add a software-engineering domain model showing source tables, validation, pairing, analysis and reporting, with metric calculation points.
- Keep raw CSV data as published. A JSONL export may be added for the requested repository layout, with the original source retained. Technical cold-start filtering is not applicable to human session measurements; no observations are removed as warm-up.
- Record exact versions of any new notebook/plotting dependencies and verify a clean run before release.
