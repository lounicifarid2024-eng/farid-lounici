from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "profile",
    "binome_intelligent",
    "evidence",
    "claims_policy",
}

REQUIRED_HUMAN_GATES = {
    "publication",
    "payment",
    "contract_or_signature",
    "deletion",
    "confidential_data_release",
    "irreversible_change",
}

FORBIDDEN_CERTIFICATION_WORDING = {
    "officially certified",
    "scientifically proven",
    "guaranteed compliance",
    "guaranteed performance",
    "100% autonomous",
}


class ProfileValidationError(ValueError):
    """Raised when the Binôme Intelligent profile violates its governance contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProfileValidationError(message)


def validate_profile(data: dict[str, Any]) -> dict[str, Any]:
    """Validate the public Binôme Intelligent profile manifest.

    This validator checks the declared governance contract. It does not certify
    the person, prove professional competence, or verify external credentials.
    """
    _require(REQUIRED_TOP_LEVEL_KEYS.issubset(data), "Missing required top-level fields")

    profile = data["profile"]
    governance = data["binome_intelligent"]
    evidence = data["evidence"]
    claims = data["claims_policy"]

    _require(profile.get("external_certification") is False,
             "Profile must not claim external certification without verifiable evidence")
    _require(profile.get("validation_scope") == "self-documented technical profile",
             "Validation scope must remain explicitly self-documented")

    _require(governance.get("human_decision_final") is True,
             "Human final decision authority is mandatory")
    _require(governance.get("deny_by_default") is True,
             "Deny-by-default governance is mandatory")

    declared_gates = set(governance.get("required_human_gates", []))
    _require(REQUIRED_HUMAN_GATES.issubset(declared_gates),
             "All sensitive actions must require human validation")

    applied = evidence.get("applied_capability_index")
    low = evidence.get("market_industrial_evidence_index_min")
    high = evidence.get("market_industrial_evidence_index_max")
    _require(isinstance(applied, int) and 0 <= applied <= 100,
             "Applied capability index must be an integer from 0 to 100")
    _require(isinstance(low, int) and isinstance(high, int) and 0 <= low <= high <= 100,
             "Market evidence range must be valid")

    notice = str(evidence.get("index_notice", "")).lower()
    for phrase in ("not a certification", "not a", "scientific"):
        _require(phrase in notice, "Index disclaimer is incomplete")

    forbidden = {str(x).lower() for x in claims.get("forbidden_unverified_claims", [])}
    _require(FORBIDDEN_CERTIFICATION_WORDING.issubset(forbidden),
             "Claims policy must block unverified superiority/certification claims")

    return {
        "status": "VALID",
        "scope": profile["validation_scope"],
        "human_final_authority": True,
        "external_certification": False,
        "message": "Binôme Intelligent profile contract is internally consistent and security-gated.",
    }


def load_and_validate(path: str | Path = "binome_profile.json") -> dict[str, Any]:
    profile_path = Path(path)
    with profile_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return validate_profile(data)


if __name__ == "__main__":
    result = load_and_validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
