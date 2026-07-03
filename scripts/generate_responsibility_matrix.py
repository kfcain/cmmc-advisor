#!/usr/bin/env python3
"""Export internal RACI / responsibility matrix from program data.

Distinct from FedRAMP CRM: maps organization.roles to CMMC practice scope.

Usage (from repo root):
    python3 scripts/generate_responsibility_matrix.py templates/program-data.sample.yaml
    python3 scripts/generate_responsibility_matrix.py program.yaml -o exports/raci
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def role_label(program: dict[str, Any], slug: str | None) -> str:
    if not slug:
        return ""
    role = (program.get("organization") or {}).get("roles") or {}
    entry = role.get(slug) or {}
    name = entry.get("name") or slug
    title = entry.get("title")
    return f"{name} ({title})" if title else name


def build_matrix(program: dict[str, Any]) -> dict[str, Any]:
    org = program.get("organization") or {}
    matrix = program.get("responsibility_matrix") or {}
    entries_out: list[dict[str, Any]] = []

    for entry in matrix.get("entries") or []:
        entries_out.append(
            {
                "scope": entry.get("scope"),
                "scope_label": entry.get("scope_label") or entry.get("scope"),
                "accountable": entry.get("accountable"),
                "accountable_label": role_label(program, entry.get("accountable")),
                "responsible": entry.get("responsible") or [],
                "responsible_labels": [role_label(program, s) for s in entry.get("responsible") or []],
                "consulted": entry.get("consulted") or [],
                "consulted_labels": [role_label(program, s) for s in entry.get("consulted") or []],
                "informed": entry.get("informed") or [],
                "informed_labels": [role_label(program, s) for s in entry.get("informed") or []],
                "evidence_owner": entry.get("evidence_owner"),
                "evidence_owner_label": role_label(program, entry.get("evidence_owner")),
                "notes": entry.get("notes"),
            }
        )

    return {
        "schema_version": "1.0",
        "export_type": "responsibility_matrix",
        "generated_at": date.today().isoformat(),
        "organization": org.get("name"),
        "system_name": org.get("system_name"),
        "matrix_updated": matrix.get("updated"),
        "matrix_notes": matrix.get("notes"),
        "disclaimer": (
            "Internal RACI for CMMC program governance. Not a FedRAMP Customer "
            "Responsibility Matrix; see inheritance_sources for CRM rows."
        ),
        "entries": entries_out,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# CMMC Internal Responsibility Matrix",
        "",
        f"**Organization:** {report.get('organization')}",
        f"**System:** {report.get('system_name')}",
        f"**Matrix updated:** {report.get('matrix_updated') or 'unset'}",
        f"**Generated:** {report.get('generated_at')}",
        "",
        report.get("disclaimer") or "",
        "",
        "| Scope | A | R | C | I | Evidence owner | Notes |",
        "|-------|---|---|---|---|----------------|-------|",
    ]
    for row in report.get("entries") or []:
        r = ", ".join(row.get("responsible_labels") or []) or "-"
        c = ", ".join(row.get("consulted_labels") or []) or "-"
        i = ", ".join(row.get("informed_labels") or []) or "-"
        lines.append(
            f"| {row.get('scope_label')} | {row.get('accountable_label') or '-'} | "
            f"{r} | {c} | {i} | {row.get('evidence_owner_label') or '-'} | "
            f"{row.get('notes') or ''} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Export responsibility matrix from program data")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=None)
    ap.add_argument("--format", choices=("json", "markdown", "both"), default="both")
    args = ap.parse_args()

    program = load_program(args.program_data)
    report = build_matrix(program)
    out_dir = args.out or Path("exports") / f"responsibility-matrix-{date.today().isoformat()}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("json", "both"):
        path = out_dir / "responsibility-matrix.json"
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path}")

    if args.format in ("markdown", "both"):
        path = out_dir / "responsibility-matrix.md"
        path.write_text(render_markdown(report), encoding="utf-8")
        print(f"wrote {path}")

    print(f"entries: {len(report.get('entries') or [])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
