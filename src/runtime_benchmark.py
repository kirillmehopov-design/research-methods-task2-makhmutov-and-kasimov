"""Measure CSV parsing and pair validation, separately from human outcomes."""
import json
import os
import platform
import random
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .benchmark import interval, percentile
from .process_data import parse_csv, read_data, validate_pairs, write_csv


def summarize_runtime(rows, config):
    summaries = []
    rng = random.Random(config['random_seed'])
    for workload in ('sample', 'full'):
        selected = [r for r in rows if r['workload'] == workload and r['phase'] == 'benchmark']
        valid = [r['elapsed_ms'] for r in selected if r['status'] == 'ok']
        if not valid:
            raise ValueError(f'No successful measurements for {workload}')
        boot = [statistics.mean(rng.choices(valid, k=len(valid)))
                for _ in range(config['bootstrap_repetitions'])]
        ci = interval(boot)
        q1, q3 = percentile(valid, .25), percentile(valid, .75)
        summaries.append(dict(
            workload=workload, input_rows=selected[0]['input_rows'], attempts=len(selected),
            successes=len(valid), errors=len(selected) - len(valid),
            error_rate=(len(selected) - len(valid)) / len(selected),
            mean_ms=statistics.mean(valid), sd_ms=statistics.stdev(valid),
            median_ms=statistics.median(valid), p25_ms=q1, p75_ms=q3,
            p95_ms=percentile(valid, .95), ci95_low_ms=ci[0], ci95_high_ms=ci[1],
            iqr_flags=sum(v < q1 - 1.5 * (q3 - q1) or v > q3 + 1.5 * (q3 - q1)
                          for v in valid),
        ))
    return summaries


def collect_runtime(root):
    root = Path(root)
    config = json.loads((root / 'configs/runtime.json').read_text())
    for key in ('warmup_runs', 'evaluation_runs', 'bootstrap_repetitions'):
        if type(config[key]) is not int or config[key] < 1:
            raise ValueError(f'Invalid {key}')
    if config['evaluation_runs'] < 2:
        raise ValueError('At least two evaluation runs are required')
    rows = []
    for workload, filename in (('sample', 'sample.json'), ('full', 'config.json')):
        source_config = json.loads((root / 'configs' / filename).read_text())
        validated = read_data(root, source_config)
        texts = [(group, (root / path).read_text(encoding='utf-8-sig'))
                 for group, path in source_config['input_files'].items()]
        for index in range(config['warmup_runs'] + config['evaluation_runs']):
            phase = 'warmup' if index < config['warmup_runs'] else 'benchmark'
            status, error_type = 'ok', ''
            start = time.perf_counter_ns()
            try:
                parsed = []
                for group, text in texts:
                    parsed.extend(parse_csv(text, group))
                validate_pairs(parsed)
            except Exception as error:
                status, error_type = 'error', type(error).__name__
            elapsed = (time.perf_counter_ns() - start) / 1_000_000
            rows.append(dict(workload=workload, run=index + 1, phase=phase,
                             input_rows=len(validated), elapsed_ms=elapsed,
                             status=status, error_type=error_type))
    output = root / 'data/raw'
    (output / 'test_run.jsonl').write_text(
        ''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
    metadata = dict(
        collected_at_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version.split()[0], os=platform.platform(),
        processor=platform.processor() or 'not reported', logical_cpus=os.cpu_count(),
        config=config, clock='time.perf_counter_ns',
        measured_operation='Parse preloaded CSV strings and validate participant pairs',
        excluded_from_timer='File reading, source hash checks, log writes, and summary calculation',
        interpretation='Local repeated timings of one fixed input; not human productivity evidence',
    )
    try:
        import psutil
        metadata['ram_bytes'] = psutil.virtual_memory().total
    except ImportError:
        metadata['ram_bytes'] = None
    (output / 'runtime_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    summaries = summarize_runtime(rows, config)
    write_csv(root / 'data/processed/runtime_summary.csv', summaries)
    return summaries


if __name__ == '__main__':
    for result in collect_runtime(Path(__file__).resolve().parents[1]):
        print(result)
