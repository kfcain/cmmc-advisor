#!/usr/bin/env python3
"""Generate the Level 1 self-assessment package with affirmation-readiness gates.

Maps the FAR 52.204-21 requirements through the model's 17 practices to
their Level 2 identifiers (level1_counterpart in the AO dataset), pulls
status and evidence from the program data file, and checks the four
gates from references/level-1-affirmation-readiness.md. Exits 0 only
when every gate passes; otherwise prints the blockers and exits 1.

Usage (from repo root):
    python3 scripts/generate_l1_package.py program.yaml
    python3 scripts/generate_l1_package.py program.yaml -o exports/l1-package --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, load_json  # noqa: E402


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


def l1_requirements(dataset: dict) -> list[dict]:
    return [r for r in dataset.get("requirements", []) if r.get("level1_counterpart")]


def requirement_row(req: dict, entry: dict | None) -> dict:
    entry = entry if isinstance(entry, dict) else {}
    objectives = entry.get("objectives") or {}
    evidence_names: list[str] = []
    statements = 0
    for obj in objectives.values():
        if not isinstance(obj, dict):
            continue
        if obj.get("statement"):
            statements += 1
        for ev in obj.get("evidence") or []:
            if isinstance(ev, dict) and ev.get("name"):
                evidence_names.append(ev["name"])
    conformity = entry.get("conformity") or "not-assessed"
    return {
        "far_id": req["level1_counterpart"],
        "l2_id": req["id"],
        "name": req.get("name"),
        "conformity": conformity,
        "statements": statements,
        "evidence": evidence_names,
    }


def build_package(program: dict, dataset: dict) -> dict:
    org = program.get("organization") or {}
    reqs = l1_requirements(dataset)
    entries = program.get("requirements") or {}
    rows = [requirement_row(r, entries.get(r["id"])) for r in reqs]

    discovery = program.get("discovery") or {}
    qa_log = discovery.get("qa_log") if isinstance(discovery, dict) else None
    scope_checked = any(
        isinstance(q, dict) and q.get("phase") == "contracts-cui"
        for q in (qa_log if isinstance(qa_log, list) else [])
    )

    unmet = [
        r for r in rows
        if not (r["conformity"] == "met" or (r["conformity"] == "not-applicable" and r["statements"]))
    ]
    met_without_evidence = [r for r in rows if r["conformity"] == "met" and not r["evidence"]]

    roles = org.get("roles") or {}
    has_official = any(
        "affirming" in str(slug).lower() or "affirming" in str((role or {}).get("title", "")).lower()
        for slug, role in (roles.items() if isinstance(roles, dict) else [])
    )

    gates = {
        "gate_scope": {
            "passed": scope_checked,
            "reason": "hidden-CUI check recorded (contracts-cui qa_log entry)" if scope_checked
            else "no contracts-cui qa_log entry: run the hidden-CUI check and record it",
        },
        "gate_all_met": {
            "passed": not unmet,
            "reason": "all Level 1 requirements MET" if not unmet
            else f"{len(unmet)} requirement(s) not MET; Level 1 permits no POA&Ms (32 CFR 170.15)",
        },
        "gate_evidence": {
            "passed": not met_without_evidence,
            "reason": "every MET requirement carries evidence" if not met_without_evidence
            else f"{len(met_without_evidence)} MET requirement(s) have no evidence on file",
        },
        "gate_official": {
            "passed": has_official,
            "reason": "Affirming Official named in organization.roles" if has_official
            else "no role mentioning 'affirming' in organization.roles (32 CFR 170.22)",
        },
    }

    blockers: list[str] = []
    for gate in gates.values():
        if not gate["passed"]:
            blockers.append(gate["reason"])
    for r in unmet:
        blockers.append(f"{r['far_id']} ({r['l2_id']} {r['name']}): {r['conformity']}")
    for r in met_without_evidence:
        blockers.append(f"{r['far_id']} ({r['l2_id']} {r['name']}): met but no evidence")

    return {
        "schema_version": "1.0",
        "export_type": "l1_self_assessment_package",
        "generated_at": date.today().isoformat(),
        "organization": org.get("name"),
        "system_name": org.get("system_name"),
        "requirement_count": len(rows),
        "gates": gates,
        "requirements": rows,
        "blockers": blockers,
        "affirmation_ready": all(g["passed"] for g in gates.values()),
    }


def render_markdown(pkg: dict) -> str:
    lines = [
        "# Level 1 Self-Assessment Package",
        "",
        f"**Organization:** {pkg.get('organization')}",
        f"**System:** {pkg.get('system_name')}",
        f"**Generated:** {pkg.get('generated_at')}",
        f"**Affirmation ready:** {'YES' if pkg.get('affirmation_ready') else 'NO'}",
        "",
        "## Readiness gates",
        "",
        "| Gate | Result | Detail |",
        "|------|--------|--------|",
    ]
    for name, gate in pkg["gates"].items():
        lines.append(f"| {name} | {'pass' if gate['passed'] else 'FAIL'} | {gate['reason']} |")
    lines.append("")
    lines.append("## Requirements")
    lines.append("")
    by_far: dict[str, list[dict]] = {}
    for row in pkg["requirements"]:
        by_far.setdefault(row["far_id"], []).append(row)
    for far_id in sorted(by_far):
        rows = by_far[far_id]
        lines.append(f"### {far_id}")
        for r in rows:
            ev = "; ".join(r["evidence"]) if r["evidence"] else "none on file"
            lines.append(f"- {r['l2_id']} {r['name']}: **{r['conformity']}** (evidence: {ev})")
        lines.append("")
    if pkg["blockers"]:
        lines.append("## Blockers (resolve before anyone signs in SPRS)")
        lines.append("")
        for b in pkg["blockers"]:
            lines.append(f"- {b}")
        lines.append("")
    lines.append(
        "Per references/level-1-affirmation-readiness.md: the affirmation is a "
        "personally signed, annually renewed representation. Do not sign around "
        "a blocker; there is no POA&M at Level 1."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the L1 self-assessment package with readiness gates")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON")
    ap.add_argument("-o", "--out-dir", type=Path, default=None, help="output directory")
    ap.add_argument("--json", action="store_true", help="also print the JSON report to stdout")
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data did not parse to an object")
    dataset = load_json(AO_DATASET)
    pkg = build_package(program, dataset)

    out_dir = args.out_dir or Path(f"exports/l1-package-{date.today().isoformat()}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "l1-package.json").write_text(json.dumps(pkg, indent=2, default=str) + "\n", encoding="utf-8")
    (out_dir / "l1-package.md").write_text(render_markdown(pkg), encoding="utf-8")
    print(f"wrote {out_dir / 'l1-package.json'}")
    print(f"wrote {out_dir / 'l1-package.md'}")

    if args.json:
        print(json.dumps(pkg, indent=2, default=str))

    if pkg["affirmation_ready"]:
        print("affirmation ready: all gates pass")
        return 0
    print(f"NOT affirmation ready: {len(pkg['blockers'])} blocker(s)")
    for b in pkg["blockers"]:
        print(f"  - {b}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
