#!/usr/bin/env python3
"""Bootstrap a full demo OSC under examples/demo-osc/ for toolkit testing.

Creates program-data.yaml (all 110 requirements), synthetic evidence,
runs generators and validators, and writes DEMO-OSC-GUIDE.html.

Usage (from repo root):
    python3 scripts/bootstrap_demo_osc.py
    python3 scripts/bootstrap_demo_osc.py --skip-generators
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = REPO_ROOT / "examples" / "demo-osc"
SAMPLE = REPO_ROOT / "templates" / "program-data.sample.yaml"
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"
CONTROLBOT_SEEDS = REPO_ROOT / "templates" / "controlbot-poam-seeds.sample.json"

DETAILED_REQS = {
    "AC.L2-3.1.1",
    "SC.L2-3.13.11",
    "AU.L2-3.3.5",
    "IA.L2-3.5.3",
    "CA.L2-3.12.4",
    "CM.L2-3.4.1",
    "MP.L2-3.8.1",
    "MP.L2-3.8.3",
    "MP.L2-3.8.4",
    "MP.L2-3.8.5",
}
NOT_MET_NO_POAM = {"AU.L2-3.3.5"}
NOT_MET_POAM = {"CM.L2-3.4.7", "AC.L2-3.1.22"}
PARTIAL = {"IA.L2-3.5.3", "SC.L2-3.13.11"}
INHERITED_PE = {
    "PE.L2-3.10.1",
    "PE.L2-3.10.2",
    "PE.L2-3.10.3",
    "PE.L2-3.10.4",
    "PE.L2-3.10.5",
    "PE.L2-3.10.6",
}


def load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_yaml(data: dict, path: Path) -> None:
    import yaml

    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")


def run(cmd: list[str], *, cwd: Path = REPO_ROOT, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True, check=False)


def default_objectives(req: dict, *, inherited: bool = False) -> dict:
    objectives: dict = {}
    for letter in req["assessment_objectives"]:
        if inherited:
            objectives[letter] = {
                "conformity": "inherited",
                "statement": (
                    "Physical protection for the GCC High boundary is inherited from "
                    "Microsoft 365 GCC High per CRM Appendix J; no customer-operated "
                    "datacenter for this enclave."
                ),
                "inheritance": {
                    "source": "gcch",
                    "type": "inherited",
                    "crm_ref": "PE family rows (Appendix J)",
                },
            }
        else:
            objectives[letter] = {
                "conformity": "met",
                "statement": (
                    f"Demo OSC: {req['name']} objective {letter} satisfied via "
                    "documented enclave controls (Atlas Precision Manufacturing)."
                ),
                "evidence": [
                    {
                        "name": f"Demo evidence — {req['id']} [{letter}]",
                        "link": f"evidence/demo/{req['id'].replace('.', '-')}-{letter}.json",
                        "collected": str(date.today()),
                        "refresh_bucket": "document",
                    }
                ],
            }
    return objectives


def roll_up_conformity(objectives: dict, req_id: str) -> str:
    if req_id in NOT_MET_NO_POAM:
        return "not-met"
    if req_id in NOT_MET_POAM:
        return "not-met"
    if req_id in PARTIAL:
        return "partially-met"
    values = {o.get("conformity") for o in objectives.values()}
    if values <= {"inherited"}:
        return "met"
    if "not-met" in values:
        return "not-met"
    if "shared" in values or "partially-met" in values:
        return "partially-met"
    return "met"


def apply_paper_cui_enrichment(program: dict, reqs: dict) -> None:
    """Paper CUI: cover sheets, shredding, chain of custody, asset stickers."""
    today = str(date.today())
    org = program.setdefault("organization", {})
    org["scope_narrative"] = (
        (org.get("scope_narrative") or "")
        + " Paper CUI (marked CTI hardcopy, traveler drawings, mail pouches) is "
        "in scope for the CUI floor mail room, locked job boxes, and cross-cut "
        "destruction path; digital CUI remains in GCC High."
    )
    assets = program.setdefault("assets", {})
    assets.setdefault("cui", []).extend(
        [
            {
                "name": "CUI mail room (Building A Room 104)",
                "description": "Inbound/outbound hardcopy staging, cover-sheet log, locked shred console",
            },
            {
                "name": "Locked CUI job boxes (12, ENG floor)",
                "description": "Orange CUI asset stickers; keys on PE access list",
            },
        ]
    )
    assets.setdefault("contractor_risk_managed", []).append(
        {
            "name": "HSM cross-cut shredder (Model HSM-150)",
            "location": "Mail room 104",
            "description": "Destroy sanitization for daily paper CUI; strip-cut prohibited by policy",
            "baseline_profile": "printer-mfp",
            "baseline_validation": {
                "validated": "2026-06-18",
                "cross_cut": True,
                "shred_log_maintained": True,
            },
        }
    )
    assets.setdefault("security_protection", []).append(
        {
            "name": "Certified destruction vendor (NAID AAA)",
            "vendor": "SecureShred Regional",
            "description": "Quarterly bulk purge with certificate of destruction",
        }
    )

    policies = program.setdefault("policies", [])
    policies.append(
        {
            "id": "pol-mp-paper",
            "title": "Paper CUI Marking, Transport, and Destruction",
            "version": "1.2",
            "owner": "Sam Patel",
            "reviewed": "2026-05-20",
            "location": "policies/paper-cui-handling-v1.2.pdf",
            "procedures": [
                "procedures/cui-cover-sheet-v1.pdf",
                "procedures/shred-chain-of-custody-v1.pdf",
                "procedures/cui-mail-courier-v1.pdf",
            ],
            "requirements": [
                "MP.L2-3.8.1",
                "MP.L2-3.8.3",
                "MP.L2-3.8.4",
                "MP.L2-3.8.5",
                "PE.L2-3.10.6",
            ],
        }
    )

    discovery = program.setdefault("discovery", {})
    discovery["updated"] = today
    phases = discovery.setdefault("phases", {})
    phases["physical-media"] = {
        "status": "in-progress",
        "last_touched": today,
        "summary": (
            "Paper CUI cover sheets and cross-cut shred log in place. Mail-room "
            "accumulation backlog and MFP scan relay still open. NAID vendor "
            "certificates on file for Q1 bulk purge."
        ),
    }
    discovery.setdefault("qa_log", []).extend(
        [
            {
                "id": "QA-0005",
                "date": "2026-07-04",
                "phase": "physical-media",
                "question": "What shred method and particle size apply to paper CUI, and who witnesses destruction?",
                "answer": (
                    "Policy requires cross-cut Destroy per NIST SP 800-88. Daily "
                    "shred uses HSM-150 in mail room with dual-person witness log. "
                    "Bulk boxes use NAID AAA vendor with certificate of destruction."
                ),
                "answered_by": "ISSM",
                "confidence": "verified",
                "affects": ["HSM cross-cut shredder (Model HSM-150)"],
            },
            {
                "id": "QA-0006",
                "date": "2026-07-04",
                "phase": "physical-media",
                "question": "How is chain of custody maintained when paper CUI goes to the prime via FedEx?",
                "answer": (
                    "Cover sheet, tamper-evident inner envelope, outer label without "
                    "content sensitivity, FedEx signature required, handoff log signed "
                    "by mail-room clerk and ISSM for each shipment."
                ),
                "answered_by": "Mail room supervisor",
                "confidence": "verified",
                "affects": ["CUI mail room (Building A Room 104)"],
            },
        ]
    )
    discovery.setdefault("open_questions", []).append(
        {
            "id": "OQ-0003",
            "raised": today,
            "phase": "physical-media",
            "question": "Does the mail-room accumulation shelf (pre-shred staging) meet locked-media control for overnight storage?",
            "why_it_matters": (
                "MP.L2-3.8.1 requires physical control at rest; unlocked staging "
                "recategorizes the shelf as a CUI store."
            ),
            "owner": "Sam Patel",
            "status": "open",
        }
    )

    paper_evidence = {
        "cover_sheet_sample": "evidence/mp/paper/cui-cover-sheet-sample-redacted.pdf",
        "shred_log": "evidence/mp/paper/shred-witness-log-2026-06.csv",
        "coc_fedex": "evidence/mp/paper/chain-of-custody-fedex-2026-06-12.pdf",
        "vendor_cert": "evidence/mp/paper/n aid-destruction-cert-2026-q1.pdf",
        "asset_stickers": "evidence/mp/paper/cui-asset-sticker-inventory-2026-06.json",
        "marking_std": "evidence/mp/paper/cui-marking-standard-excerpt.pdf",
    }
    # fix typo naid
    paper_evidence["vendor_cert"] = "evidence/mp/paper/naid-destruction-cert-2026-q1.pdf"

    reqs["MP.L2-3.8.1"] = {
        "conformity": "partially-met",
        "objectives": {
            "a": {
                "conformity": "met",
                "statement": (
                    "Paper CUI at rest in locked job boxes and locked file cabinets "
                    "on the CUI floor; orange CUI stickers on each container."
                ),
                "evidence": [
                    {"name": "CUI asset sticker inventory", "link": paper_evidence["asset_stickers"], "collected": today, "refresh_bucket": "periodic"},
                    {"name": "PE access list for job-box keys", "link": "evidence/mp/paper/job-box-key-register-2026-06.csv", "collected": today, "refresh_bucket": "periodic"},
                ],
            },
            "b": {
                "conformity": "not-met",
                "statement": (
                    "Mail-room pre-shred accumulation shelf is not locked overnight; "
                    "POA&M tracks lockable console install."
                ),
            },
        },
        "poam": {
            "priority": "Medium",
            "description": "Install locked shred console for overnight mail-room accumulation",
            "opened": "2026-07-01",
            "due": "2026-08-15",
            "owner": "Sam Patel",
            "status": "in-progress",
            "actions": ["Procure lockable console", "Update mail-room procedure", "Photo evidence for assessor"],
        },
    }
    reqs["MP.L2-3.8.3"] = {
        "conformity": "met",
        "objectives": {
            "a": {
                "conformity": "met",
                "statement": (
                    "Paper CUI destroyed via cross-cut shredding (HSM-150) with dual-person "
                    "witness log, or NAID AAA vendor with certificate of destruction. "
                    "No recycling bins for CUI."
                ),
                "evidence": [
                    {"name": "Shred witness log", "link": paper_evidence["shred_log"], "collected": today, "refresh_bucket": "periodic"},
                    {"name": "NAID destruction certificate Q1", "link": paper_evidence["vendor_cert"], "collected": "2026-03-15", "refresh_bucket": "document"},
                    {"name": "Paper CUI destruction procedure", "link": "policies/paper-cui-handling-v1.2.pdf", "collected": today, "refresh_bucket": "document"},
                ],
            }
        },
    }
    reqs["MP.L2-3.8.4"] = {
        "conformity": "met",
        "objectives": {
            "a": {
                "conformity": "met",
                "statement": (
                    "CTI banner and portion markings applied per 32 CFR 2002; CUI cover "
                    "sheets on all external transmittals."
                ),
                "evidence": [
                    {"name": "Redacted cover sheet sample", "link": paper_evidence["cover_sheet_sample"], "collected": today, "refresh_bucket": "document"},
                    {"name": "Marking standard excerpt", "link": paper_evidence["marking_std"], "collected": today, "refresh_bucket": "document"},
                ],
            },
            "b": {
                "conformity": "met",
                "statement": "Distribution limitations (NOFORN where applicable) on cover sheets and document headers.",
                "evidence": [
                    {"name": "Training roster — paper CUI marking", "link": "evidence/mp/paper/marking-training-roster-2026-05.csv", "collected": today, "refresh_bucket": "periodic"},
                ],
            },
        },
    }
    reqs["MP.L2-3.8.5"] = {
        "conformity": "met",
        "objectives": {
            "a": {
                "conformity": "met",
                "statement": (
                    "Only mail-room clerks and ISSM may remove paper CUI from the CUI floor; "
                    "authorization logged on cover sheet."
                ),
                "evidence": [
                    {"name": "Mail/courier authorization procedure", "link": "procedures/cui-mail-courier-v1.pdf", "collected": today, "refresh_bucket": "document"},
                ],
            },
            "b": {
                "conformity": "met",
                "statement": (
                    "Chain-of-custody forms for FedEx and internal courier; signature on delivery."
                ),
                "evidence": [
                    {"name": "FedEx chain of custody 2026-06-12", "link": paper_evidence["coc_fedex"], "collected": "2026-06-12", "refresh_bucket": "periodic"},
                    {"name": "Chain of custody blank template", "link": "procedures/shred-chain-of-custody-v1.pdf", "collected": today, "refresh_bucket": "document"},
                ],
            },
        },
    }


def build_program() -> dict:
    import yaml

    base = load_yaml(SAMPLE)
    dataset = json.loads(AO_DATASET.read_text(encoding="utf-8"))
    program = deepcopy(base)

    program["organization"] = {
        **program.get("organization", {}),
        "name": "Atlas Precision Manufacturing LLC",
        "system_name": "APM GCC High CUI Enclave",
        "cage_codes": ["8XYZ9"],
        "revision": "Rev 2",
        "date": str(date.today()),
        "purpose": "Demo OSC for CMMC Advisor toolkit walkthrough",
        "scope_narrative": (
            "Atlas Precision Manufacturing (APM) machines vehicle components for an "
            "Army prime. CUI (CTI and export-controlled drawings) is processed only "
            "in a Microsoft 365 GCC High tenant, twelve Intune-managed Windows "
            "laptops, Azure Government file services, and Microsoft Sentinel. "
            "Commercial M365, corporate HR/finance, and IGEL thin-client VDI "
            "terminals are out of scope with documented separation."
        ),
        "environment_narrative": (
            "Primary enclave: GCC High (Entra ID USGov, EXO/SPO/Teams), Azure "
            "Government (Sentinel, project file share). Edge: FortiGate 100F. "
            "RMM: NinjaOne for Government on CUI laptops only. Engineering uses "
            "Azure DevOps Government for IaC; ControlBot gates Terraform PRs."
        ),
        "roles": {
            **program.get("organization", {}).get("roles", {}),
            "system_owner": {
                "name": "Jordan Rivera",
                "title": "Director of Engineering",
                "email": "jrivera@atlasprecision.example",
            },
            "issm": {
                "name": "Sam Patel",
                "title": "ISSM / IT Security Lead",
                "email": "spatel@atlasprecision.example",
                "responsibilities": [
                    "Maintain SSP, POA&M, and program-data.yaml",
                    "Run quarterly evidence collection and SPRS updates",
                ],
            },
            "affirming_official": {
                "name": "Casey Morgan",
                "title": "CEO",
                "email": "cmorgan@atlasprecision.example",
                "responsibilities": ["Affirm continuing compliance in SPRS"],
            },
            "engineer_lead": {
                "name": "Alex Kim",
                "title": "Cloud Engineering Lead",
                "email": "akim@atlasprecision.example",
                "responsibilities": ["ControlBot profile and Terraform enclave IaC"],
            },
        },
    }

    program["assessment"] = {
        "level": "2",
        "path": "c3pao",
        "target_date": "2026-11-15",
        "c3pao": "Demo C3PAO (placeholder)",
    }
    program["sprs_submission"] = {
        "score": 92,
        "date": "2026-06-15",
        "submitted_by": "Sam Patel",
        "notes": "Pre-assessment self-score; dashboard computed score reflects open gaps",
    }

    phases = program.setdefault("discovery", {}).setdefault("phases", {})
    for phase_id, summary in {
        "people": ("complete", "42 in-scope users; screening records in HRIS"),
        "locations": ("complete", "Single HQ; CUI floor badge-controlled"),
        "platforms-tenants": ("complete", "GCC High tenant isolated from commercial M365"),
        "endpoints": ("complete", "12 Intune laptops; AVD for remote engineers"),
        "data-flows": ("in-progress", "DFD updated; MFP scan path still open"),
        "backup-dr": ("in-progress", "Azure backup for file share; restore test due Q3"),
        "esps-access-paths": ("in-progress", "MSP NinjaOne console path under review"),
    }.items():
        phases.setdefault(phase_id, {})
        phases[phase_id].update(
            {
                "status": summary[0],
                "last_touched": str(date.today()),
                "summary": summary[1],
            }
        )

    program["grc_integrations"] = {
        "demo-placeholder": {
            "last_sync": str(date.today()),
            "last_snapshot": "templates/grc-snapshot.sample.json",
            "requirements_linked": 0,
            "unmapped_count": 110,
            "workspace_id": "demo-workspace",
        }
    }

    reqs: dict = {}
    sample_reqs = program.get("requirements") or {}
    for row in dataset["requirements"]:
        rid = row["id"]
        if rid in sample_reqs and rid in DETAILED_REQS:
            reqs[rid] = deepcopy(sample_reqs[rid])
            continue
        inherited = rid in INHERITED_PE
        objectives = default_objectives(row, inherited=inherited)
        entry: dict = {
            "conformity": roll_up_conformity(objectives, rid),
            "objectives": objectives,
        }
        if rid == "IA.L2-3.5.3":
            entry["objectives"]["c"]["conformity"] = "met"
            entry["objectives"]["d"]["conformity"] = "not-met"
            entry["statement"] = (
                "Phishing-resistant MFA enforced via CA; one legacy app still on SMS OTP."
            )
        if rid == "CA.L2-3.12.4":
            entry["conformity"] = "met"
            entry["objectives"]["a"]["statement"] = (
                "System Security Plan maintained at Rev 2; generated from program-data.yaml."
            )
            entry["objectives"]["a"]["evidence"] = [
                {
                    "name": "SSP Rev 2 (generated)",
                    "link": "outputs/ssp.md",
                    "collected": str(date.today()),
                    "refresh_bucket": "document",
                }
            ]
        if rid in NOT_MET_POAM:
            entry["poam"] = {
                "priority": "Medium",
                "description": f"Close gap on {rid} before C3PAO assessment",
                "opened": "2026-06-01",
                "due": "2026-09-30",
                "owner": "Sam Patel",
                "status": "open",
                "actions": ["Document control", "Collect assessor evidence", "Update conformity"],
            }
        reqs[rid] = entry

    apply_paper_cui_enrichment(program, reqs)
    program["requirements"] = reqs
    program["diagrams"] = {
        "network": "outputs/diagrams/network.svg",
        "cui_flow": "outputs/diagrams/cui-flow.svg",
    }
    return program


def write_evidence_stubs(program: dict, evidence_root: Path) -> None:
    evidence_root.mkdir(parents=True, exist_ok=True)
    for req_id, entry in (program.get("requirements") or {}).items():
        for obj in (entry.get("objectives") or {}).values():
            for ev in obj.get("evidence") or []:
                link = ev.get("link")
                if not link or link.startswith("http"):
                    continue
                path = DEMO_ROOT / link
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.suffix == ".json":
                    payload = {
                        "demo": True,
                        "requirement": req_id,
                        "evidence_name": ev.get("name"),
                        "collected": ev.get("collected"),
                        "note": "Synthetic collector output for toolkit testing",
                    }
                    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
                elif path.suffix == ".csv":
                    path.write_text("user,group,source\njrivera,ENG-CUI,entra\n", encoding="utf-8")
                elif path.suffix == ".pdf":
                    path.write_text("%PDF-1.4 demo placeholder\n", encoding="utf-8")
                else:
                    path.write_text(f"Demo evidence stub for {ev.get('name')}\n", encoding="utf-8")

    sample_paths = [
        "evidence/ac/3.1.1/group-export-2026-06.csv",
        "evidence/ac/3.1.1/ca-01-export.json",
        "evidence/sc/3.13.11/intune-fips-policy.json",
    ]
    for rel in sample_paths:
        src = REPO_ROOT / "templates" / "program-data.sample.yaml"
        _ = src
        dest = evidence_root.parent / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            if rel.endswith(".json"):
                dest.write_text('{"demo": true, "collector": "manual-upload"}\n', encoding="utf-8")
            else:
                dest.write_text("demo,stub\n", encoding="utf-8")


def run_generators(program_path: Path, out_dir: Path, report_lines: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    jobs: list[tuple[str, list[str]]] = [
        ("dashboard", [py, "scripts/generate_dashboard.py", str(program_path), "-o", str(out_dir / "dashboard.html")]),
        ("ssp", [py, "scripts/generate_ssp.py", str(program_path), "-o", str(out_dir / "ssp.md")]),
        ("diagrams", [py, "scripts/generate_diagrams.py", str(program_path), "-o", str(out_dir / "diagrams")]),
        ("trust-center", [py, "scripts/generate_trust_center.py", str(program_path), "-o", str(out_dir / "trust-center.html")]),
        ("executive-brief", [py, "scripts/generate_executive_brief.py", str(program_path), "-o", str(out_dir / "executive-brief.html")]),
        ("oscal", [py, "scripts/generate_oscal_ssp.py", str(program_path), "-o", str(out_dir / "oscal-ssp.json")]),
        ("sprs-json", [py, "scripts/export_sprs.py", str(program_path), "-o", str(out_dir / "sprs.json")]),
        ("sprs-csv", [py, "scripts/export_sprs.py", str(program_path), "--csv", str(out_dir / "sprs.csv")]),
        ("mock-ia", [py, "scripts/generate_mock_assessment.py", str(program_path), "--family", "IA", "-o", str(out_dir / "mock-assessment-ia"), "--format", "markdown"]),
        ("raci", [py, "scripts/generate_responsibility_matrix.py", str(program_path), "-o", str(out_dir / "responsibility-matrix"), "--format", "markdown"]),
        ("recommend", [py, "scripts/recommend_solutions.py", str(program_path), "-o", str(out_dir / "recommend-solutions.md"), "--format", "md"]),
        ("controlbot-profile", [py, "scripts/export_controlbot_profile.py", str(program_path), "-o", str(out_dir / "controlbot-profile.yaml")]),
        ("collect-dry", [py, "scripts/collect_evidence.py", str(program_path), "--dry-run", "--evidence-root", str(DEMO_ROOT / "evidence")]),
    ]
    for name, cmd in jobs:
        proc = run(cmd)
        report_lines.append(f"## {name}\n")
        report_lines.append(f"command: {' '.join(cmd)}\n")
        report_lines.append(f"exit: {proc.returncode}\n")
        if proc.stdout:
            report_lines.append(proc.stdout[:4000])
        if proc.stderr:
            report_lines.append(proc.stderr[:2000])
        report_lines.append("\n")

    validators: list[tuple[str, list[str], Path]] = [
        ("validate-poam", [py, "scripts/validate_poam.py", str(program_path), "--json"], out_dir / "validate-poam.json"),
        ("validate-assets", [py, "scripts/validate_asset_baselines.py", str(program_path), "--json"], out_dir / "validate-assets.json"),
        ("validate-evidence", [py, "scripts/validate_evidence.py", str(program_path), "-o", str(out_dir / "validate-evidence.json")], out_dir / "validate-evidence.json"),
        ("discovery", [py, "scripts/discovery_report.py", str(program_path)], out_dir / "discovery-report.txt"),
    ]
    for name, cmd, dest in validators:
        proc = run(cmd)
        report_lines.append(f"## {name}\n")
        report_lines.append(f"exit: {proc.returncode}\n")
        body = proc.stdout or proc.stderr or ""
        if name == "discovery":
            dest.write_text(body, encoding="utf-8")
        elif proc.stdout:
            dest.write_text(proc.stdout, encoding="utf-8")
        report_lines.append(body[:6000])
        report_lines.append("\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap demo OSC example")
    ap.add_argument("--skip-generators", action="store_true")
    args = ap.parse_args()

    if DEMO_ROOT.exists():
        shutil.rmtree(DEMO_ROOT)
    DEMO_ROOT.mkdir(parents=True)
    out_dir = DEMO_ROOT / "outputs"
    evidence_dir = DEMO_ROOT / "evidence"
    program_path = DEMO_ROOT / "program-data.yaml"

    program = build_program()
    dump_yaml(program, program_path)
    write_evidence_stubs(program, evidence_dir)

    (DEMO_ROOT / "controlbot").mkdir(parents=True, exist_ok=True)
    shutil.copy(CONTROLBOT_SEEDS, DEMO_ROOT / "controlbot" / "poam-seeds.json")

    run(
        [
            sys.executable,
            "scripts/import_controlbot_seeds.py",
            str(DEMO_ROOT / "controlbot" / "poam-seeds.json"),
            str(program_path),
            "--evidence",
            str(REPO_ROOT / "templates" / "controlbot-evidence-facts.sample.json"),
        ]
    )
    program = load_yaml(program_path)

    report_lines = ["# Atlas Precision Manufacturing — Demo OSC Test Report\n", f"Generated: {date.today()}\n\n"]
    if not args.skip_generators:
        run_generators(program_path, out_dir, report_lines)
    (out_dir / "demo-test-report.txt").write_text("".join(report_lines), encoding="utf-8")

    run([sys.executable, "scripts/generate_demo_guide.py", str(DEMO_ROOT)])
    print(f"demo OSC ready: {DEMO_ROOT}")
    print(f"  open {DEMO_ROOT / 'DEMO-OSC-GUIDE.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
