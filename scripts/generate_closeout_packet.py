#!/usr/bin/env python3
"""Assemble a POA&M closeout evidence packet from program data.

Bundles open POA&M items, linked evidence, remediation narratives, and SPRS
context for the closeout assessor (C3PAO, OSA self-assessment, or DIBCAC).

Usage (from repo root):
    python3 scripts/generate_closeout_packet.py templates/program-data.sample.yaml
    python3 scripts/generate_closeout_packet.py program.yaml -o exports/poam-closeout
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, build_sprs_export, load_json, sha256_file  # noqa: E402
from poam_lib import collect_poam_items, validate_poam_program  # noqa: E402
from validate_evidence import collect_evidence_entries, resolve_link  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


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


def poam_requirement_ids(program: dict[str, Any]) -> set[str]:
    return {item["requirement_id"] for item in collect_poam_items(program)}


def build_closeout_summary(
    program: dict[str, Any],
    dataset: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    index = {req["id"]: req for req in dataset["requirements"]}
    items_out: list[dict[str, Any]] = []

    for item in collect_poam_items(program):
        req_id = item["requirement_id"]
        meta = index.get(req_id) or {}
        objectives_out: list[dict[str, Any]] = []
        for letter, obj in (item.get("objectives") or {}).items():
            objectives_out.append(
                {
                    "objective": letter,
                    "text": (meta.get("assessment_objectives") or {}).get(letter),
                    "conformity": obj.get("conformity"),
                    "statement": obj.get("statement"),
                    "evidence": obj.get("evidence") or [],
                }
            )

        ruling = next(
            (r for r in validation.get("rulings") or [] if r.get("requirement_id") == req_id),
            {},
        )
        items_out.append(
            {
                "requirement_id": req_id,
                "name": meta.get("name"),
                "sprs_value": meta.get("sprs_value"),
                "poam": item["poam"],
                "remediation_plan": item.get("remediation_plan"),
                "objectives": objectives_out,
                "closeout_checklist": [
                    "Practice fully implemented and effective (not paper-only)",
                    "Evidence supports each assessment objective",
                    "SSP updated to reflect implementation",
                    "POA&M item marked closed with closeout date",
                ],
                "poam_eligible": ruling.get("eligible"),
                "eligibility_notes": ruling.get("reasons"),
            }
        )

    org = program.get("organization") or {}
    return {
        "schema_version": "1.0",
        "export_type": "poam_closeout_packet",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "organization": org.get("name"),
        "system_name": org.get("system_name"),
        "assessment": program.get("assessment"),
        "conditional_status_date": program.get("conditional_status_date"),
        "closeout_deadline": validation.get("closeout_deadline"),
        "days_until_closeout": validation.get("days_until_closeout"),
        "closeout_actor": validation.get("closeout_actor"),
        "validation_valid": validation.get("valid"),
        "validation_issues": validation.get("issues"),
        "poam_items": items_out,
    }


def export_closeout_packet(program_path: Path, program: dict, out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    dataset = load_json(AO_DATASET)
    validation = validate_poam_program(program, dataset)
    poam_ids = poam_requirement_ids(program)

    manifest_files: list[dict[str, Any]] = []
    program_copy = out_dir / f"program-data{program_path.suffix}"
    shutil.copy2(program_path, program_copy)
    manifest_files.append(
        {"role": "program_data", "path": program_copy.name, "sha256": sha256_file(program_copy)}
    )

    summary = build_closeout_summary(program, dataset, validation)
    summary_path = out_dir / "poam-closeout-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    manifest_files.append(
        {"role": "poam_closeout_summary", "path": summary_path.name, "sha256": sha256_file(summary_path)}
    )

    validation_path = out_dir / "poam-validation.json"
    validation_path.write_text(json.dumps(validation, indent=2, default=str) + "\n", encoding="utf-8")
    manifest_files.append(
        {"role": "poam_validation", "path": validation_path.name, "sha256": sha256_file(validation_path)}
    )

    sprs = build_sprs_export(program, dataset)
    sprs_path = out_dir / "sprs-scoresheet.json"
    sprs_path.write_text(json.dumps(sprs, indent=2, default=str) + "\n", encoding="utf-8")
    manifest_files.append(
        {"role": "sprs_export", "path": sprs_path.name, "sha256": sha256_file(sprs_path)}
    )

    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    seen: set[str] = set()

    for row in collect_evidence_entries(program):
        if row.get("requirement_id") not in poam_ids:
            continue
        link = row.get("link")
        if not link or link in seen:
            continue
        seen.add(link)
        src = resolve_link(link)
        if not src.is_file():
            manifest_files.append(
                {
                    "role": "evidence_missing",
                    "source_link": link,
                    "requirement_id": row.get("requirement_id"),
                    "objective": row.get("objective"),
                }
            )
            continue
        try:
            rel = src.relative_to(REPO_ROOT)
            dest = out_dir / rel
        except ValueError:
            dest = evidence_dir / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        manifest_files.append(
            {
                "role": "evidence",
                "source_link": link,
                "path": str(dest.relative_to(out_dir)),
                "sha256": sha256_file(dest),
                "requirement_id": row.get("requirement_id"),
            }
        )

    checklist_lines = [
        "# POA&M Closeout Readiness Checklist",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Organization: {summary.get('organization') or 'unknown'}",
        f"Closeout actor: {summary.get('closeout_actor')}",
        f"Closeout deadline: {summary.get('closeout_deadline') or 'set conditional_status_date'}",
        "",
    ]
    for item in summary["poam_items"]:
        checklist_lines.append(f"## {item['requirement_id']}: {item.get('name') or ''}")
        checklist_lines.append(f"- Owner: {(item.get('poam') or {}).get('owner', 'unset')}")
        checklist_lines.append(f"- Due: {(item.get('poam') or {}).get('due', 'unset')}")
        for step in item.get("closeout_checklist") or []:
            checklist_lines.append(f"- [ ] {step}")
        checklist_lines.append("")

    checklist_path = out_dir / "closeout-checklist.md"
    checklist_path.write_text("\n".join(checklist_lines) + "\n", encoding="utf-8")
    manifest_files.append(
        {"role": "closeout_checklist", "path": checklist_path.name, "sha256": sha256_file(checklist_path)}
    )

    package = {
        "schema_version": "1.0",
        "export_type": "poam_closeout_package",
        "generated_at": date.today().isoformat(),
        "poam_item_count": len(summary["poam_items"]),
        "validation_valid": validation["valid"],
        "files": manifest_files,
    }
    manifest_path = out_dir / "package-manifest.json"
    manifest_path.write_text(json.dumps(package, indent=2, default=str) + "\n", encoding="utf-8")
    package["manifest_sha256"] = sha256_file(manifest_path)
    manifest_path.write_text(json.dumps(package, indent=2, default=str) + "\n", encoding="utf-8")
    return package


def main() -> int:
    ap = argparse.ArgumentParser(description="Export POA&M closeout evidence packet")
    ap.add_argument("program_data", type=Path, help="program data file")
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="output directory (default: exports/poam-closeout-YYYY-MM-DD)",
    )
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data did not parse to an object")
    out_dir = args.out or Path("exports") / f"poam-closeout-{date.today().isoformat()}"
    package = export_closeout_packet(args.program_data, program, out_dir)
    print(
        f"wrote {out_dir} "
        f"({package['poam_item_count']} POA&M items, "
        f"validation={'PASS' if package['validation_valid'] else 'FAIL'})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
