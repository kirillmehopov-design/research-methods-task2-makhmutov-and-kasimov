"""Checks for the published-data Task 3 statistics and saved outputs."""
import csv
import json
import math
import subprocess
import sys
import unittest
from unittest.mock import patch

from src.benchmark import ROOT, percentile, summarize
from src.process_data import paired_changes, read_data
from src.task3_analysis import (build_analysis, describe, leave_one_out,
                                metric_rows, save_analysis)


class Task3AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / 'configs/config.json').read_text(encoding='utf-8'))
        cls.records = read_data(ROOT, cls.config)
        cls.results = build_analysis(ROOT)

    def test_full_dataset_and_original_unadjusted_contrast(self):
        self.assertEqual(len(self.records), 66)
        self.assertEqual(len(paired_changes(self.records)), 33)
        self.assertEqual(self.results['observations'], 66)
        self.assertEqual(self.results['participants'], 33)
        original, _ = summarize(self.records, self.config)
        self.assertEqual(self.results['primary_contrast'], original['primary_contrast'])
        self.assertEqual(self.results['bootstrap'], original['bootstrap'])
        self.assertEqual(self.results['by_group']['expert']['participants'], 16)
        self.assertEqual(self.results['by_group']['novice']['participants'], 17)

    def test_sample_sd_and_linear_percentiles(self):
        stats = describe([1, 2, 3, 4])
        self.assertEqual(stats['n'], 4)
        self.assertAlmostEqual(stats['sd'], math.sqrt(5 / 3))
        self.assertEqual(stats['median'], 2.5)
        self.assertEqual(stats['p25'], 1.75)
        self.assertEqual(stats['p75'], 3.25)
        self.assertEqual(stats['p95'], percentile([1, 2, 3, 4], .95))
        self.assertEqual(describe([4])['sd'], None)

    def test_mode_statistics_match_source_records(self):
        for group in ('expert', 'novice'):
            for mode in ('automatic', 'manual'):
                sessions = [row for row in self.records
                            if row['experience_group'] == group and row['mode'] == mode]
                for metric in ('productivity_per_hour', 'completion_pct', 'time_minutes'):
                    values = [row[metric] for row in sessions]
                    self.assertEqual(self.results['by_group'][group]['conditions'][mode][metric],
                                     describe(values))
        self.assertEqual(len(metric_rows(self.results)), 12)
        self.assertTrue(any(row['completion_pct'] == 0 for row in self.records))

    def test_leave_one_out_exact_and_sign(self):
        pairs = [
            {'participant_id': 'e1', 'experience_group': 'expert',
             'productivity_per_hour_change': 2.0},
            {'participant_id': 'e2', 'experience_group': 'expert',
             'productivity_per_hour_change': -2.0},
            {'participant_id': 'n1', 'experience_group': 'novice',
             'productivity_per_hour_change': -.5},
            {'participant_id': 'n2', 'experience_group': 'novice',
             'productivity_per_hour_change': -.5},
        ]
        result = leave_one_out(pairs, .5)
        self.assertEqual([entry['estimate'] for entry in result['estimates']],
                         [-1.5, 2.5, .5, .5])
        self.assertEqual((result['min'], result['max']), (-1.5, 2.5))
        self.assertTrue(result['sign_changed'])
        self.assertNotIn('ci95', result)

    def test_full_leave_one_out_and_task_sensitivity(self):
        loo = self.results['leave_one_out']
        self.assertEqual(len(loo['estimates']), 33)
        self.assertEqual(loo['min'], min(row['estimate'] for row in loo['estimates']))
        self.assertEqual(loo['max'], max(row['estimate'] for row in loo['estimates']))
        sensitivity = self.results['task_allocation_sensitivity']
        for group, size in (('novice', 17), ('expert', 16)):
            cells = sensitivity['by_group'][group]['by_automatic_task']
            self.assertEqual(cells['A']['n'] + cells['B']['n'], size)
            self.assertGreater(cells['A']['n'], 0)
            self.assertGreater(cells['B']['n'], 0)

    def test_pure_function_and_reproducibility(self):
        with patch('pathlib.Path.write_text', side_effect=AssertionError('wrote a file')):
            again = build_analysis(ROOT)
        self.assertEqual(self.results, again)
        self.assertEqual(self.results['bootstrap']['seed'], 42)
        self.assertEqual(self.results['bootstrap']['repetitions'], 10000)

    def test_cli_and_saved_outputs(self):
        completed = subprocess.run([sys.executable, '-m', 'src.task3_analysis'],
                                   cwd=ROOT, check=True, capture_output=True, text=True)
        self.assertIn('66 sessions', completed.stdout)
        output = ROOT / 'data/processed'
        with (output / 'results.json').open(encoding='utf-8') as handle:
            self.assertEqual(json.load(handle), self.results)
        for filename, expected in (('observations.csv', 66), ('paired_changes.csv', 33),
                                   ('metrics_summary.csv', 12)):
            with (output / filename).open(encoding='utf-8', newline='') as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), expected)
        with (output / 'metrics_summary.csv').open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0].keys(), {
            'experience_group': None, 'mode': None, 'metric': None, 'unit': None,
            'n': None, 'mean': None, 'sd': None, 'median': None,
            'p25': None, 'p75': None, 'p95': None,
        }.keys())
        self.assertAlmostEqual(float(rows[0]['sd']),
                               self.results['by_group']['novice']['conditions']['manual']
                               ['productivity_per_hour']['sd'])


if __name__ == '__main__':
    unittest.main()
