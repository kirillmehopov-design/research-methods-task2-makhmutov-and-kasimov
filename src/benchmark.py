"""Run a secondary analysis of published Copilot measurements."""
import argparse
import json
import random
import statistics
import sys
from pathlib import Path

try:
    from .process_data import DataError, read_data, paired_changes, write_csv
except ImportError:
    from process_data import DataError, read_data, paired_changes, write_csv

ROOT = Path(__file__).resolve().parents[1]


def percentile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def interval(values):
    return [percentile(values, .025), percentile(values, .975)]


def summarize(records, config):
    repetitions = config['bootstrap_repetitions']
    if type(repetitions) is not int or repetitions < 100:
        raise DataError('Use at least 100 bootstrap repetitions')
    rng = random.Random(config['random_seed'])
    changes = paired_changes(records)
    by_group = {}
    for group in ('novice', 'expert'):
        people = [r for r in changes if r['experience_group'] == group]
        summary = {'participants': len(people), 'conditions': {}, 'paired_changes': {}}
        for mode in ('manual', 'automatic'):
            observations = [r for r in records if r['experience_group'] == group and r['mode'] == mode]
            summary['conditions'][mode] = {
                field: {'mean': statistics.mean(r[field] for r in observations),
                        'median': statistics.median(r[field] for r in observations),
                        'p95': percentile([r[field] for r in observations], .95)}
                for field in ('productivity_per_hour', 'completion_pct', 'time_minutes')}
        for field in ('productivity_per_hour_change', 'completion_pct_change', 'time_minutes_change'):
            values = [r[field] for r in people]
            samples = [statistics.mean(rng.choices(values, k=len(values))) for _ in range(repetitions)]
            summary['paired_changes'][field] = {'mean': statistics.mean(values), 'ci95': interval(samples)}
        completion = summary['paired_changes']['completion_pct_change']['mean']
        summary['completion_guardrail_met'] = completion >= -config['max_completion_drop_pp']
        by_group[group] = summary
    field = 'productivity_per_hour_change'
    values = {g: [r[field] for r in changes if r['experience_group'] == g] for g in by_group}
    boot = [statistics.mean(rng.choices(values['expert'], k=len(values['expert']))) -
            statistics.mean(rng.choices(values['novice'], k=len(values['novice'])))
            for _ in range(repetitions)]
    primary = statistics.mean(values['expert']) - statistics.mean(values['novice'])
    return {'analysis_type': 'secondary exploratory replication',
            'dataset_scope': config['dataset_scope'], 'participants': len(changes),
            'observations': len(records), 'baseline': 'manual Copilot invocation',
            'units': {'productivity': 'completed task fraction/hour', 'completion': 'percent', 'time': 'minutes'},
            'by_group': by_group,
            'primary_contrast': {'definition': 'expert mean paired change minus novice mean paired change',
                                 'estimate': primary, 'ci95': interval(boot)},
            'bootstrap': {'repetitions': repetitions, 'seed': config['random_seed'],
                          'unit': 'participant pair, resampled within experience group'},
            'limitations': ['Unadjusted estimates; task and order adjustment is planned for Task 3.',
                            'Experience was not randomly assigned.',
                            'Manual mode still uses Copilot.',
                            'Completion is not a full code quality or security assessment.',
                            'Bootstrap intervals describe sampling uncertainty within this convenience sample.']}, changes


def run(config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    records = read_data(ROOT, config)
    result, changes = summarize(records, config)
    output = ROOT / config['output_dir']
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'observations.csv', records)
    write_csv(output / 'paired_changes.csv', changes)
    (output / 'results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (output / 'benchmark.log').write_text(
        f"Published data analysis: {len(records)} observations, {len(changes)} participants.\n", encoding='utf-8')
    print(config['dataset_scope'])
    print(f"Published data: {len(changes)} participants, {len(records)} observations")
    print(f"Primary contrast: {result['primary_contrast']['estimate']:.4f} task fraction/hour")
    print('Output: ' + str(output))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'configs/config.json')
    args = parser.parse_args()
    try:
        run(args.config if args.config.is_absolute() else ROOT / args.config)
    except (DataError, OSError, ValueError, KeyError) as error:
        print(f'Analysis failed: {error}', file=sys.stderr)
        sys.exit(1)
