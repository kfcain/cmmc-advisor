#!/usr/bin/env python3
"""Generate mock-assessment interview scripts and evidence requests from AO data.

Builds per-family (or per-requirement) prep packs from assessment_methods and
assessment_objectives in references/data/assessment-objectives.json, scoped to
requirements present in the program data file.

Usage (from repo root):
    python3 scripts/generate_mock_assessment.py templates/program-data.sample.yaml
    python3 scripts/generate_mock_assessment.py program.yaml --family AU -o exports/mock-au
    python3 scripts/generate_mock_assessment.py program.yaml --format markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import AO_DATASET, load_json  # noqa: E402
from poam_lib import domain_family  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ORDER = ["AC", "AT", "AU", "CA", "CM", "IA", "IR", "MA", "MP", "PE", "PS", "RA", "SC", "SI"]


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


def scoped_requirement_ids(program: dict[str, Any], dataset: dict[str, Any]) -> list[str]:
    program_reqs = program.get("requirements") or {}
    if program_reqs:
        return sorted(program_reqs.keys())
    return sorted(req["id"] for req in dataset["requirements"])


def interview_prompts(
    req: dict[str, Any],
    obj_letter: str,
    obj_text: str,
    system_name: str,
) -> list[str]:
    prompts: list[str] = []
    targets = (req.get("assessment_methods") or {}).get("interview") or []
    if targets:
        for target in targets:
            prompts.append(
                f"Interview {target}: How does {system_name} satisfy objective "
                f"[{obj_letter}] {obj_text}? Walk through roles, frequency, and evidence."
            )
    else:
        prompts.append(
            f"Ask the control owner: How is objective [{obj_letter}] {obj_text} "
            f"implemented in {system_name}?"
        )
    return prompts


def build_requirement_pack(
    req: dict[str, Any],
    entry: dict[str, Any] | None,
    system_name: str,
) -> dict[str, Any]:
    methods = req.get("assessment_methods") or {}
    objectives = req.get("assessment_objectives") or {}
    obj_entries = (entry or {}).get("objectives") or {}

    objective_packs: list[dict[str, Any]] = []
    for letter in sorted(objectives.keys()):
        obj_text = objectives[letter]
        prog_obj = obj_entries.get(letter) or {}
        objective_packs.append(
            {
                "objective": letter,
                "text": obj_text,
                "conformity": prog_obj.get("conformity") or (entry or {}).get("conformity"),
                "statement": prog_obj.get("statement"),
                "evidence_on_file": prog_obj.get("evidence") or [],
                "interview_prompts": interview_prompts(req, letter, obj_text, system_name),
                "scoring_template": {
                    "met": "Objective satisfied with named mechanism and corroborating evidence",
                    "not-met": "Gap documented; mechanism missing or ineffective",
                    "not-applicable": "Scoped out with boundary justification in SSP",
                    "assessor_notes": "",
                },
            }
        )

    return {
        "requirement_id": req["id"],
        "name": req.get("name"),
        "statement": req.get("statement"),
        "sprs_value": req.get("sprs_value"),
        "conformity": (entry or {}).get("conformity"),
        "examine": methods.get("examine") or [],
        "interview": methods.get("interview") or [],
        "test": methods.get("test") or [],
        "objectives": objective_packs,
        "evidence_requests": {
            "examine": methods.get("examine") or [],
            "test": methods.get("test") or [],
        },
    }


def build_mock_assessment(
    program: dict[str, Any],
    dataset: dict[str, Any],
    *,
    family_filter: str | None = None,
) -> dict[str, Any]:
    org = program.get("organization") or {}
    system_name = org.get("system_name") or org.get("name") or "the assessed system"
    index = {req["id"]: req for req in dataset["requirements"]}
    program_reqs = program.get("requirements") or {}

    families: dict[str, list[dict[str, Any]]] = {d: [] for d in DOMAIN_ORDER}
    for req_id in scoped_requirement_ids(program, dataset):
        if family_filter and domain_family(req_id) != family_filter.upper():
            continue
        meta = index.get(req_id)
        if not meta:
            continue
        fam = domain_family(req_id)
        pack = build_requirement_pack(meta, program_reqs.get(req_id), system_name)
        families.setdefault(fam, []).append(pack)

    families_out = []
    for fam in DOMAIN_ORDER:
        reqs = families.get(fam) or []
        if not reqs:
            continue
        families_out.append(
            {
                "family": fam,
                "requirement_count": len(reqs),
                "requirements": reqs,
                "family_opener": (
                    f"Mock assessment block for {fam} ({len(reqs)} practices in scope). "
                    f"Confirm scope narrative covers each practice before interviews."
                ),
            }
        )

    return {
        "schema_version": "1.0",
        "export_type": "mock_assessment_prep",
        "generated_at": date.today().isoformat(),
        "organization": org.get("name"),
        "system_name": system_name,
        "assessment": program.get("assessment"),
        "family_filter": family_filter,
        "families": families_out,
        "discovery_watchlist": build_discovery_watchlist(program),
        "usage_notes": [
            "Use examine lists as document pull requests before interview day.",
            "Score at the assessment-objective level, not practice level only.",
            "Chase the discovery watchlist first: open questions and unverified answers are where evidence fails.",
            "Cross-check POA&M-eligible gaps with validate_poam.py before conditional planning.",
        ],
    }


def build_discovery_watchlist(program: dict[str, Any]) -> dict[str, Any]:
    """Items from the discovery section a mock should chase: open questions,
    answers taken on the OSC's word, and assumptions nobody confirmed."""
    discovery = program.get("discovery") or {}
    if not isinstance(discovery, dict):
        return {}

    def entries(section: str) -> list[dict[str, Any]]:
        raw = discovery.get(section)
        if not isinstance(raw, list):
            return []
        return [e for e in raw if isinstance(e, dict)]

    open_questions = [
        {"id": q.get("id"), "question": q.get("question"), "owner": q.get("owner"), "why_it_matters": q.get("why_it_matters")}
        for q in entries("open_questions")
        if q.get("status", "open") == "open"
    ]
    unverified_answers = [
        {"id": q.get("id"), "question": q.get("question"), "answer": q.get("answer"), "confidence": q.get("confidence")}
        for q in entries("qa_log")
        if q.get("confidence") in ("reported", "assumed")
    ]
    open_assumptions = [
        {"id": a.get("id"), "statement": a.get("statement"), "risk_if_wrong": a.get("risk_if_wrong")}
        for a in entries("assumptions")
        if a.get("status", "open") == "open"
    ]
    if not (open_questions or unverified_answers or open_assumptions):
        return {}
    return {
        "open_questions": open_questions,
        "unverified_answers": unverified_answers,
        "open_assumptions": open_assumptions,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Mock Assessment Prep Pack",
        "",
        f"**System:** {report.get('system_name')}",
        f"**Generated:** {report.get('generated_at')}",
        "",
    ]
    watchlist = report.get("discovery_watchlist") or {}
    if watchlist:
        lines.append("## Discovery watchlist (chase these first)")
        lines.append("")
        for q in watchlist.get("open_questions") or []:
            lines.append(f"- **Open {q.get('id')}** ({q.get('owner') or 'no owner'}): {q.get('question')}")
        for q in watchlist.get("unverified_answers") or []:
            lines.append(f"- **Unverified {q.get('id')}** (confidence: {q.get('confidence')}): {q.get('question')}")
        for a in watchlist.get("open_assumptions") or []:
            lines.append(f"- **Assumption {a.get('id')}**: {a.get('statement')} Risk if wrong: {a.get('risk_if_wrong') or 'not recorded'}")
        lines.append("")
    for block in report.get("families") or []:
        lines.append(f"## {block['family']} ({block['requirement_count']} practices)")
        lines.append("")
        lines.append(block.get("family_opener") or "")
        lines.append("")
        for req in block.get("requirements") or []:
            lines.append(f"### {req['requirement_id']}: {req.get('name') or ''}")
            if req.get("conformity"):
                lines.append(f"- Program conformity: **{req['conformity']}**")
            if req.get("examine"):
                lines.append("- **Examine:**")
                for item in req["examine"]:
                    lines.append(f"  - {item}")
            if req.get("test"):
                lines.append("- **Test:**")
                for item in req["test"]:
                    lines.append(f"  - {item}")
            for obj in req.get("objectives") or []:
                lines.append(f"- **Objective [{obj['objective']}]** {obj.get('text')}")
                for prompt in obj.get("interview_prompts") or []:
                    lines.append(f"  - Interview: {prompt}")
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate mock-assessment prep from AO dataset")
    ap.add_argument("program_data", type=Path, help="program data YAML or JSON")
    ap.add_argument("--family", help="limit to one domain family (e.g. AU, AC)")
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="output directory (default: exports/mock-assessment-YYYY-MM-DD)",
    )
    ap.add_argument(
        "--format",
        choices=("json", "markdown", "both"),
        default="both",
        help="output format (default: both)",
    )
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data did not parse to an object")
    dataset = load_json(AO_DATASET)
    report = build_mock_assessment(program, dataset, family_filter=args.family)

    out_dir = args.out or Path("exports") / f"mock-assessment-{date.today().isoformat()}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("json", "both"):
        json_path = out_dir / "mock-assessment.json"
        json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
        print(f"wrote {json_path}")

    if args.format in ("markdown", "both"):
        md_path = out_dir / "mock-assessment.md"
        md_path.write_text(render_markdown(report), encoding="utf-8")
        print(f"wrote {md_path}")

    fam_count = len(report.get("families") or [])
    req_count = sum(b["requirement_count"] for b in report.get("families") or [])
    print(f"mock assessment pack: {fam_count} families, {req_count} requirements")
    return 0


if __name__ == "__main__":
    sys.exit(main())
