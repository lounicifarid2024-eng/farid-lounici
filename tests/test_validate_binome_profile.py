import json
import unittest
from pathlib import Path

from src.validate_binome_profile import ProfileValidationError, validate_profile

ROOT = Path(__file__).resolve().parents[1]


def load_profile():
    return json.loads((ROOT / "binome_profile.json").read_text(encoding="utf-8"))


class BinomeProfileTests(unittest.TestCase):
    def test_reference_profile_is_valid(self):
        result = validate_profile(load_profile())
        self.assertEqual(result["status"], "VALID")
        self.assertTrue(result["human_final_authority"])
        self.assertFalse(result["external_certification"])

    def test_rejects_missing_human_final_authority(self):
        data = load_profile()
        data["binome_intelligent"]["human_decision_final"] = False
        with self.assertRaises(ProfileValidationError):
            validate_profile(data)

    def test_rejects_disabled_deny_by_default(self):
        data = load_profile()
        data["binome_intelligent"]["deny_by_default"] = False
        with self.assertRaises(ProfileValidationError):
            validate_profile(data)

    def test_rejects_missing_sensitive_gate(self):
        data = load_profile()
        data["binome_intelligent"]["required_human_gates"].remove("payment")
        with self.assertRaises(ProfileValidationError):
            validate_profile(data)

    def test_rejects_external_certification_claim(self):
        data = load_profile()
        data["profile"]["external_certification"] = True
        with self.assertRaises(ProfileValidationError):
            validate_profile(data)


if __name__ == "__main__":
    unittest.main()
