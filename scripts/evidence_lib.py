"""Shared helpers for CMMC evidence collectors and merge tooling."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime
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


def artifact_path(requirement_id: str, slug: str, ext: str = "json") -> str:
    family, _, rest = requirement_id.partition(".")
    nist = rest.replace("L2-", "")
    return f"evidence/{family.lower()}/{nist}/{slug}.{ext}"


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
