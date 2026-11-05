# Task 3 Analysis Notes

This is our exploratory **secondary analysis** of the published productivity tables, not a new experiment and not the original authors' statistical analysis. We use 66 sessions from 33 people (17 novices and 16 experts). Both Copilot modes provide AI suggestions. All numbers below come from `python -m src.task3_analysis`.

## Research questions

- **RQ1, novices:** Mean automatic-minus-manual productivity change is **+0.2901 completed task fraction/hour** (95% bootstrap CI **[+0.1338, +0.4560]**, 17 pairs). Automatic suggestions are associated with higher productivity in this group.
- **RQ2, experts:** Mean change is **-0.2759 completed task fraction/hour** (95% bootstrap CI **[-0.4954, -0.0489]**, 16 pairs). Manual invocation is associated with higher productivity in this group.
- **RQ3, group comparison:** Expert mean change minus novice mean change is **-0.5660 completed task fraction/hour** (95% bootstrap CI **[-0.8387, -0.2839]**). This is the main **unadjusted** estimate. It does not establish a causal effect of experience.

Bootstrap intervals use 10,000 participant-pair resamples within experience groups and seed 42. A leave-one-participant-out analysis gives **33** estimates, ranging from **-0.6233 to -0.5200**. No single removal reverses the sign. **This range is not a confidence interval.**

## Completion guardrail

We flag a group if average automatic-minus-manual task completion drops by **more than 5 percentage points**. Novices have **+32.21 points** (not flagged); experts have **-22.97 points** (flagged). This is a project-defined reporting threshold, **not** an established code-quality standard. Completion measures implemented task requirements; it is not test accuracy or security.

## Task assignment and session order

The [source paper, Section 5.4 and Table 1](https://doi.org/10.1007/s10664-026-10965-6) confirms four counterbalanced **first/second** task and suggestion-mode sequences, with a 15-minute break. Its table names these **#1-#4**. Our source CSVs instead use **A-D**. From the recorded sessions, A/D assign automatic mode to Task A and B/C assign automatic mode to Task B. **The available CSVs do not explicitly map A-D to the paper's numbered sequences or store first/second period.** CSV row order is not evidence of session order.

Therefore we can compare **task allocation**, but cannot estimate a separate session-order or carryover effect from these files. As a limited sensitivity check, we equally weight automatic-task A and B *within each experience group*. The resulting expert-minus-novice contrast is **-0.5773**, versus **-0.5660** unadjusted. This is **not** a full order-adjusted model. Individual task effects, practice effects, and any remaining confounding cannot be ruled out. Confirmed source-level period labels would be needed for an order-adjusted analysis.

## Remaining work

The other participant will handle the notebook, publication plots, README, dependencies/Docker, final report, and release. Cite the source authors and clearly separate their conclusions from our exploratory calculations. Keep zero-completion rows and genuine outliers; do not filter human sessions as technical warm-ups.
