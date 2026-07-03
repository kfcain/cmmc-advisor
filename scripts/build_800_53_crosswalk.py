#!/usr/bin/env python3
"""Build the CMMC-to-800-53 crosswalk dataset from primary NIST sources.

Merges NIST SP 800-171 Rev 2 Appendix D mappings (parsed from the
authoritative tables in references/fedramp-gap.md, which reproduce
Appendix D) with CMMC requirement identifiers from
references/data/assessment-objectives.json and FedRAMP Moderate baseline
membership from the NIST OSCAL content repository.

Usage (from repo root):
    python3 scripts/build_800_53_crosswalk.py
    python3 scripts/build_800_53_crosswalk.py -o references/data/800-53-crosswalk.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"
FEDRAMP_GAP = REPO_ROOT / "references" / "fedramp-gap.md"
DEFAULT_OUTPUT = REPO_ROOT / "references" / "data" / "800-53-crosswalk.json"
MODERATE_BASELINE_URL = (
    "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
    "nist.gov/SP800-53/rev5/json/"
    "NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog-min.json"
)

TABLE_ROW = re.compile(
    r"^\|\s*([A-Z]{2}\.L2-3\.\d+\.\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$"
)

REV5_NOTES: dict[str, str] = {
    "IA-2(8)": "Rev 5 Moderate includes replay resistance for non-privileged accounts; Rev 4 Moderate did not (Appendix D footnote 33).",
    "IA-2(9)": "Rev 5 Moderate includes replay resistance for non-privileged accounts; Rev 4 Moderate did not (Appendix D footnote 33).",
    "CM-7(5)": "Rev 4 restricted allowlisting to High baseline (Appendix D footnote 32); confirm CSP Rev 5 authorization reflects current baseline treatment.",
}

ISO_27001_NOTES = (
    "NIST SP 800-171 Rev 2 Appendix D maps each requirement to ISO/IEC 27001 "
    "controls where a direct mapping exists; some cells read 'No direct mapping'. "
    "For ISO/IEC 27001:2022 alignment at the 800-53 layer, use the NIST OLIR "
    "crosswalk from SP 800-53 Rev 5 (see SOURCES.md). Mappings are indicative, "
    "not one-to-one equivalencies."
)


def _fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "cmmc-advisor-crosswalk-builder"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to fetch {url}: {exc}") from exc


def _parse_controls(cell: str) -> list[str]:
    controls: list[str] = []
    for part in cell.split(","):
        token = part.strip()
        if not token:
            continue
        controls.append(token.upper().replace(" ", ""))
    return controls


def _to_oscal_id(control_id: str) -> str:
    base, _, enh = control_id.partition("(")
    base = base.lower()
    if enh:
        enh = enh.rstrip(")").lower()
        return f"{base}.{enh}"
    return base


def _parse_fedramp_gap_tables(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    start = text.find("### The 110-practice crosswalk")
    end = text.find("### Where the mapping is tightest")
    if start == -1 or end == -1:
        raise SystemExit(f"Could not locate crosswalk tables in {path}")

    rows: list[dict[str, str]] = []
    for line in text[start:end].splitlines():
        match = TABLE_ROW.match(line.strip())
        if not match:
            continue
        cmmc_id, controls_cell, notes = match.groups()
        rows.append(
            {
                "cmmc_id": cmmc_id.strip(),
                "controls_cell": controls_cell.strip(),
                "notes": notes.strip(),
            }
        )
    return rows


def _moderate_baseline_controls(catalog: dict[str, Any]) -> set[str]:
    controls: set[str] = set()
    for group in catalog["catalog"]["groups"]:
        for control in group.get("controls", []):
            controls.add(control["id"])
            for enhancement in control.get("controls", []):
                controls.add(enhancement["id"])
    return controls


def build_crosswalk(fetch_baseline: bool = True) -> dict[str, Any]:
    ao = json.loads(AO_DATASET.read_text(encoding="utf-8"))
    ao_by_id = {req["id"]: req for req in ao["requirements"]}

    table_rows = _parse_fedramp_gap_tables(FEDRAMP_GAP)
    if len(table_rows) != 110:
        raise SystemExit(f"Expected 110 crosswalk rows, found {len(table_rows)}")

    moderate_oscal: set[str] = set()
    if fetch_baseline:
        baseline = _fetch_json(MODERATE_BASELINE_URL)
        moderate_oscal = _moderate_baseline_controls(baseline)

    requirements: list[dict[str, Any]] = []
    control_index: dict[str, dict[str, Any]] = {}

    for row in table_rows:
        cmmc_id = row["cmmc_id"]
        if cmmc_id not in ao_by_id:
            raise SystemExit(f"Crosswalk id {cmmc_id} missing from assessment-objectives.json")

        ao_req = ao_by_id[cmmc_id]
        controls = _parse_controls(row["controls_cell"])
        oscal_ids = [_to_oscal_id(c) for c in controls]
        rev5_notes = [REV5_NOTES[c] for c in controls if c in REV5_NOTES]
        in_moderate = [c for c, oid in zip(controls, oscal_ids) if oid in moderate_oscal]
        outside_moderate = [c for c, oid in zip(controls, oscal_ids) if oid not in moderate_oscal]

        entry = {
            "cmmc_id": cmmc_id,
            "nist_800_171": ao_req["nist_800_171"],
            "name": ao_req["name"],
            "controls_800_53_rev4": controls,
            "controls_oscal": oscal_ids,
            "fedramp_moderate": {
                "in_baseline": controls,
                "outside_baseline": outside_moderate,
            },
            "notes": row["notes"] or None,
            "rev5_notes": rev5_notes or None,
        }
        requirements.append(entry)

        for control, oscal_id in zip(controls, oscal_ids):
            idx = control_index.setdefault(
                control,
                {
                    "control_id": control,
                    "oscal_id": oscal_id,
                    "cmmc_requirements": [],
                    "fedramp_moderate": oscal_id in moderate_oscal if moderate_oscal else None,
                },
            )
            idx["cmmc_requirements"].append(cmmc_id)

    return {
        "sources": [
            "NIST SP 800-171 Revision 2, Appendix D (Mapping Tables D-1 through D-14)",
            "references/fedramp-gap.md (Appendix D reproduction, verified against primary PDF)",
            "references/data/assessment-objectives.json (CMMC requirement identifiers)",
            "NIST SP 800-53 Revision 5 FedRAMP Moderate baseline (OSCAL, usnistgov/oscal-content)",
        ],
        "verified": f"{date.today().isoformat()}: 110 requirements; Appendix D control mappings; FedRAMP Moderate baseline membership from NIST OSCAL profile",
        "mapping_source": "NIST SP 800-171 Rev 2 Appendix D",
        "nist_800_53_appendix_d_revision": "4",
        "nist_800_53_operational_revision": "5",
        "fedramp_baseline": "Moderate",
        "requirement_count": 110,
        "iso_27001_notes": ISO_27001_NOTES,
        "requirements": requirements,
        "control_index": dict(sorted(control_index.items())),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the 800-53 crosswalk dataset")
    ap.add_argument("-o", "--out", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument(
        "--offline",
        action="store_true",
        help="Skip FedRAMP Moderate baseline fetch (outside_baseline lists stay empty)",
    )
    args = ap.parse_args()

    crosswalk = build_crosswalk(fetch_baseline=not args.offline)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        json.dump(crosswalk, handle, indent=1)
        handle.write("\n")

    unique_controls = len(crosswalk["control_index"])
    outside = sum(
        len(r["fedramp_moderate"]["outside_baseline"]) for r in crosswalk["requirements"]
    )
    print(f"Wrote {args.out} ({crosswalk['requirement_count']} requirements, {unique_controls} unique 800-53 controls)")
    if not args.offline:
        print(f"Controls mapped but outside FedRAMP Moderate resolved baseline: {outside}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
