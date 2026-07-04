#!/usr/bin/env python3
"""Import a Meridian GCP ConMon evidence run into CMMC program data.

Reads hash-chained artifacts from a Meridian evidence store (local path or
gs:// prefix recorded as an external root) and links dated evidence on mapped
CMMC requirements. Meridian maps checks to 800-171 practice ids; this script
resolves them to full requirement ids (e.g. 3.4.1 -> CM.L2-3.4.1).

Usage (from repo root):
    python3 scripts/import_meridian_run.py /path/to/meridian/evidence_store program.yaml
    python3 scripts/import_meridian_run.py ./meridian_store program.yaml --run-id 20260703T054324Z-917ba1
    python3 scripts/import_meridian_run.py ./meridian_store program.yaml --annotate-gaps
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, load_json, merge_collector_result  # noqa: E402
from meridian_lib import (  # noqa: E402
    COLLECTOR_ID,
    SOURCE_SYSTEM,
    build_nist171_index,
    cmmc_l2_ids_from_assertion,
    link_for_artifact,
    load_assertions_from_manifest,
    map_cmmc_l2_to_requirements,
    resolve_run,
    rollup_requirement_status,
    verify_meridian_chain,
)

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


def save_program(path: Path, program: dict) -> None:
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        path.write_text(yaml.safe_dump(program, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(program, indent=2, default=str) + "\n", encoding="utf-8")


def import_run(
    store_root: Path,
    program: dict,
    *,
    run_id: str | None,
    annotate_gaps: bool,
    repo_root: Path,
) -> dict[str, Any]:
    dataset = load_json(AO_DATASET)
    nist_index = build_nist171_index(dataset)
    resolved_run_id, _date, summary_path, manifest_path = resolve_run(store_root, run_id)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    collected_at = (summary.get("finished") or summary.get("started") or "")[:10]

    by_requirement: dict[str, list[dict]] = defaultdict(list)
    artifact_for_req: dict[str, str] = {}
    artifact_sha: dict[str, str] = {}

    for rel, assertion, sha in load_assertions_from_manifest(store_root, manifest):
        for req_id in map_cmmc_l2_to_requirements(cmmc_l2_ids_from_assertion(assertion), nist_index):
            by_requirement[req_id].append(assertion)
            artifact_for_req.setdefault(req_id, rel)
            artifact_sha.setdefault(req_id, sha)

    merged = 0
    failures = 0
    for req_id, assertions in sorted(by_requirement.items()):
        rel = artifact_for_req[req_id]
        link = link_for_artifact(store_root, rel, repo_root)
        rollup = rollup_requirement_status(assertions)
        fail_checks = [a.get("check_id") for a in assertions if (a.get("status") or "").upper() == "FAIL"]
        name = f"Meridian GCP ConMon {resolved_run_id} ({rollup})"
        if fail_checks:
            name += f" ({fail_checks[0]})"
            failures += 1

        merge_collector_result(
            program,
            {
                "requirement_id": req_id,
                "objectives": ["a"],
                "artifact_name": name[:200],
                "collector": COLLECTOR_ID,
                "source_system": SOURCE_SYSTEM,
                "refresh_bucket": "machine",
                "sha256": artifact_sha[req_id],
            },
            link,
            collected_at=collected_at,
        )
        merged += 1

        if annotate_gaps and rollup in ("FAIL", "ERROR"):
            req_entry = program.setdefault("requirements", {}).setdefault(req_id, {})
            obj_a = req_entry.setdefault("objectives", {}).setdefault("a", {})
            reasons = "; ".join(
                f"{a.get('check_id')}: {a.get('reason', '')[:120]}"
                for a in assertions
                if (a.get("status") or "").upper() in ("FAIL", "ERROR")
            )[:500]
            note = f"Meridian {rollup} on {collected_at}: {reasons}"
            existing = (obj_a.get("statement") or "").strip()
            if note not in existing:
                obj_a["statement"] = f"{existing}\n\n{note}".strip() if existing else note

    chain = verify_meridian_chain(store_root)
    program["meridian_import"] = {
        "last_run_id": resolved_run_id,
        "last_imported": collected_at,
        "evidence_root": str(store_root),
        "manifest_path": str(manifest_path),
        "manifest_sha256": summary.get("manifest_sha256") or manifest.get("manifest_sha256"),
        "run_status": summary.get("run_status"),
        "requirements_linked": merged,
        "requirements_with_fail": failures,
        "chain_intact": chain["chain_intact"],
    }
    return {
        "run_id": resolved_run_id,
        "requirements_linked": merged,
        "requirements_with_fail": failures,
        "chain_intact": chain["chain_intact"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Import Meridian GCP ConMon run into program data")
    ap.add_argument("meridian_store", type=Path, help="Meridian evidence store root")
    ap.add_argument("program_data", type=Path, help="program data file to update")
    ap.add_argument("--run-id", type=str, default="", help="specific Meridian run id (default: latest)")
    ap.add_argument(
        "--annotate-gaps",
        action="store_true",
        help="append Meridian FAIL/ERROR notes to objective a statements",
    )
    ap.add_argument("--verify-chain-only", action="store_true", help="verify hash chain and exit")
    args = ap.parse_args()

    store_root = args.meridian_store.resolve()
    if not store_root.is_dir():
        sys.exit(f"Meridian store not found: {store_root}")

    if args.verify_chain_only:
        result = verify_meridian_chain(store_root)
        print(json.dumps(result, indent=2, default=str))
        return 0 if result["chain_intact"] else 1

    program = load_program(args.program_data)
    stats = import_run(
        store_root,
        program,
        run_id=args.run_id or None,
        annotate_gaps=args.annotate_gaps,
        repo_root=REPO_ROOT,
    )
    save_program(args.program_data, program)
    print(
        f"imported Meridian run {stats['run_id']}: "
        f"{stats['requirements_linked']} requirements linked, "
        f"{stats['requirements_with_fail']} with FAIL signals, "
        f"chain_intact={stats['chain_intact']}"
    )
    print(f"updated {args.program_data}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
