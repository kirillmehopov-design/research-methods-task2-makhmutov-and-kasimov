import copy
import json
import unittest
from unittest.mock import patch

from src.benchmark import ROOT, percentile, summarize
from src.process_data import DataError, parse_csv, read_data, validate_pairs, paired_changes


class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / 'configs/config.json').read_text())
        cls.records = read_data(ROOT, cls.config)

    def test_full_source_and_formula(self):
        self.assertEqual(len(self.records), 66)
        self.assertEqual(len(paired_changes(self.records)), 33)
        for r in self.records:
            self.assertAlmostEqual(r['productivity_per_hour'], .6 * r['completion_pct'] / r['time_minutes'])

    def test_real_sample_has_four_complete_pairs(self):
        config = json.loads((ROOT / 'configs/sample.json').read_text())
        rows = read_data(ROOT, config)
        self.assertEqual(len(rows), 8)
        self.assertEqual(len(paired_changes(rows)), 4)

    def test_missing_pair_is_rejected(self):
        with self.assertRaises(DataError):
            validate_pairs(self.records[1:])

    def test_duplicate_is_rejected(self):
        with self.assertRaises(DataError):
            validate_pairs(self.records + [self.records[0]])

    def test_inconsistent_group_is_rejected(self):
        rows = copy.deepcopy(self.records)
        rows[0]['experience_group'] = 'novice'
        with self.assertRaises(DataError):
            validate_pairs(rows)

    def test_bad_source_values_are_rejected(self):
        header = 'User ID,Study group,Session,Completeness,Time(min),PRODa\n'
        for values in ('50,0,0', '101,60,1.01', 'nan,60,0', '50,60,1'):
            with self.subTest(values=values), self.assertRaises(DataError):
                parse_csv(header + 'test,A,SUGG enabled - Task A,' + values, 'novice')

    def test_unknown_session_and_assignment_are_rejected(self):
        header = 'User ID,Study group,Session,Completeness,Time(min),PRODa\n'
        for session in ('AI disabled', 'SUGG enabled - Task B'):
            with self.subTest(session=session), self.assertRaises(DataError):
                parse_csv(header + f'test,A,{session},50,60,"0,5"', 'novice')

    def test_zero_completion_is_kept(self):
        self.assertTrue(any(r['completion_pct'] == 0 for r in self.records))

    def test_checksum_detects_changed_source(self):
        with patch('pathlib.Path.read_bytes', return_value=b'changed'):
            with self.assertRaises(DataError):
                read_data(ROOT, self.config)

    def test_paired_change_sign_and_primary_contrast(self):
        config = dict(self.config, bootstrap_repetitions=100)
        result, changes = summarize(self.records, config)
        means = {}
        for group in ('expert', 'novice'):
            delta = [r['productivity_per_hour_change'] for r in changes if r['experience_group'] == group]
            means[group] = sum(delta) / len(delta)
        self.assertAlmostEqual(result['primary_contrast']['estimate'], means['expert'] - means['novice'])
        self.assertEqual(result['by_group']['expert']['participants'], 16)
        self.assertEqual(result['by_group']['novice']['participants'], 17)

    def test_bootstrap_is_reproducible_and_uses_pairs(self):
        config = dict(self.config, bootstrap_repetitions=100)
        a, _ = summarize(self.records, config)
        b, _ = summarize(list(reversed(self.records)), config)
        self.assertEqual(a, b)

    def test_percentile_interpolation(self):
        self.assertEqual(percentile([0, 10], .95), 9.5)


if __name__ == '__main__':
    unittest.main()
