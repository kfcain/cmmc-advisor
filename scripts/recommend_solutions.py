#!/usr/bin/env python3
"""Recommend FedRAMP Marketplace categories and CIS/on-prem fallbacks from program gaps.

Reads open gaps in program-data.yaml and maps control families to capability
categories. Output is JSON or Markdown for ISSM/executive tool selection.

Usage (from repo root):
    python3 scripts/recommend_solutions.py program-data.yaml
    python3 scripts/recommend_solutions.py program-data.yaml -o exports/solution-hints.md --format md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from executive_brief_lib import build_executive_brief, recommend_for_families  # noqa: E402
from generate_dashboard import load_program  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Gap-driven solution recommendations")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--format", choices=["json", "md"], default="json")
    args = ap.parse_args()

    program = load_program(args.program_data)
    dataset = json.loads(AO_DATASET.read_text(encoding="utf-8"))
    brief = build_executive_brief(program, dataset)
    families = sorted(brief.families_with_gaps.keys(), key=lambda f: -brief.families_with_gaps[f])
    hints = recommend_for_families(families)

    payload = {
        "points_at_stake": brief.points_at_stake,
        "gap_count": len(brief.top_gaps),
        "families_with_gaps": brief.families_with_gaps,
        "recommendations": hints,
        "fedramp_selection": "references/grc/solution-selection.md",
        "marketplace_guide": "references/fedramp-marketplace-guide.md",
        "cis_appliances": "references/modern-it/asset-baselines/cis-appliance-baselines.md",
    }

    if args.format == "json":
        text = json.dumps(payload, indent=2) + "\n"
    else:
        lines = [
            "# CMMC gap-driven solution hints",
            "",
            f"SPRS points at stake on open gaps: **{brief.points_at_stake}**",
            "",
            "Verify every FedRAMP listing at marketplace.fedramp.gov before procurement.",
            "See `references/grc/solution-selection.md` for Rev5 Class C/D and 20x rules.",
            "",
        ]
        for h in hints:
            lines.extend(
                [
                    f"## {h['family']} — {h['category']}",
                    "",
                    f"- **Marketplace:** {h['marketplace']}",
                    f"- **On-prem / CIS fallback:** {h['fallback']}",
                    "",
                ]
            )
        text = "\n".join(lines)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
