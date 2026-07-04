#!/usr/bin/env python3
"""Report on the discovery (advisor memory) section of a CMMC program data file.

Read-only. Prints phase coverage against the ten interrogation phases in
references/assessor-playbook/scope-discovery-question-bank.md, open question
and unretired assumption counts, stale answers, and id integrity (duplicate
or malformed ids, dangling answer_ref and discovery_refs targets). Exits
nonzero on integrity errors so CI can gate on it.

Usage (from repo root):
    python3 scripts/discovery_report.py templates/program-data.sample.yaml
    python3 scripts/discovery_report.py program.yaml --stale-days 90 --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

PHASE_IDS = [
    "contracts-cui",
    "people",
    "locations",
    "platforms-tenants",
    "endpoints",
    "physical-media",
    "specialized-ot",
    "esps-access-paths",
    "data-flows",
    "backup-dr",
]

ID_PATTERNS = {
    "qa_log": re.compile(r"^QA-\d{4,}$"),
    "assumptions": re.compile(r"^AS-\d{4,}$"),
    "open_questions": re.compile(r"^OQ-\d{4,}$"),
    "decisions": re.compile(r"^DE-\d{4,}$"),
}

DATE_FIELD = {"qa_log": "date", "assumptions": "date", "open_questions": "raised", "decisions": "date"}


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def parse_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def collect_asset_names(program: dict) -> set[str]:
    names: set[str] = set()
    for entries in (program.get("assets") or {}).values():
        for asset in entries or []:
            if isinstance(asset, dict) and asset.get("name"):
                names.add(asset["name"])
    return names


def build_report(program: dict, stale_days: int, today: date) -> dict:
    discovery = program.get("discovery") or {}
    errors: list[str] = []
    warnings: list[str] = []

    phases = discovery.get("phases") or {}
    phase_status = {}
    for pid in PHASE_IDS:
        entry = phases.get(pid) or {}
        phase_status[pid] = entry.get("status", "not-started")
    for pid in phases:
        if pid not in PHASE_IDS:
            errors.append(f"unknown phase id '{pid}' (not in the question bank's phase list)")

    seen_ids: dict[str, str] = {}
    stale: list[dict] = []
    for section, pattern in ID_PATTERNS.items():
        for entry in discovery.get(section) or []:
            if not isinstance(entry, dict):
                errors.append(f"{section}: non-object entry")
                continue
            eid = entry.get("id", "")
            if not eid:
                errors.append(f"{section}: entry missing id")
                continue
            if not pattern.match(str(eid)):
                errors.append(f"{section}: id '{eid}' does not match the {pattern.pattern} pattern")
            if eid in seen_ids:
                errors.append(f"duplicate id '{eid}' in {section} (also in {seen_ids[eid]})")
            seen_ids[eid] = section
            phase = entry.get("phase")
            if phase and phase not in PHASE_IDS:
                errors.append(f"{section} {eid}: unknown phase '{phase}'")
            entry_date = parse_date(entry.get(DATE_FIELD[section]))
            if entry_date is None:
                errors.append(f"{section} {eid}: missing or malformed {DATE_FIELD[section]}")
            elif section == "qa_log" and (today - entry_date).days > stale_days:
                stale.append({"id": eid, "date": entry_date.isoformat(), "question": entry.get("question", "")})

    qa_ids = {e.get("id") for e in discovery.get("qa_log") or [] if isinstance(e, dict)}
    open_count = 0
    for oq in discovery.get("open_questions") or []:
        if not isinstance(oq, dict):
            continue
        status = oq.get("status", "open")
        if status == "open":
            open_count += 1
        ref = oq.get("answer_ref")
        if ref and ref not in qa_ids:
            errors.append(f"open_questions {oq.get('id')}: answer_ref '{ref}' has no qa_log entry")
        if status == "answered" and not ref:
            warnings.append(f"open_questions {oq.get('id')}: answered without an answer_ref")

    unretired = sum(
        1
        for a in discovery.get("assumptions") or []
        if isinstance(a, dict) and a.get("status", "open") == "open"
    )

    asset_names = collect_asset_names(program)
    for asset in [a for entries in (program.get("assets") or {}).values() for a in entries or []]:
        if not isinstance(asset, dict):
            continue
        refs = asset.get("discovery_refs") or []
        if isinstance(refs, str):
            errors.append(f"asset '{asset.get('name')}': discovery_refs must be a list, not a string")
            continue
        for ref in refs:
            if ref not in seen_ids:
                errors.append(f"asset '{asset.get('name')}': discovery_refs '{ref}' has no discovery entry")

    known_targets = asset_names | set(
        (program.get("requirements") or {}).keys()
    ) | {
        n.get("id")
        for n in ((program.get("topology") or {}).get("nodes") or [])
        if isinstance(n, dict) and n.get("id") is not None
    }
    for qa in discovery.get("qa_log") or []:
        if not isinstance(qa, dict):
            continue
        affects = qa.get("affects") or []
        if isinstance(affects, str):
            warnings.append(f"qa_log {qa.get('id')}: affects must be a list, not a string")
            continue
        for target in affects:
            if target not in known_targets:
                warnings.append(
                    f"qa_log {qa.get('id')}: affects '{target}' matches no asset, requirement, or topology node"
                )

    return {
        "valid": not errors,
        "phase_status": phase_status,
        "phases_complete": sum(1 for s in phase_status.values() if s == "complete"),
        "phases_untouched": [p for p, s in phase_status.items() if s == "not-started"],
        "qa_count": len(discovery.get("qa_log") or []),
        "open_questions": open_count,
        "unretired_assumptions": unretired,
        "stale_answers": stale,
        "stale_days": stale_days,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Report on discovery memory in program data")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON")
    ap.add_argument("--stale-days", type=int, default=180, help="age in days before a qa_log answer counts as stale")
    ap.add_argument("--json", action="store_true", help="emit full JSON report on stdout")
    args = ap.parse_args()

    try:
        program = load_program(args.program_data)
    except Exception as exc:
        sys.exit(f"error reading or parsing program data: {exc}")
    if not isinstance(program, dict):
        sys.exit("program data did not parse to an object")
    report = build_report(program, args.stale_days, date.today())

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "OK" if report["valid"] else "FAIL"
        print(f"Discovery report: {status}")
        print(f"  Phases complete: {report['phases_complete']}/{len(PHASE_IDS)}")
        for pid, s in report["phase_status"].items():
            if s != "not-started":
                print(f"    {pid}: {s}")
        if report["phases_untouched"]:
            print(f"  Untouched phases: {', '.join(report['phases_untouched'])}")
        print(f"  Q&A entries: {report['qa_count']}")
        print(f"  Open questions: {report['open_questions']}")
        print(f"  Unretired assumptions: {report['unretired_assumptions']}")
        for entry in report["stale_answers"]:
            print(f"  STALE (> {report['stale_days']}d) {entry['id']} {entry['date']}: {entry['question']}")
        for message in report["errors"]:
            print(f"  ERROR: {message}")
        for message in report["warnings"]:
            print(f"  WARN: {message}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
