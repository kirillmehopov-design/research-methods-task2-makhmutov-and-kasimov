import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.benchmark import DataError, analyze_trials, analyze_reviews, analyze_survey, load_csv, validate_participants


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((ROOT/"configs/config.json").read_text(encoding="utf-8"))
        cls.trials=load_csv(ROOT/"data/sample/trials.csv",["participant_id","experience_group","condition","task_id","completion_seconds","tests_passed","tests_total","static_analysis_defects","critical_defects","prompt_count","accepted_suggestions","verification_actions"])
        cls.reviews=load_csv(ROOT/"data/sample/reviews.csv",["participant_id","experience_group","seeded_defects_total","defects_detected","defects_correctly_fixed","review_seconds"])
        cls.survey=load_csv(ROOT/"data/sample/survey.csv",["participant_id","experience_group","ai_uses_per_week","primary_ai_use"])

    def test_smoke_primary_result(self):
        output=analyze_trials(self.trials,self.config)
        self.assertEqual(output["paired_participants"],4)
        self.assertEqual(set(output["by_group"]),{"novice","experienced"})
        self.assertIsInstance(output["primary_effect_experienced_minus_novice_percentage_points"],float)

    def test_no_ai_prompts_rejected(self):
        sample=copy.deepcopy(self.trials)
        no_ai=next(r for r in sample if r["condition"]=="no_ai")
        no_ai["prompt_count"]="1"
        with self.assertRaises(DataError):analyze_trials(sample,self.config)

    def test_missing_pair_rejected(self):
        with self.assertRaises(DataError):analyze_trials(self.trials[:-1],self.config)

    def test_pass_count_over_total_rejected(self):
        sample=copy.deepcopy(self.trials)
        sample[0]["tests_passed"]="999"
        with self.assertRaises(DataError):analyze_trials(sample,self.config)

    def test_experience_consistency(self):
        sample=copy.deepcopy(self.reviews)
        sample[0]["experience_group"]="experienced" if sample[0]["experience_group"]=="novice" else "novice"
        with self.assertRaises(DataError):validate_participants(self.trials,self.survey,sample)

    def test_repeated_task_rejected(self):
        sample=copy.deepcopy(self.trials)
        sample[1]["task_id"]=sample[0]["task_id"]
        with self.assertRaises(DataError):analyze_trials(sample,self.config)

    def test_missing_review_participant_rejected(self):
        with self.assertRaises(DataError):validate_participants(self.trials,self.survey,self.reviews[:-1])

    def test_review_and_survey(self):
        self.assertIn("novice",analyze_reviews(self.reviews))
        self.assertIn("experienced",analyze_survey(self.survey))


if __name__=="__main__":unittest.main()
