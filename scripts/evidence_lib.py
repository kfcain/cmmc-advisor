"""Shared helpers for CMMC evidence collectors and merge tooling."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "references" / "data" / "evidence-collector-manifest.json"
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"

REFRESH_STALE_DAYS = {
    "machine": 90,
    "periodic": 365,
    "document": 365,
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_manifest() -> dict[str, Any]:
    return load_json(MANIFEST_PATH)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_path(
    requirement_id: str,
    slug: str,
    *,
    evidence_bucket: str | None = None,
    ext: str = "json",
) -> str:
    family, _, rest = requirement_id.partition(".")
    nist = rest.replace("L2-", "")
    rel = f"{family.lower()}/{nist}/{slug}.{ext}"
    if evidence_bucket:
        return f"evidence/{evidence_bucket}/{rel}"
    return f"evidence/{rel}"


def days_since(iso_date: str | None) -> int | None:
    if not iso_date:
        return None
    try:
        collected = date.fromisoformat(iso_date[:10])
    except ValueError:
        return None
    return (date.today() - collected).days


def evidence_stale(collected: str | None, refresh_bucket: str) -> bool:
    age = days_since(collected)
    if age is None:
        return True
    limit = REFRESH_STALE_DAYS.get(refresh_bucket, 365)
    return age > limit


def compute_sprs(program: dict, dataset: dict) -> dict[str, Any]:
    entries = program.get("requirements") or {}
    score = 110
    ssp_missing = False
    deductions: list[dict[str, Any]] = []

    for req in dataset["requirements"]:
        rid = req["id"]
        status = (entries.get(rid) or {}).get("conformity") or "not-assessed"
        if status in ("met", "not-applicable"):
            continue
        if rid == "CA.L2-3.12.4" and status == "not-met":
            ssp_missing = True
            continue
        if status == "partially-met" and req.get("sprs_partial_value"):
            deducted = req["sprs_partial_value"]
        elif status in ("not-met", "partially-met", "not-assessed"):
            deducted = req["sprs_value"]
        else:
            deducted = 0
        if deducted:
            score -= deducted
            deductions.append({"requirement_id": rid, "status": status, "points": deducted})

    return {
        "computed_score": max(score, -203),
        "ssp_missing": ssp_missing,
        "deductions": deductions,
    }


def merge_collector_result(
    program: dict,
    mapping: dict[str, Any],
    artifact_rel: str,
    collected_at: str | None = None,
) -> None:
    """Append or replace evidence on mapped objectives."""
    req_id = mapping["requirement_id"]
    objectives = mapping.get("objectives") or ["a"]
    name = mapping.get("artifact_name") or Path(artifact_rel).name
    collected = (collected_at or date.today().isoformat())[:10]
    entry = {
        "name": name,
        "link": artifact_rel,
        "collected": collected,
        "collector": mapping.get("collector"),
        "source_system": mapping.get("source_system"),
        "refresh_bucket": mapping.get("refresh_bucket", "machine"),
    }
    if mapping.get("sha256"):
        entry["sha256"] = mapping["sha256"]

    reqs = program.setdefault("requirements", {})
    req_entry = reqs.setdefault(req_id, {})
    obj_map = req_entry.setdefault("objectives", {})

    for letter in objectives:
        obj_entry = obj_map.setdefault(letter, {})
        evidence = obj_entry.setdefault("evidence", [])
        evidence[:] = [e for e in evidence if e.get("collector") != entry["collector"]]
        evidence.append(entry)


def normalize_control_id(control: str) -> str:
    c = control.strip().lower().replace("(", ".").replace(")", "")
    return c


def sprs_assessment_status(conformity: str) -> str:
    mapping = {
        "met": "MET",
        "not-met": "NOT MET",
        "partially-met": "NOT MET",
        "not-applicable": "NOT APPLICABLE",
        "not-assessed": "NOT MET",
    }
    return mapping.get(conformity or "not-assessed", "NOT MET")


def sprs_points_deducted(conformity: str, req: dict[str, Any]) -> int:
    if conformity in ("met", "not-applicable"):
        return 0
    if req["id"] == "CA.L2-3.12.4" and conformity == "not-met":
        return 0
    if conformity == "partially-met" and req.get("sprs_partial_value") is not None:
        return int(req["sprs_partial_value"])
    if conformity in ("not-met", "partially-met", "not-assessed"):
        return int(req["sprs_value"])
    return 0


def build_sprs_export(program: dict, dataset: dict) -> dict[str, Any]:
    """Build SPRS Basic Assessment export payload from program data."""
    org = program.get("organization") or {}
    assessment = program.get("assessment") or {}
    entries = program.get("requirements") or {}
    summary = compute_sprs(program, dataset)
    requirements_out: list[dict[str, Any]] = []

    for req in dataset["requirements"]:
        rid = req["id"]
        conformity = (entries.get(rid) or {}).get("conformity") or "not-assessed"
        deducted = sprs_points_deducted(conformity, req)
        requirements_out.append(
            {
                "requirement_id": rid,
                "nist_id": req.get("nist_id"),
                "name": req.get("name"),
                "conformity": conformity,
                "sprs_assessment_status": sprs_assessment_status(conformity),
                "sprs_value": req.get("sprs_value"),
                "sprs_partial_value": req.get("sprs_partial_value"),
                "points_deducted": deducted,
            }
        )

    return {
        "schema_version": "1.0",
        "export_type": "sprs_basic_assessment",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "methodology": "DoD Assessment Methodology v1.2.1 (110 practices, -203 floor)",
        "organization": {
            "name": org.get("name"),
            "system_name": org.get("system_name"),
            "cage_codes": org.get("cage_codes") or [],
        },
        "assessment": {
            "level": assessment.get("level"),
            "path": assessment.get("path"),
            "target_date": assessment.get("target_date"),
        },
        "summary_score": summary["computed_score"],
        "maximum_score": 110,
        "minimum_score": -203,
        "ssp_missing": summary["ssp_missing"],
        "deductions": summary["deductions"],
        "requirements": requirements_out,
        "sprs_submission": program.get("sprs_submission"),
        "submission_notes": (
            "Import this scoresheet into your SPRS workflow. SPRS portal entry is manual; "
            "retain this file as the reproducible basis of the submitted score per "
            "references/grc/continuous-monitoring.md."
        ),
    }
