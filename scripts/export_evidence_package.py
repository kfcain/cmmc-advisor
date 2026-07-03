#!/usr/bin/env python3
"""Export a C3PAO-oriented evidence package from program data.

Bundles program data, SPRS scoresheet, and referenced evidence artifacts into
an exports/ directory with a manifest of SHA-256 hashes for reproducibility.

Usage (from repo root):
    python3 scripts/export_evidence_package.py templates/program-data.sample.yaml
    python3 scripts/export_evidence_package.py program.yaml -o exports/c3pao-package
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, build_sprs_export, load_json, sha256_file  # noqa: E402
from validate_evidence import collect_evidence_entries, resolve_link  # noqa: E402

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


def export_package(program_path: Path, program: dict, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_files: list[dict] = []

    program_copy = out_dir / f"program-data{program_path.suffix}"
    shutil.copy2(program_path, program_copy)
    manifest_files.append(
        {"role": "program_data", "path": program_copy.name, "sha256": sha256_file(program_copy)}
    )

    dataset = load_json(AO_DATASET)
    sprs = build_sprs_export(program, dataset)
    sprs_path = out_dir / "sprs-scoresheet.json"
    sprs_path.write_text(json.dumps(sprs, indent=2) + "\n", encoding="utf-8")
    manifest_files.append(
        {"role": "sprs_export", "path": sprs_path.name, "sha256": sha256_file(sprs_path)}
    )

    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    seen: set[str] = set()

    for row in collect_evidence_entries(program):
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
                "collector": row.get("collector"),
            }
        )

    meridian = program.get("meridian_import")
    if meridian:
        manifest_files.append({"role": "meridian_import_metadata", "record": meridian})

    package = {
        "schema_version": "1.0",
        "export_type": "c3pao_evidence_package",
        "generated_at": date.today().isoformat(),
        "organization": (program.get("organization") or {}).get("name"),
        "files": manifest_files,
        "sprs_summary_score": sprs.get("summary_score"),
        "evidence_file_count": sum(1 for f in manifest_files if f.get("role") == "evidence"),
        "missing_evidence_count": sum(1 for f in manifest_files if f.get("role") == "evidence_missing"),
    }
    manifest_path = out_dir / "package-manifest.json"
    manifest_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    package["manifest_sha256"] = sha256_file(manifest_path)
    manifest_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    return package


def main() -> int:
    ap = argparse.ArgumentParser(description="Export C3PAO evidence package")
    ap.add_argument("program_data", type=Path, help="program data file")
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="output directory (default: exports/evidence-package-YYYY-MM-DD)",
    )
    args = ap.parse_args()

    program = load_program(args.program_data)
    out_dir = args.out or Path("exports") / f"evidence-package-{date.today().isoformat()}"
    package = export_package(args.program_data, program, out_dir)
    print(
        f"wrote {out_dir} "
        f"({package['evidence_file_count']} evidence files, "
        f"{package['missing_evidence_count']} missing, "
        f"SPRS {package['sprs_summary_score']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
