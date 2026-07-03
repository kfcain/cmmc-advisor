#!/usr/bin/env python3
"""Validate POA&M eligibility and closeout readiness in a CMMC program data file.

Checks 32 CFR 170.21 rules: banned practices, 1-point limit, FIPS carve-out,
80% score floor, SSP gate, and 180-day closeout dates.

Usage (from repo root):
    python3 scripts/validate_poam.py templates/program-data.sample.yaml
    python3 scripts/validate_poam.py program.yaml --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, load_json  # noqa: E402
from poam_lib import validate_poam_program  # noqa: E402


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate POA&M eligibility in program data")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON")
    ap.add_argument("--json", action="store_true", help="emit full JSON report on stdout")
    args = ap.parse_args()

    program = load_program(args.program_data)
    dataset = load_json(AO_DATASET)
    report = validate_poam_program(program, dataset)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "PASS" if report["valid"] else "FAIL"
        print(f"POA&M validation: {status}")
        print(f"  Level {report['level']} path={report['path']} closeout by {report['closeout_actor']}")
        print(f"  Open POA&M items: {report['poam_item_count']} ({report['eligible_poam_count']} eligible)")
        print(f"  Computed SPRS: {report['computed_sprs_score']}")
        if report.get("closeout_deadline"):
            print(f"  Closeout deadline: {report['closeout_deadline']} ({report['days_until_closeout']} days left)")
        for issue in report["issues"]:
            rid = issue.get("requirement_id", "")
            prefix = f"  ERROR [{rid}]" if rid else "  ERROR"
            print(f"{prefix}: {issue['message']}")
        for warning in report["warnings"]:
            rid = warning.get("requirement_id", "")
            prefix = f"  WARN [{rid}]" if rid else "  WARN"
            print(f"{prefix}: {warning['message']}")

    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
