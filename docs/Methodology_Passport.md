# Methodology Passport

**Title:** Copilot Interaction Mode and Productivity Across Programmer Experience Levels
**Authors:** Makhmutov Damir and Kasimov Amir
**Repository:** https://github.com/kirillmehopov-design/research-methods-task2-makhmutov-and-kasimov

## Research type

Quantitative secondary analysis of a published quasi-experiment. We compare paired outcomes under automatic and manually requested Copilot suggestions and examine differences between experience groups. We use the authors' existing data rather than conduct a new participant experiment.

## Object, subject and aim

The object is AI-assisted programming. The subject is the relationship between Copilot interaction mode, programmer experience and task productivity. Our aim is to estimate mode-related productivity changes within each group and compare those changes between groups using reproducible calculations.

## Questions and hypotheses

Let P be completed task fraction per hour and D = P_automatic - P_manual for each participant.

| Question | Null hypothesis | Alternative hypothesis |
| --- | --- | --- |
| RQ1: How does mode affect novices' productivity? | H01: Mean D among novices is zero. | H11: Mean D among novices is not zero. |
| RQ2: How does mode affect experts' productivity? | H02: Mean D among experts is zero. | H12: Mean D among experts is not zero. |
| RQ3: Does the mode-related change differ by experience? | H03: Mean D among experts equals mean D among novices. | H13: The two means differ. |

RQ3 is primary. These are two-sided replication hypotheses. Data and published findings were available before this plan, so we do not claim preregistration. A difference in within-group significance alone is not evidence of a between-group difference.

## Variables

| Type | Variables and definitions |
| --- | --- |
| Factors | Copilot mode: automatic/manual; experience: novice/expert as classified by the source authors |
| Primary outcome | Expert mean paired productivity change minus novice mean paired change, in task fraction/hour |
| Additional outcomes | Within-group productivity change; completion (%); time (minutes) |
| Recorded design factors | Java task A/B and assignment group A/B/C/D, which encode task/mode allocation and order |
| Fixed source setting | GitHub Copilot, Java maintenance tasks, source-study instructions and scoring procedure |
| Remaining limitations | Convenience sampling, different participant skills, incomplete tasks and source-study conditions |

Source eligibility: novices were computing students with less than three years of programming experience; experts were industry developers with at least three years. We preserve the published group labels. The original Task 1 thresholds are replaced with the source study's definitions.

## Metrics and baseline

P = (completion percent / 100) / (minutes / 60). A value of 0.5 means half a task per hour. Manual invocation is the baseline; it still provides Copilot access. Neither condition is an AI-free control.

Primary metric: mean(D_expert) - mean(D_novice). Positive values mean a larger automatic-mode benefit for experts. Secondary metrics show productivity, completion and time separately. The completion guardrail flags an average automatic-minus-manual drop exceeding five percentage points within either group. This threshold is a student-defined reporting rule, not an established quality standard. Source data do not support a critical-security-defect guardrail.

## Data and analysis

The published productivity tables contain 66 task sessions from 33 participants (16 experts, 17 novices). Each participant has one session in each mode and two different tasks. Original CSV files, source links and hashes are retained. Eight real rows form the test sample.

The current pipeline validates the data, computes participant pairs, summaries, mean changes and percentile-bootstrap 95% intervals. Resampling uses whole participant pairs within each experience group. Task 3 will add adjustment/sensitivity checks for task and order, leave-one-participant-out checks and the final notebook and figures. Repeated sessions are not treated as independent participants.

## Research tasks

1. Review literature on experience and AI-assisted programming.
2. Document and validate the published data and mode definitions.
3. Recalculate productivity and paired differences.
4. Estimate uncertainty and examine task/order sensitivity.
5. Present results, limitations and practical implications in the report and defense.

## Reproducibility and ethics

Python 3.12.12 and a digest-pinned Docker image provide the runtime. The analysis needs no external Python packages or AI account. The code, configuration and small source tables allow offline execution after setup. The original researchers collected the observations. We use published participant IDs and do not attempt identification. Cite the source paper and CC BY 4.0 data package.

Source: Guglielmi et al., *How do Copilot Suggestions Impact Developers' Frustration and Productivity?*, https://doi.org/10.1007/s10664-026-10965-6. Data: https://figshare.com/s/2f26b8ee294a3a87c908.
