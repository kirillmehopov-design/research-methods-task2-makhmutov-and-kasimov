# Defense Notes

## Short presentation

Our project studies whether the productivity difference between automatic and manually requested GitHub Copilot suggestions depends on programmer experience. We use published experimental measurements from 17 novice and 16 experienced developers. Each participant completed one task in each mode.

Our main metric is the difference between the groups' average paired productivity changes. Productivity combines task completion and session time. Manual Copilot invocation is our baseline. We also report completion and time separately.

For Task 2, we prepared the methodology, source data, validation, configuration, tests and an executable analysis. The program checks the original file hashes, validates all 66 observations and calculates participant-level comparisons with confidence intervals. Task 3 will extend this with the notebook, plots and task/order sensitivity analysis.

## Questions

**Did you collect these data?** No. We use the published replication package and cite its authors. Our contribution is a reproducible secondary analysis and additional robustness checks.

**What changed from Task 1?** We narrowed the practical design to experience and productivity under two Copilot interaction modes, using available experimental data. We replaced the AI/no-AI comparison and removed the separate questionnaire and defect-review experiment.

**Does manual mean no AI?** No. Participants can request Copilot suggestions manually. The contrast concerns automatic versus on-demand suggestions.

**Why combine completion and time?** Some sessions end with incomplete tasks. Shorter time alone does not show higher successful performance. We use completed task fraction/hour and show both components separately.

**Why are there 33 participants rather than 66?** Each participant contributes two sessions. We retain this pairing in comparisons and bootstrap resampling.

**What does a negative primary contrast mean?** Experts have a smaller automatic-minus-manual productivity change than novices in this sample.

**What is the guardrail?** We flag an average completion drop exceeding five percentage points within either group. It is our reporting threshold, not a validated safety rule.

**What is new?** We do not claim a first discovery. This is a student replication with transparent calculations, uncertainty estimates and planned task/order and participant sensitivity checks.

**What does the working program prove?** It proves that we can validate and analyze the published data reproducibly. General recommendations still require interpretation of the design and limitations.

**What about warm-up?** Technical startup warm-up does not apply to these human task sessions. We document this and keep the source observations.
