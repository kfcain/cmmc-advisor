#!/usr/bin/env python3
"""Merge GRC Engineering Club Finding JSON into CMMC program data evidence arrays.

Reads finding files shaped like GRCEngClub/claude-grc-engineering
schemas/finding.schema.json (evaluations with control_id and evidence_refs),
maps controls to CMMC requirements via references/data/800-53-crosswalk.json
control_index, and writes evidence entries on affected objectives.

Usage (from repo root):
    python3 scripts/merge_findings.py finding.json program-data.yaml
    python3 scripts/merge_findings.py ~/.cache/claude-grc/findings/github-inspector/*.json program.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import load_json, merge_collector_result, normalize_control_id  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = REPO_ROOT / "references" / "data" / "800-53-crosswalk.json"


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def save_program(path: Path, program: dict) -> None:
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        path.write_text(yaml.safe_dump(program, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(program, indent=2) + "\n", encoding="utf-8")


def control_to_cmmc(control_id: str, crosswalk: dict[str, Any]) -> list[str]:
    idx = crosswalk.get("control_index") or {}
    raw = control_id.strip()
    candidates = {raw.upper(), raw.lower()}
    candidates.add(normalize_control_id(raw))
    for human, entry in idx.items():
        if human.upper() in candidates or entry.get("oscal_id") in candidates:
            return entry.get("cmmc_requirements") or []
    return []


def merge_finding(program: dict, finding: dict[str, Any], crosswalk: dict[str, Any]) -> int:
    source = finding.get("source") or "grc-inspector"
    collected_at = (finding.get("collected_at") or date.today().isoformat())[:10]
    merged = 0

    for evaluation in finding.get("evaluations") or []:
        controls: list[str] = []
        if evaluation.get("control_id"):
            controls = [evaluation["control_id"]]
        controls.extend(evaluation.get("controls") or [])

        cmmc_ids: set[str] = set()
        for control in controls:
            cmmc_ids.update(control_to_cmmc(str(control), crosswalk))

        refs = evaluation.get("evidence_refs") or []
        link = refs[0] if refs else f"evidence/imports/{source}-{finding.get('run_id', 'run')}.json"
        name = evaluation.get("message") or f"{source} evaluation {evaluation.get('control_id', '')}"

        for req_id in sorted(cmmc_ids):
            merge_collector_result(
                program,
                {
                    "requirement_id": req_id,
                    "objectives": ["a"],
                    "artifact_name": name[:200],
                    "collector": source,
                    "source_system": source,
                    "refresh_bucket": "machine",
                },
                link,
                collected_at=collected_at,
            )
            merged += 1

    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge GRC inspector findings into program data")
    ap.add_argument("findings", type=Path, nargs="+", help="finding JSON file(s)")
    ap.add_argument("program_data", type=Path, help="program data file to update")
    args = ap.parse_args()

    program = load_program(args.program_data)
    crosswalk = load_json(CROSSWALK)
    total = 0

    for path in args.findings:
        finding = load_json(path)
        count = merge_finding(program, finding, crosswalk)
        total += count
        print(f"merged {count} requirement links from {path}")

    save_program(args.program_data, program)
    print(f"updated {args.program_data} ({total} total requirement evidence links)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
