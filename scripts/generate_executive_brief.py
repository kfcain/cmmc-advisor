#!/usr/bin/env python3
"""Generate an internal executive brief from CMMC program data.

Unlike the public trust center, this HTML is for C-level and budget owners:
SPRS exposure, top gaps by point value, POA&M risk, and marketplace/CIS
solution hints. Pair with the operational dashboard for ISSM detail.

Usage (from repo root):
    python3 scripts/generate_executive_brief.py program-data.yaml -o exports/executive-brief.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from executive_brief_lib import brief_to_dict, build_executive_brief  # noqa: E402
from generate_dashboard import embed, load_program  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "templates" / "program-executive-brief.html"
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate CMMC executive brief HTML")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("executive-brief.html"))
    args = ap.parse_args()

    program = load_program(args.program_data)
    dataset = json.loads(AO_DATASET.read_text(encoding="utf-8"))
    brief = build_executive_brief(program, dataset)
    payload = brief_to_dict(brief)

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__BRIEF_JSON__", embed(payload))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
