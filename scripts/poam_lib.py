"""POA&M eligibility rules and closeout helpers (32 CFR 170.21)."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from evidence_lib import compute_sprs

L2_BANNED_POAM: frozenset[str] = frozenset(
    {
        "AC.L2-3.1.20",
        "AC.L2-3.1.22",
        "CA.L2-3.12.4",
        "PE.L2-3.10.3",
        "PE.L2-3.10.4",
        "PE.L2-3.10.5",
    }
)

L3_BANNED_POAM: frozenset[str] = frozenset(
    {
        "IR.L3-3.6.1e",
        "IR.L3-3.6.2e",
        "RA.L3-3.11.1e",
        "RA.L3-3.11.4e",
        "RA.L3-3.11.6e",
        "RA.L3-3.11.7e",
        "SI.L3-3.14.3e",
    }
)

FIPS_CARVEOUT_ID = "SC.L2-3.13.11"
SSP_REQUIREMENT_ID = "CA.L2-3.12.4"
CONDITIONAL_SCORE_RATIO = 0.8
L2_REQUIREMENT_COUNT = 110
L2_SCORE_FLOOR = 88
CLOSEOUT_DAYS = 180


def requirement_index(dataset: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {req["id"]: req for req in dataset["requirements"]}


def domain_family(requirement_id: str) -> str:
    return requirement_id.split(".", 1)[0]


def closeout_actor(level: str, path: str) -> str:
    level = str(level or "2")
    path = (path or "").lower()
    if level == "3":
        return "DCMA DIBCAC"
    if path in ("self", "level2-self", "l2-self"):
        return "OSA (Level 2 self-assessment closeout)"
    return "authorized or accredited C3PAO"


def closeout_deadline(conditional_status_date: str | None) -> date | None:
    if not conditional_status_date:
        return None
    try:
        start = date.fromisoformat(conditional_status_date[:10])
    except ValueError:
        return None
    return start + timedelta(days=CLOSEOUT_DAYS)


def days_until_closeout(conditional_status_date: str | None, *, today: date | None = None) -> int | None:
    deadline = closeout_deadline(conditional_status_date)
    if deadline is None:
        return None
    ref = today or date.today()
    return (deadline - ref).days


def poam_eligibility(
    requirement_id: str,
    req_meta: dict[str, Any],
    entry: dict[str, Any],
    *,
    level: str = "2",
) -> dict[str, Any]:
    """Return eligibility ruling for one requirement with an open POA&M or NOT MET status."""
    level = str(level or "2")
    conformity = entry.get("conformity") or "not-assessed"
    poam = entry.get("poam") or {}
    reasons: list[str] = []
    rule_refs: list[str] = []

    if level == "1":
        return {
            "requirement_id": requirement_id,
            "eligible": False,
            "reasons": ["Level 1 does not permit POA&Ms; every practice must be MET at affirmation."],
            "rule_refs": ["32 CFR 170.21 (Level 1)"],
            "conformity": conformity,
        }

    if level == "3":
        if requirement_id in L3_BANNED_POAM:
            reasons.append("Requirement is on the Level 3 never-POA&M list.")
            rule_refs.append("32 CFR 170.21(a)(3)(ii)")
        return {
            "requirement_id": requirement_id,
            "eligible": not reasons,
            "reasons": reasons or ["Eligible under Level 3 POA&M rules if score floor is met."],
            "rule_refs": rule_refs or ["32 CFR 170.21(a)(3)"],
            "conformity": conformity,
        }

    if requirement_id in L2_BANNED_POAM:
        short = req_meta.get("name") or requirement_id
        reasons.append(f"{requirement_id} ({short}) is never POA&M-eligible at Level 2.")
        rule_refs.append("32 CFR 170.21(a)(2)(iii)")

    sprs_value = int(req_meta.get("sprs_value") or 0)
    if sprs_value > 1:
        if requirement_id == FIPS_CARVEOUT_ID:
            if conformity == "partially-met" and req_meta.get("sprs_partial_value") is not None:
                rule_refs.append("32 CFR 170.21(a)(2)(ii) FIPS carve-out")
            elif poam.get("status") in ("open", "in-progress"):
                reasons.append(
                    "SC.L2-3.13.11 may appear on a POA&M only when encryption is employed "
                    "but not FIPS-validated (partially-met / 3-point condition)."
                )
                rule_refs.append("32 CFR 170.21(a)(2)(ii)")
            else:
                reasons.append(
                    "Multi-point requirement; POA&M allowed only for the FIPS-validation carve-out."
                )
                rule_refs.append("32 CFR 170.21(a)(2)(ii)")
        else:
            reasons.append(
                f"Practice carries {sprs_value} SPRS points; only 1-point practices may defer via POA&M."
            )
            rule_refs.append("32 CFR 170.21(a)(2)(ii)")

    if conformity in ("met", "not-applicable", "inherited", "shared"):
        reasons.append(f"Conformity is {conformity}; POA&M is for open gaps, not satisfied practices.")

    eligible = not reasons
    if eligible:
        reasons = ["Eligible 1-point (or FIPS carve-out) item under Level 2 POA&M rules."]
        rule_refs = rule_refs or ["32 CFR 170.21(a)(2)"]

    return {
        "requirement_id": requirement_id,
        "eligible": eligible,
        "reasons": reasons,
        "rule_refs": rule_refs,
        "conformity": conformity,
        "sprs_value": sprs_value,
    }


def collect_poam_items(program: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for req_id, entry in (program.get("requirements") or {}).items():
        poam = entry.get("poam")
        if not poam:
            continue
        status = (poam.get("status") or "open").lower()
        if status == "closed":
            continue
        items.append(
            {
                "requirement_id": req_id,
                "conformity": entry.get("conformity"),
                "poam": poam,
                "objectives": entry.get("objectives") or {},
                "remediation_plan": entry.get("remediation_plan"),
            }
        )
    return items


def validate_poam_program(program: dict[str, Any], dataset: dict[str, Any]) -> dict[str, Any]:
    """Validate POA&M entries and conditional certification prerequisites."""
    assessment = program.get("assessment") or {}
    level = str(assessment.get("level") or "2")
    path = assessment.get("path") or "c3pao"
    index = requirement_index(dataset)
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    rulings: list[dict[str, Any]] = []

    ssp_entry = (program.get("requirements") or {}).get(SSP_REQUIREMENT_ID) or {}
    ssp_conformity = ssp_entry.get("conformity") or "not-assessed"
    if level == "2" and path.lower() != "self" and ssp_conformity != "met":
        issues.append(
            {
                "type": "ssp_gate",
                "requirement_id": SSP_REQUIREMENT_ID,
                "message": (
                    "CA.L2-3.12.4 (SSP) must be MET for Conditional Level 2 (C3PAO); "
                    "the SSP itself cannot be on a POA&M."
                ),
                "rule_ref": "32 CFR 170.21(a)(2)(iii)",
            }
        )

    poam_items = collect_poam_items(program)
    for item in poam_items:
        req_id = item["requirement_id"]
        meta = index.get(req_id)
        if not meta:
            issues.append(
                {
                    "type": "unknown_requirement",
                    "requirement_id": req_id,
                    "message": "Requirement id not found in assessment-objectives dataset.",
                }
            )
            continue

        entry = (program.get("requirements") or {}).get(req_id) or {}
        ruling = poam_eligibility(req_id, meta, entry, level=level)
        rulings.append({**ruling, "poam": item["poam"]})
        if not ruling["eligible"]:
            issues.append(
                {
                    "type": "poam_ineligible",
                    "requirement_id": req_id,
                    "message": "; ".join(ruling["reasons"]),
                    "rule_refs": ruling["rule_refs"],
                }
            )

        poam = item["poam"]
        for field in ("description", "owner", "due"):
            if not poam.get(field):
                warnings.append(
                    {
                        "type": "poam_incomplete",
                        "requirement_id": req_id,
                        "message": f"POA&M missing recommended field: {field}",
                    }
                )

    conditional_date = program.get("conditional_status_date")
    deadline = closeout_deadline(conditional_date)
    remaining = days_until_closeout(conditional_date)
    if poam_items and not conditional_date:
        warnings.append(
            {
                "type": "conditional_date_missing",
                "message": (
                    "Open POA&M items exist but conditional_status_date is unset; "
                    "180-day closeout clocks cannot be computed."
                ),
            }
        )
    elif deadline and remaining is not None:
        for item in poam_items:
            poam_due = item["poam"].get("due")
            if poam_due:
                try:
                    due = date.fromisoformat(poam_due[:10])
                except ValueError:
                    warnings.append(
                        {
                            "type": "invalid_due_date",
                            "requirement_id": item["requirement_id"],
                            "message": f"Invalid POA&M due date: {poam_due}",
                        }
                    )
                    continue
                if due > deadline:
                    issues.append(
                        {
                            "type": "due_after_closeout",
                            "requirement_id": item["requirement_id"],
                            "message": (
                                f"POA&M due {poam_due} is after the 180-day closeout deadline "
                                f"({deadline.isoformat()})."
                            ),
                            "rule_ref": "32 CFR 170.21(b)",
                        }
                    )
        if remaining < 0:
            issues.append(
                {
                    "type": "closeout_expired",
                    "message": (
                        f"Conditional closeout window expired {abs(remaining)} days ago "
                        f"(deadline {deadline.isoformat()})."
                    ),
                    "rule_ref": "32 CFR 170.21(b)",
                }
            )
        elif remaining <= 30:
            warnings.append(
                {
                    "type": "closeout_soon",
                    "message": f"{remaining} days remain until POA&M closeout deadline.",
                    "deadline": deadline.isoformat(),
                }
            )

    sprs = compute_sprs(program, dataset)
    score = sprs["computed_score"]
    ratio = score / L2_REQUIREMENT_COUNT if level == "2" else score / max(len(index), 1)
    if level == "2" and ratio < CONDITIONAL_SCORE_RATIO:
        issues.append(
            {
                "type": "score_floor",
                "message": (
                    f"Computed SPRS score {score} is below the 80% conditional floor "
                    f"({L2_SCORE_FLOOR} of {L2_REQUIREMENT_COUNT})."
                ),
                "computed_score": score,
                "rule_ref": "32 CFR 170.21(a)(2)(i)",
            }
        )

    for req_id, entry in (program.get("requirements") or {}).items():
        if entry.get("poam"):
            continue
        conformity = entry.get("conformity") or "not-assessed"
        if conformity not in ("not-met", "partially-met"):
            continue
        meta = index.get(req_id)
        if not meta:
            continue
        ruling = poam_eligibility(req_id, meta, entry, level=level)
        if ruling["eligible"]:
            warnings.append(
                {
                    "type": "missing_poam",
                    "requirement_id": req_id,
                    "message": (
                        f"{req_id} is NOT MET and POA&M-eligible but has no POA&M entry; "
                        "fix before assessment or add a lawful POA&M if pursuing Conditional status."
                    ),
                }
            )

    return {
        "level": level,
        "path": path,
        "closeout_actor": closeout_actor(level, path),
        "conditional_status_date": conditional_date,
        "closeout_deadline": deadline.isoformat() if deadline else None,
        "days_until_closeout": remaining,
        "computed_sprs_score": score,
        "ssp_missing": sprs.get("ssp_missing"),
        "poam_item_count": len(poam_items),
        "eligible_poam_count": sum(1 for r in rulings if r.get("eligible")),
        "rulings": rulings,
        "issues": issues,
        "warnings": warnings,
        "valid": not issues,
    }
