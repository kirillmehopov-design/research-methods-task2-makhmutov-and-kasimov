"""Write the Task 3 report directly from saved results."""
import csv
import json
from pathlib import Path


def mean_sd(value):
    return f"{value['mean']:.3f} ± {value['sd']:.3f}"


def change_ci(value):
    low, high = value['ci95']
    return f"{value['mean']:+.3f} [{low:+.3f}, {high:+.3f}]"


def write_report(root):
    root = Path(root)
    results = json.loads((root / 'data/processed/results.json').read_text())
    lines = [
        '# Task 3 Research Results and Data Analysis',
        '',
        '**Authors:** Damir Makhmutov and Amir Kasimov',
        '',
        'We examine whether automatic versus manually requested Copilot suggestions are associated '
        'with different productivity changes for novice and experienced programmers. This report '
        'presents our exploratory secondary analysis of published data and a separate local benchmark '
        'of our data-processing code. The two datasets answer different questions and are never pooled.',
        '',
        '## Data and methods',
        '',
        'The source productivity tables contain 66 sessions from 33 participants: 17 novices and '
        '16 experts. Each participant has one session per mode, on different Java tasks. Manual '
        'invocation is the baseline and still provides Copilot. We retain all published rows, '
        'including zero completion, verify file hashes, check task allocation, and independently '
        'recalculate productivity. No participants are recruited for this project.',
        '',
        '`Productivity = (completion_percent / 100) / (time_minutes / 60)`',
        '',
        'The unit is completed task fraction per hour. Changes are automatic minus manual. '
        'The primary contrast is the experts’ mean change minus the novices’ mean change. '
        'All 95% confidence intervals use 10,000 bootstrap draws of whole participant pairs '
        'within experience groups, with seed 42. SD is the sample standard deviation; it describes '
        'dispersion, whereas a confidence interval describes estimation uncertainty. '
        'Medians, quartiles, and p95 are available in the saved summary CSV.',
        '',
        '## Results and Discussion',
        '',
        'Manual is the baseline; automatic is the comparison condition, not a method invented by us. '
        'Mode values below are mean ± SD. Changes are mean [95% CI].',
        '',
        '| Group | Outcome (unit) | Manual baseline | Automatic | Paired change [95% CI] |',
        '| --- | --- | --- | --- | --- |',
    ]
    metrics = [('productivity_per_hour', 'Productivity (task fraction/hour)'),
               ('completion_pct', 'Completion (%; change in pp)'),
               ('time_minutes', 'Session time (minutes)')]
    for group in ('novice', 'expert'):
        entry = results['by_group'][group]
        for metric, label in metrics:
            lines.append(f"| {group.title()} (n={entry['participants']}) | {label} | "
                         f"{mean_sd(entry['conditions']['manual'][metric])} | "
                         f"{mean_sd(entry['conditions']['automatic'][metric])} | "
                         f"{change_ci(entry['paired_changes'][metric + '_change'])} |")
    primary = results['primary_contrast']
    low, high = primary['ci95']
    loo = results['leave_one_out']
    sensitivity = results['task_allocation_sensitivity']['primary_contrast']
    lines += [
        '',
        '**RQ1:** Automatic suggestions are associated with higher productivity among novices '
        'in this sample. **RQ2:** Experts show the opposite average change. '
        f"**RQ3:** The direct expert-minus-novice contrast is **{primary['estimate']:+.4f}** "
        f'task fraction/hour (95% CI [{low:+.4f}, {high:+.4f}]). '
        'This conclusion uses the direct group comparison, not a comparison of two significance decisions.',
        '',
        '![Paired changes and primary contrast](figures/fig1_paired_changes.png)',
        '',
        '*Figure 1. Mean automatic-minus-manual productivity changes and the direct group contrast. '
        'Whiskers are participant-pair bootstrap 95% CIs. The dashed line marks no change.*',
        '',
        '![Productivity distribution and participant pairs](figures/fig2_productivity_distribution.png)',
        '',
        '*Figure 2. All participant outcomes, linked within each pair. Boxes show p25–p75, '
        'the centre line is the median, and whiskers extend to observations within 1.5 IQR. '
        'All observations are plotted. Black diamonds and their bars show means and bootstrap 95% CIs.*',
        '',
        '![Completion and time changes](figures/fig3_completion_time.png)',
        '',
        '*Figure 3. Mean paired completion and session-time changes with bootstrap 95% CIs. '
        'The dotted completion line is the project-defined −5 percentage-point reporting threshold.*',
        '',
        'Completion rises by 32.21 percentage points for novices but falls by 22.97 points '
        'for experts, triggering the expert completion guardrail. Session time increases in '
        'both groups, so the novice productivity increase must not be described as faster completion. '
        'Completion is a task score, not a security or comprehensive code-quality measure.',
        '',
        '## Robustness and limits',
        '',
        f"Removing each participant in turn gives contrasts from {loo['min']:+.4f} "
        f"to {loo['max']:+.4f}; no single removal changes the sign. This is a sensitivity range, "
        'not a confidence interval. '
        f'Equal weighting of automatic-task A and B within each group gives {sensitivity:+.4f}. '
        'This checks task-allocation imbalance but does not adjust session order or carryover.',
        '',
        'The source paper describes four counterbalanced sequences, but the released productivity '
        'CSVs use A–D labels without an explicit mapping to the numbered sequence table or first/second '
        'period. We do not infer period from row order. Further order adjustment would require confirmed '
        'source-level period labels. Experience is not randomized; the small convenience sample, '
        'task differences, scoring, and historical Copilot setting limit generalization. '
        'Data and published findings were available before our analysis plan: this is not preregistered. '
        'The bootstrap does not remove confounding or selection bias. These results do not establish '
        'that automatic suggestions cause a benefit or harm for all programmers.',
        '',
        '## Supplementary code benchmark',
        '',
        'To address the technical logging requirements, we separately measure parsing and pair '
        'validation on 8-row and 66-row source inputs. Text loading and source integrity checks '
        'happen before timing; log writes and aggregation happen afterwards. Each workload has '
        '20 warm-up attempts followed by 100 evaluation attempts. Only warm-up timing records '
        'are excluded from technical summaries. No human session is removed as warm-up.',
        '',
        '| Input | Evaluation attempts | Errors | Mean time (ms) [95% CI] | Median (ms) | p95 (ms) | IQR flags kept |',
        '| --- | --- | --- | --- | --- | --- | --- |',
    ]
    with (root / 'data/processed/runtime_summary.csv').open(newline='') as handle:
        for row in csv.DictReader(handle):
            lines.append(f"| {row['input_rows']} rows | {row['attempts']} | {row['errors']} | "
                         f"{float(row['mean_ms']):.4f} [{float(row['ci95_low_ms']):.4f}, "
                         f"{float(row['ci95_high_ms']):.4f}] | {float(row['median_ms']):.4f} | "
                         f"{float(row['p95_ms']):.4f} | {row['iqr_flags']} |")
    lines += [
        '',
        '![Local parsing benchmark](figures/fig4_runtime.png)',
        '',
        '*Figure 4. Local mean parsing/validation time for two fixed input sizes. Bars are '
        '2,000-draw bootstrap 95% intervals over successful evaluation timings, seed 42.*',
        '',
        'Failures remain in JSONL and count toward the error rate; latency summaries describe '
        'successful attempts only. IQR flags are descriptive and never delete measurements. '
        'This is one local, sequential run without strict CPU isolation; repeated timings can be '
        'correlated and affected by background activity. The intervals describe this run and are '
        'not hardware-independent performance guarantees. Rerunning changes timings. '
        'These measurements provide no additional Copilot participant evidence.',
        '',
        '## Reproduction and submission',
        '',
        'From the repository root with Python 3.12:',
        '',
        '```sh',
        'python -m venv .venv',
        '# Activate .venv using the command for your operating system.',
        'python -m pip install -r requirements.lock.txt',
        'python -m unittest discover -s tests -v',
        'python -m src.run_task3',
        '```',
        '',
        'The final command recalculates statistics, collects new local timings, exports PDF/PNG '
        'figures, regenerates this report, and executes the notebook in a fresh kernel. '
        'The checked-in notebook retains its outputs. Scientific data results should match; '
        'timing results and machine metadata should change. See [the repository README](../README.md) '
        'for Docker commands and [the requirement checklist](../docs/task3_checklist.md) for coverage.',
        '',
        '## Sources and attribution',
        '',
        'Guglielmi, E., Arnoudova, V., Bavota, G., Oliveto, R., and Scalabrino, S. '
        '*How do Copilot Suggestions Impact Developers’ Frustration and Productivity?* '
        '[Source paper](https://doi.org/10.1007/s10664-026-10965-6). '
        '[Replication package](https://figshare.com/s/2f26b8ee294a3a87c908). '
        'The original productivity CSVs retain their bytes and CC BY 4.0 attribution; '
        'see [data provenance](../data/README.md). Our statistical estimates and local runtime '
        'measurements are produced by this repository.',
    ]
    destination = root / 'reports/task3_report.md'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return destination
