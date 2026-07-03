#!/usr/bin/env python3
"""Generate the single-file CMMC program dashboard.

Injects a program data file (templates/program-data.schema.json shape) and
the assessment-objective dataset into templates/program-dashboard.html,
producing a self-contained HTML file: family progress, per-objective
statuses and narratives, live SPRS score (DoD Assessment Methodology,
partial credit, -203 floor, SSP special rule), POA&M table with 180-day
clocks, gap remediation view, and inherited-controls view with CRM
references.

Usage (from repo root):
    python3 scripts/generate_dashboard.py path/to/program-data.yaml -o dashboard.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "templates" / "program-dashboard.html"
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def embed(value: dict) -> str:
    # </script> can never appear inside an inline JSON script element
    return json.dumps(value, separators=(",", ":")).replace("</", "<\\/")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the CMMC program dashboard")
    ap.add_argument("program_data", type=Path, help="program data file (YAML or JSON)")
    ap.add_argument("-o", "--out", type=Path, default=Path("cmmc-dashboard.html"))
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data must parse to a mapping (YAML or JSON object)")
    dataset = json.loads(AO_DATASET.read_text(encoding="utf-8"))
    known = {r["id"] for r in dataset["requirements"]}
    unknown = [k for k in (program.get("requirements") or {}) if k not in known]
    if unknown:
        sys.exit(f"unknown requirement ids in program data: {unknown}")

    if program.get("topology"):
        from generate_diagrams import build_svg
        program["_diagrams"] = {
            "network": build_svg(program, "network"),
            "cui_flow": build_svg(program, "cui-flow"),
        }

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__PROGRAM_DATA__", embed(program))
    html = html.replace("__AO_DATASET__", embed(dataset))
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes, self-contained)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
