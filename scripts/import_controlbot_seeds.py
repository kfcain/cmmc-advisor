#!/usr/bin/env python3
"""Import ControlBot POA&M seeds and evidence facts into CMMC program data.

Reads ControlBot artifacts (external repo: github.com/ethanolivertroy/controlbot):
  - poam-seeds.json (schema controlbot.poam-seeds.v1)
  - evidence-facts.json (schema controlbot.evidence-facts.v1, optional)

Maps NIST SP 800-53 controls through references/data/800-53-crosswalk.json,
writes per-requirement poam blocks and evidence links. Does not set conformity
unless --write-conformity is passed. ISSM review and validate_poam.py apply.

Usage (from repo root):
    python3 scripts/import_controlbot_seeds.py poam-seeds.json program-data.yaml
    python3 scripts/import_controlbot_seeds.py poam-seeds.json program.yaml --evidence evidence-facts.json
    python3 scripts/import_controlbot_seeds.py poam-seeds.json program.yaml --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crosswalk_lib import controls_to_cmmc, load_crosswalk  # noqa: E402
from evidence_lib import merge_collector_result  # noqa: E402
from merge_findings import load_program, save_program  # noqa: E402

SEVERITY_PRIORITY = {
    "CRITICAL": "Critical",
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low",
}

STATUS_MAP = {
    "open": "open",
    "closed": "closed",
    "in-progress": "in-progress",
    "in progress": "in-progress",
}


def _seed_marker(seed_id: str) -> str:
    return f"[controlbot:{seed_id}]"


def _existing_seed_ids(program: dict) -> set[str]:
    seen: set[str] = set()
    for entry in (program.get("requirements") or {}).values():
        poam = entry.get("poam") or {}
        for text in (poam.get("description") or "", entry.get("remediation_plan") or ""):
            start = text.find("[controlbot:")
            if start >= 0:
                end = text.find("]", start)
                if end > start:
                    seen.add(text[start + 12 : end])
    return seen


def _ensure_requirement(program: dict, req_id: str) -> dict:
    return program.setdefault("requirements", {}).setdefault(req_id, {})


def _poam_status(raw: str) -> str:
    return STATUS_MAP.get(raw.strip().lower().replace("_", "-"), "open")


def _apply_poam_seed(
    program: dict,
    req_id: str,
    seed: dict[str, Any],
    *,
    seen: set[str],
    existing_ids: set[str],
    generated_at: str,
    write_conformity: bool,
    force_overwrite: bool,
) -> bool:
    seed_id = str(seed.get("id") or "")
    dedup_key = f"{req_id}:{seed_id}"
    if dedup_key in seen or seed_id in existing_ids:
        return False

    entry = _ensure_requirement(program, req_id)
    existing = entry.get("poam") or {}
    if existing and not force_overwrite:
        desc = existing.get("description") or ""
        if _seed_marker(seed_id) not in desc and "[controlbot:" not in desc:
            return False

    severity = str(seed.get("severity") or "MEDIUM").upper()
    weakness = str(seed.get("weakness") or "ControlBot finding")
    remediation = str(seed.get("recommended_remediation") or "")
    marker = _seed_marker(seed_id)

    entry["poam"] = {
        "priority": SEVERITY_PRIORITY.get(severity, "Medium"),
        "description": f"{weakness} {marker}".strip()[:500],
        "opened": generated_at[:10],
        "due": str(seed.get("due_date") or "")[:10] or None,
        "owner": str(seed.get("owner") or "TBD"),
        "status": _poam_status(str(seed.get("status", "Open"))),
        "actions": [remediation[:500]] if remediation else [],
    }
    if entry["poam"].get("due") is None:
        entry["poam"].pop("due", None)

    plan_parts = [remediation, f"Source: ControlBot {seed.get('source', 'checkov')}"]
    if seed.get("merge_blocking"):
        plan_parts.append("Merge-blocking in IaC pipeline.")
    entry["remediation_plan"] = " ".join(p for p in plan_parts if p).strip()

    if write_conformity:
        conf = entry.get("conformity")
        if conf not in ("met", "not-applicable", "inherited"):
            entry["conformity"] = "not-met" if seed.get("merge_blocking") else "partially-met"

    seen.add(dedup_key)
    existing_ids.add(seed_id)
    return True


def _fact_collector_id(fact: dict[str, Any]) -> str:
    raw = fact.get("id") or f"{fact.get('path')}:{fact.get('line')}:{fact.get('subject')}"
    digest = hashlib.sha256(str(raw).encode()).hexdigest()[:12]
    return f"controlbot-{fact.get('source', 'evidence')}-{digest}"


def _merge_evidence_fact(
    program: dict,
    fact: dict[str, Any],
    crosswalk: dict[str, Any],
    collected_at: str,
) -> int:
    disposition = str(fact.get("disposition") or "observed")
    if disposition not in ("observed", "warning"):
        return 0

    controls = fact.get("controls") or []
    cmmc_ids = controls_to_cmmc([str(c) for c in controls], crosswalk)
    if not cmmc_ids:
        return 0

    path = str(fact.get("path") or "unknown")
    line = fact.get("line")
    link = f"{path}:{line}" if line else path
    name = str(fact.get("summary") or fact.get("detail") or fact.get("subject") or "ControlBot evidence")[:200]
    merged = 0
    for req_id in cmmc_ids:
        merge_collector_result(
            program,
            {
                "requirement_id": req_id,
                "objectives": ["a"],
                "artifact_name": name,
                "collector": _fact_collector_id(fact),
                "source_system": "ControlBot",
                "refresh_bucket": "machine",
            },
            link,
            collected_at=collected_at,
        )
        merged += 1
    return merged


def _seed_inline_facts(seed: dict[str, Any]) -> list[dict[str, Any]]:
    controls = seed.get("controls") or []
    if isinstance(seed.get("control"), str) and not controls:
        controls = [c.strip() for c in seed["control"].split(",") if c.strip()]
    facts: list[dict[str, Any]] = []
    for ev in seed.get("evidence") or []:
        facts.append(
            {
                **ev,
                "controls": controls,
                "source": seed.get("source", "checkov"),
                "disposition": "observed",
                "id": f"{seed.get('id')}-ev-{ev.get('path')}-{ev.get('line')}",
            }
        )
    return facts


def import_controlbot(
    program: dict,
    seeds_doc: dict[str, Any],
    crosswalk: dict[str, Any],
    evidence_doc: dict[str, Any] | None = None,
    *,
    write_conformity: bool = False,
    force_overwrite: bool = False,
) -> dict[str, Any]:
    if seeds_doc.get("schema") != "controlbot.poam-seeds.v1":
        raise ValueError(f"unexpected poam-seeds schema: {seeds_doc.get('schema')}")

    seen: set[str] = set()
    existing_ids = _existing_seed_ids(program)
    poam_applied = 0
    unmapped_seeds: list[str] = []
    requirements_touched: set[str] = set()
    generated_at = str(seeds_doc.get("generated_at") or date.today().isoformat())[:10]

    for seed in seeds_doc.get("seeds") or []:
        controls = seed.get("controls") or []
        if isinstance(seed.get("control"), str) and not controls:
            controls = [c.strip() for c in seed["control"].split(",") if c.strip()]
        cmmc_ids = controls_to_cmmc([str(c) for c in controls], crosswalk)
        if not cmmc_ids:
            unmapped_seeds.append(str(seed.get("id") or seed.get("weakness")))
            continue
        for req_id in cmmc_ids:
            if _apply_poam_seed(
                program,
                req_id,
                seed,
                seen=seen,
                existing_ids=existing_ids,
                generated_at=generated_at,
                write_conformity=write_conformity,
                force_overwrite=force_overwrite,
            ):
                poam_applied += 1
                requirements_touched.add(req_id)

    evidence_links = 0
    inline_facts: list[dict[str, Any]] = []
    for seed in seeds_doc.get("seeds") or []:
        inline_facts.extend(_seed_inline_facts(seed))

    facts_to_merge: list[dict[str, Any]] = list(inline_facts)
    if evidence_doc:
        if evidence_doc.get("schema") != "controlbot.evidence-facts.v1":
            raise ValueError(f"unexpected evidence-facts schema: {evidence_doc.get('schema')}")
        facts_to_merge.extend(evidence_doc.get("facts") or [])

    collected_at = str(
        (evidence_doc or {}).get("generated_at") or seeds_doc.get("generated_at") or date.today().isoformat()
    )[:10]
    for fact in facts_to_merge:
        evidence_links += _merge_evidence_fact(program, fact, crosswalk, collected_at)

    summary = seeds_doc.get("summary") or {}
    program["controlbot_import"] = {
        "last_imported": date.today().isoformat(),
        "baseline": seeds_doc.get("baseline"),
        "seeds_total": summary.get("total"),
        "poam_applied": poam_applied,
        "requirements_touched": len(requirements_touched),
        "evidence_links_added": evidence_links,
        "unmapped_seed_count": len(unmapped_seeds),
        "source_digest": hashlib.sha256(
            json.dumps(seeds_doc, sort_keys=True, default=str).encode()
        ).hexdigest()[:16],
    }

    return {
        "poam_applied": poam_applied,
        "requirements_touched": sorted(requirements_touched),
        "evidence_links_added": evidence_links,
        "unmapped_seeds": unmapped_seeds,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"could not parse {path}: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Import ControlBot POA&M seeds into program data")
    ap.add_argument("poam_seeds", type=Path, help="ControlBot poam-seeds.json")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON to update")
    ap.add_argument("--evidence", type=Path, help="optional ControlBot evidence-facts.json")
    ap.add_argument("--dry-run", action="store_true", help="report mapping only; do not write program data")
    ap.add_argument(
        "--write-conformity",
        action="store_true",
        help="opt-in: set not-met/partially-met from merge-blocking seeds (default: POA&M only)",
    )
    ap.add_argument(
        "--force-poam-overwrite",
        action="store_true",
        help="replace existing POA&M blocks even when not ControlBot-sourced",
    )
    args = ap.parse_args()

    seeds_doc = load_json(args.poam_seeds)
    evidence_doc = load_json(args.evidence) if args.evidence else None
    program = load_program(args.program_data)
    crosswalk = load_crosswalk()

    try:
        result = import_controlbot(
            program,
            seeds_doc,
            crosswalk,
            evidence_doc,
            write_conformity=args.write_conformity,
            force_overwrite=args.force_poam_overwrite,
        )
    except ValueError as exc:
        sys.exit(str(exc))

    print(f"baseline: {seeds_doc.get('baseline', 'unknown')}")
    print(f"poam entries applied: {result['poam_applied']}")
    print(f"requirements touched: {len(result['requirements_touched'])}")
    print(f"evidence links added: {result['evidence_links_added']}")
    if result["unmapped_seeds"]:
        print(f"unmapped seeds: {', '.join(result['unmapped_seeds'][:10])}")
        if len(result["unmapped_seeds"]) > 10:
            print(f"  ... and {len(result['unmapped_seeds']) - 10} more")

    if args.dry_run:
        print("dry-run: program data not written")
        return 0

    save_program(args.program_data, program)
    print(f"updated {args.program_data}")
    print("run: python3 scripts/validate_poam.py", args.program_data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
