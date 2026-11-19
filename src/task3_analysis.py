"""Task 3 statistics for the published Copilot productivity sessions."""
import json
import statistics
import sys
from pathlib import Path

from .benchmark import percentile, summarize
from .process_data import DataError, paired_changes, read_data, write_csv


METRICS = {
    'productivity_per_hour': 'completed task fraction/hour',
    'completion_pct': 'percent',
    'time_minutes': 'minutes',
}


def describe(values):
    """Describe observations without assuming a normal distribution."""
    return {
        'n': len(values),
        'mean': statistics.mean(values),
        'sd': statistics.stdev(values) if len(values) > 1 else None,
        'median': statistics.median(values),
        'p25': percentile(values, .25),
        'p75': percentile(values, .75),
        'p95': percentile(values, .95),
    }


def leave_one_out(changes, full_estimate):
    """Recalculate the unadjusted contrast after excluding each participant."""
    estimates = []
    for omitted in changes:
        remaining = [row for row in changes if row['participant_id'] != omitted['participant_id']]
        means = {
            group: statistics.mean(row['productivity_per_hour_change'] for row in remaining
                                   if row['experience_group'] == group)
            for group in ('novice', 'expert')
        }
        estimates.append({
            'participant_id': omitted['participant_id'],
            'experience_group': omitted['experience_group'],
            'estimate': means['expert'] - means['novice'],
        })

    def sign(value):
        return (value > 0) - (value < 0)

    values = [item['estimate'] for item in estimates]
    return {
        'full_estimate': full_estimate,
        'estimates': estimates,
        'min': min(values),
        'max': max(values),
        'sign_changed': any(sign(value) != sign(full_estimate) for value in values),
        'note': 'Sensitivity range, not a confidence interval.',
    }


def task_allocation_sensitivity(records, changes):
    """Equal-weight known automatic-task assignments, without guessing session order."""
    automatic_task = {
        row['participant_id']: row['task'] for row in records if row['mode'] == 'automatic'
    }
    by_group = {}
    for group in ('novice', 'expert'):
        cells = {}
        for task in ('A', 'B'):
            values = [row['productivity_per_hour_change'] for row in changes
                      if row['experience_group'] == group
                      and automatic_task[row['participant_id']] == task]
            if not values:
                raise DataError(f'No participants for {group}, automatic task {task}')
            cells[task] = {'n': len(values), 'mean_paired_change': statistics.mean(values)}
        by_group[group] = {
            'by_automatic_task': cells,
            'equal_task_weight_mean': statistics.mean(cells[task]['mean_paired_change']
                                                      for task in ('A', 'B')),
        }
    return {
        'method': 'Equal weights for automatic-task A and B in each experience group',
        'by_group': by_group,
        'primary_contrast': (
            by_group['expert']['equal_task_weight_mean'] -
            by_group['novice']['equal_task_weight_mean']
        ),
        'limitation': 'Task-allocation sensitivity only; session order and carryover are not adjusted.',
    }


def build_analysis(root):
    """Build JSON-compatible Task 3 results without writing any files."""
    root = Path(root)
    config = json.loads((root / 'configs/config.json').read_text(encoding='utf-8'))
    records = read_data(root, config)
    result, changes = summarize(records, config)

    for group in ('novice', 'expert'):
        for mode in ('manual', 'automatic'):
            for metric in METRICS:
                values = [row[metric] for row in records
                          if row['experience_group'] == group and row['mode'] == mode]
                result['by_group'][group]['conditions'][mode][metric].update(describe(values))
        for metric in METRICS:
            field = metric + '_change'
            values = [row[field] for row in changes if row['experience_group'] == group]
            result['by_group'][group]['paired_changes'][field].update(describe(values))

    result['leave_one_out'] = leave_one_out(changes, result['primary_contrast']['estimate'])
    result['task_allocation_sensitivity'] = task_allocation_sensitivity(records, changes)
    result['limitations'][0] = (
        'Unadjusted primary results. Task allocation is standardized in a sensitivity check; '
        'the CSV does not verify session order for an order-adjusted analysis.'
    )
    return result


def metric_rows(results):
    """Create rows for the group-by-mode CSV summary."""
    rows = []
    for group in ('novice', 'expert'):
        for mode in ('manual', 'automatic'):
            for metric, unit in METRICS.items():
                row = results['by_group'][group]['conditions'][mode][metric]
                rows.append(dict(
                    experience_group=group, mode=mode, metric=metric, unit=unit,
                    n=row['n'], mean=row['mean'], sd=row['sd'], median=row['median'],
                    p25=row['p25'], p75=row['p75'], p95=row['p95'],
                ))
    return rows


def save_analysis(root, results):
    """Save validated source-derived records and the computed results."""
    root = Path(root)
    config = json.loads((root / 'configs/config.json').read_text(encoding='utf-8'))
    records = read_data(root, config)
    changes = paired_changes(records)
    if len(records) != results['observations'] or len(changes) != results['participants']:
        raise DataError('Analysis and source row counts disagree')
    output = root / 'data/processed'
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'observations.csv', records)
    write_csv(output / 'paired_changes.csv', changes)
    write_csv(output / 'metrics_summary.csv', metric_rows(results))
    (output / 'results.json').write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8'
    )


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        results = build_analysis(root)
        save_analysis(root, results)
    except (DataError, OSError, ValueError, KeyError) as error:
        print(f'Task 3 analysis failed: {error}', file=sys.stderr)
        return 1
    print(f"Saved {results['observations']} sessions and "
          f"{results['participants']} pairs to data/processed/")
    print(f"Unadjusted expert-minus-novice contrast: "
          f"{results['primary_contrast']['estimate']:.6f} task fraction/hour")
    return 0


if __name__ == '__main__':
    sys.exit(main())
