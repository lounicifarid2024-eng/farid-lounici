import json
from pathlib import Path

import pytest

from src.validate_binome_profile import ProfileValidationError, validate_profile

ROOT = Path(__file__).resolve().parents[1]


def load_profile():
    return json.loads((ROOT / "binome_profile.json").read_text(encoding="utf-8"))


def test_reference_profile_is_valid():
    result = validate_profile(load_profile())
    assert result["status"] == "VALID"
    assert result["human_final_authority"] is True
    assert result["external_certification"] is False


def test_rejects_missing_human_final_authority():
    data = load_profile()
    data["binome_intelligent"]["human_decision_final"] = False
    with pytest.raises(ProfileValidationError):
        validate_profile(data)


def test_rejects_disabled_deny_by_default():
    data = load_profile()
    data["binome_intelligent"]["deny_by_default"] = False
    with pytest.raises(ProfileValidationError):
        validate_profile(data)


def test_rejects_missing_sensitive_gate():
    data = load_profile()
    data["binome_intelligent"]["required_human_gates"].remove("payment")
    with pytest.raises(ProfileValidationError):
        validate_profile(data)


def test_rejects_external_certification_claim():
    data = load_profile()
    data["profile"]["external_certification"] = True
    with pytest.raises(ProfileValidationError):
        validate_profile(data)
