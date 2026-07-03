"""Executive brief and gap-driven solution recommendation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from evidence_lib import compute_sprs, evidence_stale

# Gap family prefix -> marketplace capability + CIS/on-prem fallback
FAMILY_SOLUTIONS: dict[str, dict[str, str]] = {
    "AC": {
        "category": "IAM / PAM / identity governance",
        "marketplace": "Search marketplace.fedramp.gov: IAM, PAM, identity governance; Moderate or Rev5 Class C",
        "fallback": "CIS Microsoft/Azure benchmarks for IdP; on-prem: CIS Controls v8 IG1 for access",
    },
    "AT": {
        "category": "Security awareness / training platform",
        "marketplace": "FedRAMP-authorized LMS or training record systems where CUI training is tracked in SaaS",
        "fallback": "Documented AT program with LMS export; no FedRAMP required if no CUI in vendor",
    },
    "AU": {
        "category": "SIEM / log aggregation",
        "marketplace": "SIEM category in references/fedramp-marketplace-guide.md (Splunk, Sentinel, etc.)",
        "fallback": "On-prem SIEM with CIS log retention baseline; cloud-native collectors in evidence manifest",
    },
    "CA": {
        "category": "GRC / continuous monitoring",
        "marketplace": "GRC platforms with FedRAMP Moderate or Class C listing if storing CUI program data",
        "fallback": "Program dashboard + POA&M in program-data.yaml; Vanta/Drata for monitor-only",
    },
    "CM": {
        "category": "Configuration management / MDM / baselines",
        "marketplace": "MDM/endpoint management FedRAMP packages when management plane touches CUI",
        "fallback": "CIS Benchmarks + DISA STIGs per OS; Intune/GPO exports for evidence",
    },
    "IA": {
        "category": "MFA / authenticator management",
        "marketplace": "FedRAMP Moderate MFA/PAM (Duo FedRAMP package, etc.)",
        "fallback": "Entra Conditional Access / on-prem MFA with CIS authenticator guidance",
    },
    "IR": {
        "category": "Incident response / SOAR",
        "marketplace": "FedRAMP SIEM/SOAR with 72-hour reporting workflow documented",
        "fallback": "IR playbooks + ticketing; DIBNet reporting runbooks in program governance",
    },
    "MA": {
        "category": "Maintenance / patch / vulnerability",
        "marketplace": "Vulnerability management FedRAMP packages",
        "fallback": "CIS patch SLAs; WSUS/Intune patch reports; CISA KEV tracking",
    },
    "MP": {
        "category": "Media protection / DLP",
        "marketplace": "DLP and secure collaboration FedRAMP Moderate listings",
        "fallback": "Encrypted removable media policy; M365 DLP in GCC High",
    },
    "PE": {
        "category": "Physical access control (PACS)",
        "marketplace": "Rare at FedRAMP Moderate; usually on-prem PACS vendor",
        "fallback": "CIS physical security controls; badge system exports via on-prem-inspectors",
    },
    "PS": {
        "category": "Personnel screening records",
        "marketplace": "HRIS with FedRAMP only if CUI in HR SaaS",
        "fallback": "Personnel screening file exports; PS policy mapping",
    },
    "RA": {
        "category": "Vulnerability scanning / risk assessment",
        "marketplace": "Vulnerability management category in fedramp-marketplace-guide.md",
        "fallback": "CIS scanning cadence; authenticated scan evidence",
    },
    "SC": {
        "category": "Network security / SASE / boundary protection",
        "marketplace": "SASE/ZTNA and network security FedRAMP Moderate packages",
        "fallback": "CIS firewall/switch benchmarks; NGFW/WLAN baselines in asset-baselines/",
    },
    "SI": {
        "category": "EDR / malicious code protection",
        "marketplace": "EDR category in fedramp-marketplace-guide.md (CrowdStrike, Defender, etc.)",
        "fallback": "CIS endpoint malware controls; EDR API collectors",
    },
}


@dataclass
class GapItem:
    requirement_id: str
    name: str
    sprs_value: int
    status: str
    family: str
    remediation_plan: str | None = None
    poam_open: bool = False


@dataclass
class ExecutiveBriefData:
    organization: dict[str, Any]
    assessment: dict[str, Any]
    sprs: dict[str, Any]
    sprs_submission: dict[str, Any] | None
    top_gaps: list[GapItem]
    points_at_stake: int
    open_poam_count: int
    poam_overdue_count: int
    families_with_gaps: dict[str, int]
    stale_evidence_count: int
    solution_hints: list[dict[str, str]]
    cost_framework_note: str
    generated_date: str


def eff_status(req_id: str, entries: dict[str, Any]) -> str:
    return (entries.get(req_id) or {}).get("conformity") or "not-assessed"


def build_executive_brief(program: dict, dataset: dict) -> ExecutiveBriefData:
    entries = program.get("requirements") or {}
    sprs = compute_sprs(program, dataset)
    gaps: list[GapItem] = []

    for req in dataset["requirements"]:
        rid = req["id"]
        status = eff_status(rid, entries)
        if status not in ("not-met", "partially-met"):
            continue
        entry = entries.get(rid) or {}
        poam = entry.get("poam") or {}
        gaps.append(
            GapItem(
                requirement_id=rid,
                name=req.get("name") or "",
                sprs_value=int(req.get("sprs_value") or 0),
                status=status,
                family=rid.split(".")[0],
                remediation_plan=entry.get("remediation_plan"),
                poam_open=poam.get("status") not in (None, "closed"),
            )
        )

    gaps.sort(key=lambda g: (-g.sprs_value, g.requirement_id))
    top_gaps = gaps[:15]
    points_at_stake = sum(g.sprs_value for g in gaps)

    open_poam = 0
    poam_overdue = 0
    today = date.today()
    for entry in entries.values():
        poam = entry.get("poam") or {}
        if poam.get("status") in (None, "open", "in-progress"):
            open_poam += 1
            due = poam.get("due")
            if due:
                try:
                    if date.fromisoformat(str(due)[:10]) < today:
                        poam_overdue += 1
                except ValueError:
                    pass

    families: dict[str, int] = {}
    for g in gaps:
        families[g.family] = families.get(g.family, 0) + 1

    stale = 0
    for entry in entries.values():
        for obj in (entry.get("objectives") or {}).values():
            for ev in obj.get("evidence") or []:
                if evidence_stale(ev.get("collected"), ev.get("refresh_bucket") or "machine"):
                    stale += 1

    hints = recommend_for_families(sorted(families.keys(), key=lambda f: -families[f])[:8])

    return ExecutiveBriefData(
        organization=program.get("organization") or {},
        assessment=program.get("assessment") or {},
        sprs=sprs,
        sprs_submission=program.get("sprs_submission"),
        top_gaps=top_gaps,
        points_at_stake=points_at_stake,
        open_poam_count=open_poam,
        poam_overdue_count=poam_overdue,
        families_with_gaps=families,
        stale_evidence_count=stale,
        solution_hints=hints,
        cost_framework_note=(
            "Planning ranges for Level 2 preparation and tooling appear in "
            "references/contractor-profiles.md (CMMC cost framework). "
            "Use remediation_plan fields in program data for project-specific estimates."
        ),
        generated_date=date.today().isoformat(),
    )


def recommend_for_families(families: list[str]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for fam in families:
        meta = FAMILY_SOLUTIONS.get(fam)
        if not meta:
            continue
        out.append({"family": fam, **meta})
    return out


def brief_to_dict(brief: ExecutiveBriefData) -> dict[str, Any]:
    return {
        "organization": brief.organization,
        "assessment": brief.assessment,
        "sprs": brief.sprs,
        "sprs_submission": brief.sprs_submission,
        "top_gaps": [g.__dict__ for g in brief.top_gaps],
        "points_at_stake": brief.points_at_stake,
        "open_poam_count": brief.open_poam_count,
        "poam_overdue_count": brief.poam_overdue_count,
        "families_with_gaps": brief.families_with_gaps,
        "stale_evidence_count": brief.stale_evidence_count,
        "solution_hints": brief.solution_hints,
        "cost_framework_note": brief.cost_framework_note,
        "generated_date": brief.generated_date,
    }
