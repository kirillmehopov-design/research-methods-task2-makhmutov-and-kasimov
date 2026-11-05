"""Check warm-up exclusion and failure accounting independently of machine speed."""
import unittest

from src.runtime_benchmark import summarize_runtime


class RuntimeTests(unittest.TestCase):
    def test_warmup_is_excluded_but_errors_count(self):
        rows = []
        for workload in ('sample', 'full'):
            for phase, status, value in [('warmup', 'ok', 999),
                                          ('benchmark', 'ok', 1),
                                          ('benchmark', 'ok', 3),
                                          ('benchmark', 'error', 100)]:
                rows.append(dict(workload=workload, phase=phase, status=status,
                                 elapsed_ms=value, input_rows=8))
        results = summarize_runtime(rows, {'random_seed': 42, 'bootstrap_repetitions': 100})
        for row in results:
            self.assertEqual(row['attempts'], 3)
            self.assertEqual(row['errors'], 1)
            self.assertEqual(row['error_rate'], 1 / 3)
            self.assertEqual(row['mean_ms'], 2)
            self.assertEqual(row['median_ms'], 2)


if __name__ == '__main__':
    unittest.main()
