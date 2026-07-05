"""Shared 800-53 to CMMC requirement mapping helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from evidence_lib import load_json, normalize_control_id

REPO_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = REPO_ROOT / "references" / "data" / "800-53-crosswalk.json"


def load_crosswalk(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or CROSSWALK_PATH)


def control_to_cmmc(control_id: str, crosswalk: dict[str, Any]) -> list[str]:
    idx = crosswalk.get("control_index") or {}
    raw = control_id.strip()
    if not raw or raw.upper() == "UNMAPPED":
        return []
    candidates = {raw.upper(), raw.lower()}
    candidates.add(normalize_control_id(raw))
    for human, entry in idx.items():
        if human.upper() in candidates or entry.get("oscal_id") in candidates:
            return entry.get("cmmc_requirements") or []
    return []


def controls_to_cmmc(control_ids: list[str], crosswalk: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for control in control_ids:
        for req_id in control_to_cmmc(str(control), crosswalk):
            if req_id not in seen:
                seen.add(req_id)
                ordered.append(req_id)
    return ordered
