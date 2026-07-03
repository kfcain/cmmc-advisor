#!/usr/bin/env python3
"""Import a normalized GRC platform snapshot into CMMC program data.

Use after querying Vanta, Drata, Secureframe, Hyperproof, or another GRC MCP
server. The agent (or you) saves platform output as JSON matching
templates/grc-snapshot.sample.json, then this script maps controls through
references/data/800-53-crosswalk.json and writes evidence links plus
grc_monitoring metadata. It does not auto-set conformity (human/ISSM review).

Usage (from repo root):
    python3 scripts/import_grc_snapshot.py snapshot.json program-data.yaml
    python3 scripts/import_grc_snapshot.py snapshot.json program-data.yaml --dry-run
    python3 scripts/import_grc_snapshot.py snapshot.json program-data.yaml --evidence-root ./evidence
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from grc_platform_lib import import_grc_snapshot, load_crosswalk, load_json  # noqa: E402
from merge_findings import load_program, save_program  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Import GRC platform snapshot into program data")
    ap.add_argument("snapshot", type=Path, help="normalized GRC snapshot JSON")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON to update")
    ap.add_argument(
        "--evidence-root",
        type=Path,
        default=Path("evidence"),
        help="evidence root for snapshot artifact (default: ./evidence)",
    )
    ap.add_argument("--dry-run", action="store_true", help="report mapping only; do not write program data")
    args = ap.parse_args()

    snapshot = load_json(args.snapshot)
    program = load_program(args.program_data)
    crosswalk = load_crosswalk()

    result = import_grc_snapshot(
        program,
        snapshot,
        crosswalk,
        evidence_root=args.evidence_root,
        write_snapshot_artifact=not args.dry_run,
        dry_run=args.dry_run,
    )

    print(f"source: {(snapshot.get('source_system') or snapshot.get('source') or 'unknown')}")
    print(f"evidence links: {result.evidence_links_added}")
    print(f"requirements touched: {len(result.requirements_touched)}")
    if result.snapshot_path:
        print(f"snapshot artifact: {result.snapshot_path}")
    if result.unmapped_controls:
        print(f"unmapped: {', '.join(result.unmapped_controls[:20])}")
        if len(result.unmapped_controls) > 20:
            print(f"  ... and {len(result.unmapped_controls) - 20} more")
    for warning in result.warnings:
        print(f"warning: {warning}")

    if args.dry_run:
        print("dry-run: program data not written")
        return 0

    save_program(args.program_data, program)
    print(f"updated {args.program_data}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
