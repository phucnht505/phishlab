import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analytics" / "scripts"))
from analytics_core import calculate_metrics, normalize_campaign, normalize_quiz_summary, read_csv

class AnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = ROOT / "analytics" / "data"
        cls.results = read_csv(data / "sample_gophish_results.csv")
        cls.events = read_csv(data / "sample_gophish_events.csv")
        cls.quiz = normalize_quiz_summary(read_csv(data / "sample_quiz_summary.csv"))

    def test_normalize_drops_personal_fields_and_event_details(self):
        recipients, events, _ = normalize_campaign(self.results, self.events, "Test", "IT")
        self.assertEqual(len(recipients), 10)
        self.assertNotIn("email", recipients.columns)
        self.assertNotIn("details", events.columns)
        self.assertEqual(recipients.loc[recipients.recipient_code == "1003", "link_clicked"].iloc[0], True)

    def test_campaign_metrics(self):
        recipients, _, _ = normalize_campaign(self.results, self.events, "Test", "IT")
        metrics = calculate_metrics(recipients, self.quiz)
        self.assertEqual(metrics["total_recipients"], 10)
        self.assertEqual(metrics["emails_sent"], 9)
        self.assertEqual(metrics["emails_opened"], 2)
        self.assertEqual(metrics["links_clicked"], 2)
        self.assertEqual(metrics["emails_reported"], 1)
        self.assertEqual(metrics["send_rate"], 90.0)
        self.assertEqual(metrics["click_rate"], 22.22)
        self.assertEqual(metrics["training_completion_rate"], 50.0)
        self.assertEqual(metrics["average_quiz_score"], 80.0)

    def test_missing_quiz_is_not_fabricated(self):
        recipients, _, _ = normalize_campaign(self.results, self.events, "Test", "IT")
        metrics = calculate_metrics(recipients)
        self.assertIsNone(metrics["training_completed"])
        self.assertIsNone(metrics["training_completion_rate"])
        self.assertEqual(metrics["training_started_proxy"], 2)

    def test_invalid_aggregate_rejected(self):
        bad = pd.DataFrame([{"participants_started": 1, "completed_count": 2, "average_score": 80}])
        with self.assertRaises(ValueError):
            normalize_quiz_summary(bad)

if __name__ == "__main__":
    unittest.main()
