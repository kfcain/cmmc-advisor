"""Shared collector runtime: env check, dry-run samples, live stub envelope."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .env_config import credentials_present, profile_env_summary


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dry_run_payload(collector: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "collector": collector["id"],
        "source_system": collector.get("source_system"),
        "evidence_bucket": collector.get("evidence_bucket"),
        "collected_at": utc_now_iso(),
        "mode": "dry_run",
        "note": "Sample artifact for pipeline testing. Replace with live API export before assessment.",
        "sample_records": [{"status": "ok", "record_count": 3}],
    }


def credentials_missing_payload(collector: dict[str, Any], profile_name: str) -> dict[str, Any]:
    summary = profile_env_summary(profile_name)
    return {
        "schema_version": "1.0",
        "collector": collector["id"],
        "source_system": collector.get("source_system"),
        "evidence_bucket": collector.get("evidence_bucket"),
        "collected_at": utc_now_iso(),
        "mode": "credentials_missing",
        "credentials_present": False,
        "env_profile": profile_name,
        "required_env": summary["required_env"],
        "missing_env": summary["missing_env"],
        "note": (
            "Set the listed environment variables (or merge GRC Engineering Club "
            "Finding JSON via scripts/merge_findings.py) before assessment."
        ),
        "records": [],
    }


def live_stub_payload(collector: dict[str, Any], profile_name: str) -> dict[str, Any]:
    summary = profile_env_summary(profile_name)
    return {
        "schema_version": "1.0",
        "collector": collector["id"],
        "source_system": collector.get("source_system"),
        "evidence_bucket": collector.get("evidence_bucket"),
        "collected_at": utc_now_iso(),
        "mode": "live_stub",
        "credentials_present": True,
        "env_profile": profile_name,
        "endpoint": collector.get("endpoint"),
        "note": (
            "Credentials detected. Wire org-specific API fetch in this collector module, "
            "or run the matching GRC Engineering Club inspector and merge findings."
        ),
        "records": [],
        "env_summary": {k: summary[k] for k in ("required_env", "optional_env")},
    }


def run_collector(
    collector: dict[str, Any],
    *,
    profile_name: str,
    dry_run: bool,
) -> dict[str, Any]:
    if dry_run:
        return dry_run_payload(collector)
    ok, _missing = credentials_present(profile_name)
    if not ok:
        return credentials_missing_payload(collector, profile_name)
    return live_stub_payload(collector, profile_name)
