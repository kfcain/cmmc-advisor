#!/usr/bin/env python3
"""Export SPRS Basic Assessment scoresheet from program data.

Produces JSON (full scoresheet) and optional CSV (requirement status table) for
SPRS portal entry and DIBCAC reproducibility. Compare against sprs_submission in
program data before submitting an updated score.

Usage (from repo root):
    python3 scripts/export_sprs.py templates/program-data.sample.yaml
    python3 scripts/export_sprs.py program.yaml -o exports/sprs-scoresheet.json --csv exports/sprs-scoresheet.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, build_sprs_export, load_json  # noqa: E402


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


def write_csv(export: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "requirement_id",
        "nist_id",
        "name",
        "conformity",
        "sprs_assessment_status",
        "sprs_value",
        "points_deducted",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in export["requirements"]:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def main() -> int:
    ap = argparse.ArgumentParser(description="Export SPRS Basic Assessment scoresheet")
    ap.add_argument("program_data", type=Path, help="program data file (YAML or JSON)")
    ap.add_argument("-o", "--out", type=Path, default=Path("exports/sprs-scoresheet.json"))
    ap.add_argument("--csv", type=Path, default=None, help="optional CSV requirement table")
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data did not parse to an object")
    dataset = load_json(AO_DATASET)
    export = build_sprs_export(program, dataset)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(export, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"wrote {args.out} (summary score {export['summary_score']})")

    if export["ssp_missing"]:
        print("warning: CA.L2-3.12.4 (SSP) is NOT MET; assessment cannot be conducted")

    sub = export.get("sprs_submission") or {}
    if sub.get("score") is not None and sub["score"] != export["summary_score"]:
        delta = export["summary_score"] - sub["score"]
        sign = "+" if delta > 0 else ""
        print(f"sprs_submission delta vs export: {sign}{delta} (last submitted {sub['score']})")

    if args.csv:
        write_csv(export, args.csv)
        print(f"wrote {args.csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
