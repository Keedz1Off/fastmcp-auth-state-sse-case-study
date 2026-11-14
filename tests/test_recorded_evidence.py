"""Offline checks of the evidence shipped with this portfolio entry."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class RecordedEvidenceTests(unittest.TestCase):
    def test_server_denial_holds_in_recorded_cases(self):
        report = read_json("evidence/pr3278-verification.json")
        records = [
            record for variant in report["measurements"].values()
            for record in variant["records"]
        ]
        self.assertEqual(len(records), report["summary"]["measurement_cases"])
        for record in records:
            with self.subTest(variant=record["variant"], case=record["case"]):
                self.assertTrue(record["server_returned_401"])
                self.assertEqual(record["tool_count_after_denial"], 1)
                self.assertTrue(record["independent_client_still_works"])
                self.assertTrue(record["listener_closed"])

    def test_transport_result_differs_between_recorded_revisions(self):
        variants = read_json("evidence/pr3278-verification.json")["measurements"]
        for variant, expected in {"base": False, "release230": False, "head": True}.items():
            records = variants[variant]["records"]
            self.assertEqual(len(records), 3)
            for record in records:
                with self.subTest(variant=variant, case=record["case"]):
                    self.assertIs(record["transport_error_delivered"], expected)
        recovery = next(
            record for record in variants["head"]["records"]
            if record["case"] == "same_principal_reauthorization"
        )
        self.assertTrue(recovery["same_principal_recovery_succeeded"])
