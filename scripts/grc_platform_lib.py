"""GRC platform snapshot import: map external controls to CMMC program data."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from evidence_lib import merge_collector_result

REPO_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = REPO_ROOT / "references" / "data" / "800-53-crosswalk.json"
GRC_MANIFEST_PATH = REPO_ROOT / "references" / "data" / "grc-platform-mcp-manifest.json"

CMMC_REQ_RE = re.compile(
    r"^(?P<family>[A-Z]{2})\.L2-(?P<nist>\d+\.\d+\.\d+)$",
    re.IGNORECASE,
)


@dataclass
class ImportResult:
    evidence_links_added: int = 0
    requirements_touched: set[str] = field(default_factory=set)
    unmapped_controls: list[str] = field(default_factory=list)
    snapshot_path: str | None = None
    warnings: list[str] = field(default_factory=list)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_crosswalk(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or CROSSWALK_PATH)


def load_grc_manifest(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or GRC_MANIFEST_PATH)


def normalize_control_id(control: str) -> str:
    c = control.strip().lower().replace("(", ".").replace(")", "")
    return c


def normalize_cmmc_requirement_id(raw: str, crosswalk: dict[str, Any] | None = None) -> str | None:
    text = raw.strip()
    if CMMC_REQ_RE.match(text):
        parts = text.upper().split(".L2-")
        return f"{parts[0]}.L2-{parts[1]}"
    nist_match = re.match(r"^(\d+\.\d+\.\d+)$", text)
    if nist_match and crosswalk:
        nist_id = nist_match.group(1)
        for req in crosswalk.get("requirements") or []:
            if req.get("nist_800_171") == nist_id:
                return req.get("cmmc_id")
    return None


def control_to_cmmc(control_id: str, crosswalk: dict[str, Any]) -> list[str]:
    idx = crosswalk.get("control_index") or {}
    raw = control_id.strip()
    candidates = {raw.upper(), raw.lower(), normalize_control_id(raw)}
    for human, entry in idx.items():
        if human.upper() in candidates or entry.get("oscal_id") in candidates:
            return list(entry.get("cmmc_requirements") or [])
    return []


def resolve_requirement_ids(item: dict[str, Any], crosswalk: dict[str, Any]) -> list[str]:
    ids: set[str] = set()
    if item.get("cmmc_id"):
        norm = normalize_cmmc_requirement_id(str(item["cmmc_id"]), crosswalk)
        if norm:
            ids.add(norm)
    if item.get("requirement_id"):
        norm = normalize_cmmc_requirement_id(str(item["requirement_id"]), crosswalk)
        if norm:
            ids.add(norm)
    if item.get("control_id"):
        ids.update(control_to_cmmc(str(item["control_id"]), crosswalk))
    for ctrl in item.get("controls") or []:
        ids.update(control_to_cmmc(str(ctrl), crosswalk))
    return sorted(ids)


def status_label(raw: str | None) -> str:
    if not raw:
        return "unknown"
    low = raw.strip().lower()
    if low in ("pass", "passed", "healthy", "met", "ok", "green"):
        return "pass"
    if low in ("fail", "failed", "failing", "not_met", "not met", "red"):
        return "fail"
    return low


def merge_grc_evidence(
    program: dict,
    *,
    requirement_id: str,
    source_system: str,
    collector: str,
    name: str,
    link: str,
    collected_at: str,
    external_id: str | None = None,
    monitor_status: str | None = None,
) -> None:
    mapping: dict[str, Any] = {
        "requirement_id": requirement_id,
        "objectives": ["a"],
        "artifact_name": name[:200],
        "collector": collector,
        "source_system": source_system,
        "refresh_bucket": "machine",
    }
    merge_collector_result(program, mapping, link, collected_at=collected_at)

    if external_id or monitor_status:
        reqs = program.setdefault("requirements", {})
        req_entry = reqs.setdefault(requirement_id, {})
        monitoring = req_entry.setdefault("grc_monitoring", [])
        monitoring[:] = [m for m in monitoring if m.get("collector") != collector]
        monitoring.append(
            {
                "source": source_system,
                "collector": collector,
                "external_id": external_id,
                "status": monitor_status,
                "collected": collected_at[:10],
            }
        )


def import_grc_snapshot(
    program: dict,
    snapshot: dict[str, Any],
    crosswalk: dict[str, Any],
    *,
    evidence_root: Path | None = None,
    write_snapshot_artifact: bool = True,
    dry_run: bool = False,
) -> ImportResult:
    result = ImportResult()
    source = (snapshot.get("source_system") or snapshot.get("source") or "grc-platform").lower()
    collected_at = (snapshot.get("collected_at") or date.today().isoformat())[:10]
    collector = f"grc-{source}"

    items: list[dict[str, Any]] = []
    items.extend(snapshot.get("controls") or [])
    items.extend(snapshot.get("requirements") or [])
    items.extend(snapshot.get("tests") or [])

    if not items:
        result.warnings.append("snapshot contains no controls, requirements, or tests")
        return result

    snapshot_rel: str | None = None
    if write_snapshot_artifact and evidence_root is not None and not dry_run:
        imports_dir = evidence_root / "imports"
        imports_dir.mkdir(parents=True, exist_ok=True)
        artifact = imports_dir / f"{source}-{collected_at}.json"
        artifact.write_text(json.dumps(snapshot, indent=2, default=str) + "\n", encoding="utf-8")
        snapshot_rel = f"evidence/imports/{artifact.name}"
        result.snapshot_path = snapshot_rel

    for item in items:
        req_ids = resolve_requirement_ids(item, crosswalk)
        if not req_ids:
            ref = item.get("control_id") or item.get("cmmc_id") or item.get("external_id") or "unknown"
            result.unmapped_controls.append(str(ref))
            continue

        refs = item.get("evidence_refs") or item.get("evidence_urls") or []
        link = refs[0] if refs else (snapshot_rel or f"evidence/imports/{source}-{collected_at}.json")
        name = (
            item.get("name")
            or item.get("test_name")
            or item.get("message")
            or f"{source} {item.get('control_id') or item.get('cmmc_id') or 'monitor'}"
        )
        monitor_status = status_label(item.get("status"))

        for req_id in req_ids:
            result.requirements_touched.add(req_id)
            if dry_run:
                result.evidence_links_added += 1
                continue
            merge_grc_evidence(
                program,
                requirement_id=req_id,
                source_system=source,
                collector=collector,
                name=str(name)[:200],
                link=str(link),
                collected_at=collected_at,
                external_id=item.get("external_id"),
                monitor_status=monitor_status,
            )
            result.evidence_links_added += 1

    if not dry_run:
        integrations = program.setdefault("grc_integrations", {})
        platform_entry = integrations.setdefault(source, {})
        platform_entry["last_sync"] = collected_at
        platform_entry["last_snapshot"] = snapshot_rel
        platform_entry["requirements_linked"] = len(result.requirements_touched)
        platform_entry["unmapped_count"] = len(result.unmapped_controls)
        if snapshot.get("workspace_id"):
            platform_entry["workspace_id"] = snapshot["workspace_id"]

    if result.unmapped_controls:
        result.warnings.append(
            f"{len(result.unmapped_controls)} control(s) did not map to CMMC requirements via 800-53 crosswalk"
        )

    return result
