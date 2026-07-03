"""Helpers for importing Meridian GCP ConMon evidence into CMMC program data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

COLLECTOR_ID = "meridian-gcp-conmon"
SOURCE_SYSTEM = "Meridian GCP ConMon Evidence Engine"


def build_nist171_index(dataset: dict) -> dict[str, str]:
    """Map NIST SP 800-171 requirement numbers (e.g. 3.4.1) to CMMC ids."""
    index: dict[str, str] = {}
    for req in dataset.get("requirements") or []:
        nist = req.get("nist_800_171")
        if nist:
            index[str(nist)] = req["id"]
    return index


def cmmc_l2_ids_from_assertion(assertion: dict) -> list[str]:
    frameworks = assertion.get("frameworks") or {}
    return [str(x) for x in frameworks.get("cmmc_l2") or []]


def map_cmmc_l2_to_requirements(cmmc_l2_ids: list[str], nist_index: dict[str, str]) -> list[str]:
    reqs: set[str] = set()
    for raw in cmmc_l2_ids:
        rid = nist_index.get(raw)
        if rid:
            reqs.add(rid)
    return sorted(reqs)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _chain_breaks(index: dict[str, tuple[str, str | None, str | None]]) -> list[dict[str, Any]]:
    breaks: list[dict[str, Any]] = []
    for run_id, (_sha, prev_run, prev_sha) in index.items():
        if prev_run is None and prev_sha is None:
            continue
        if prev_run not in index:
            breaks.append(
                {
                    "run_id": run_id,
                    "prev_run_id": prev_run,
                    "problem": "referenced previous run is missing (deleted?)",
                    "recorded_prev": prev_sha,
                }
            )
        elif index[prev_run][0] != prev_sha:
            breaks.append(
                {
                    "run_id": run_id,
                    "prev_run_id": prev_run,
                    "problem": "previous manifest hash mismatch (tampered?)",
                    "expected_prev": index[prev_run][0],
                    "recorded_prev": prev_sha,
                }
            )
    return sorted(breaks, key=lambda b: b["run_id"])


def verify_meridian_chain(store_root: Path) -> dict[str, Any]:
    index: dict[str, tuple[str, str | None, str | None]] = {}
    for manifest_path in sorted(store_root.glob("runs/*/*/manifest.json")):
        data = manifest_path.read_bytes()
        manifest = json.loads(data)
        index[manifest.get("run_id", manifest_path.parent.name)] = (
            _sha256_bytes(data),
            manifest.get("prev_run_id"),
            manifest.get("prev_manifest_sha256"),
        )
    breaks = _chain_breaks(index)
    return {"chain_intact": len(breaks) == 0, "runs_indexed": len(index), "breaks": breaks}


def resolve_run(store_root: Path, run_id: str | None = None) -> tuple[str, str, Path, Path]:
    """Return (run_id, date, summary_path, manifest_path)."""
    if run_id:
        matches = list(store_root.glob(f"runs/*/{run_id}/summary.json"))
        if not matches:
            raise FileNotFoundError(f"Meridian run not found: {run_id}")
        summary_path = matches[0]
    else:
        summaries = sorted(store_root.glob("runs/*/*/summary.json"))
        if not summaries:
            raise FileNotFoundError(f"No Meridian runs under {store_root}")
        summary_path = summaries[-1]
    run_dir = summary_path.parent
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Missing manifest for run {run_dir.name}")
    date = run_dir.parent.name
    return run_dir.name, date, summary_path, manifest_path


def load_assertions_from_manifest(store_root: Path, manifest: dict) -> list[tuple[str, dict, str]]:
    """Load (artifact_rel, assertion_dict, artifact_sha256) from a run manifest."""
    out: list[tuple[str, dict, str]] = []
    for rel, meta in (manifest.get("artifacts") or {}).items():
        path = store_root / rel
        if not path.is_file():
            continue
        sha = meta.get("sha256") or _sha256_bytes(path.read_bytes())
        for record in json.loads(path.read_text(encoding="utf-8")):
            out.append((rel, record, sha))
    return out


def rollup_requirement_status(assertions: list[dict]) -> str:
    """Summarize Meridian assertion statuses for one requirement."""
    statuses = {(a.get("status") or "").upper() for a in assertions}
    if "FAIL" in statuses:
        return "FAIL"
    if "ERROR" in statuses:
        return "ERROR"
    if statuses == {"PASS"} or "PASS" in statuses:
        return "PASS"
    return "UNKNOWN"


def link_for_artifact(store_root: Path, artifact_rel: str, repo_root: Path) -> str:
    path = store_root / artifact_rel
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
