#!/usr/bin/env python3
"""Validate asset baseline profiles and checklist completion in program data.

Usage (from repo root):
    python3 scripts/validate_asset_baselines.py templates/program-data.sample.yaml
    python3 scripts/validate_asset_baselines.py program.yaml --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from asset_baseline_lib import validate_asset_baselines  # noqa: E402


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            sys.exit(f"could not parse {path}: {exc}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"could not parse {path}: {exc}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate asset baselines in program data")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    program = load_program(args.program_data)
    report = validate_asset_baselines(program)

    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        status = "PASS" if report["valid"] else "FAIL"
        print(f"Asset baseline validation: {status} ({report['assets_checked']} profiled assets)")
        for issue in report["issues"]:
            print(f"  ERROR [{issue.get('asset', '')}]: {issue['message']}")
        for warning in report["warnings"]:
            print(f"  WARN [{warning.get('asset', '')}]: {warning['message']}")

    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
