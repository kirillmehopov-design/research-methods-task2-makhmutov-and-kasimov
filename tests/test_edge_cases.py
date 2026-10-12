"""Additional regression tests for the Task 2 measurement pipeline.

These tests exercise invalid or unsafe input, and verify that the report's
predeclared quality guardrails are applied consistently. No real participant
measurements or GitHub Copilot credentials are required.
"""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.benchmark import (  # noqa: E402
    DataError,
    analyze_reviews,
    analyze_survey,
    analyze_trials,
    load_csv,
)


class EdgeCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "configs/config.json").read_text(encoding="utf-8"))
        cls.trials = load_csv(
            ROOT / "data/sample/trials.csv",
            ["participant_id", "experience_group", "condition", "task_id", "completion_seconds",
             "tests_passed", "tests_total", "static_analysis_defects", "critical_defects",
             "prompt_count", "accepted_suggestions", "verification_actions"],
        )
        cls.reviews = load_csv(
            ROOT / "data/sample/reviews.csv",
            ["participant_id", "experience_group", "seeded_defects_total",
             "defects_detected", "defects_correctly_fixed", "review_seconds"],
        )
        cls.survey = load_csv(
            ROOT / "data/sample/survey.csv",
            ["participant_id", "experience_group", "ai_uses_per_week", "primary_ai_use"],
        )

    def test_zero_completion_time_rejected(self):
        trials = copy.deepcopy(self.trials)
        trials[0]["completion_seconds"] = "0"
        with self.assertRaises(DataError):
            analyze_trials(trials, self.config)

    def test_nonfinite_completion_time_rejected(self):
        trials = copy.deepcopy(self.trials)
        trials[0]["completion_seconds"] = "nan"
        with self.assertRaises(DataError):
            analyze_trials(trials, self.config)

    def test_duplicate_ai_condition_rejected(self):
        trials = copy.deepcopy(self.trials)
        duplicate = copy.deepcopy(next(row for row in trials if row["participant_id"] == "P001" and row["condition"] == "ai"))
        trials.append(duplicate)
        with self.assertRaises(DataError):
            analyze_trials(trials, self.config)

    def test_critical_defect_guardrail_detects_violation(self):
        trials = copy.deepcopy(self.trials)
        ai_trial = next(row for row in trials if row["experience_group"] == "novice" and row["condition"] == "ai")
        ai_trial["critical_defects"] = "1"
        summary = analyze_trials(trials, self.config)
        self.assertFalse(summary["by_group"]["novice"]["guardrails_satisfied"])
        self.assertTrue(summary["by_group"]["experienced"]["guardrails_satisfied"])

    def test_pass_rate_guardrail_detects_violation(self):
        trials = copy.deepcopy(self.trials)
        for row in trials:
            if row["experience_group"] == "experienced" and row["condition"] == "ai":
                row["tests_passed"] = "8"
        summary = analyze_trials(trials, self.config)
        self.assertFalse(summary["by_group"]["experienced"]["guardrails_satisfied"])

    def test_review_cannot_fix_more_than_detected(self):
        reviews = copy.deepcopy(self.reviews)
        reviews[0]["defects_correctly_fixed"] = "4"
        reviews[0]["defects_detected"] = "3"
        with self.assertRaises(DataError):
            analyze_reviews(reviews)

    def test_duplicate_survey_response_rejected(self):
        survey = copy.deepcopy(self.survey)
        survey.append(copy.deepcopy(survey[0]))
        with self.assertRaises(DataError):
            analyze_survey(survey)

    def test_negative_weekly_frequency_rejected(self):
        survey = copy.deepcopy(self.survey)
        survey[0]["ai_uses_per_week"] = "-1"
        with self.assertRaises(DataError):
            analyze_survey(survey)


if __name__ == "__main__":
    unittest.main()
