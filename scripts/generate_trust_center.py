#!/usr/bin/env python3
"""Generate a portable public trust-center page from CMMC program data.

Builds a deny-by-default public payload from the program data file, then
injects it into templates/program-trust-center.html. Unlike the internal
dashboard, this script never embeds assessment-objectives.json, POA&M detail,
evidence paths, or full requirement narratives.

Usage (from repo root):
    python3 scripts/generate_trust_center.py path/to/program-data.yaml -o trust-center.html
    python3 scripts/generate_trust_center.py path/to/program-data.yaml --strict --manifest audit.json
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "templates" / "program-trust-center.html"

ALLOWED_URL_SUFFIXES = (
    "fedramp.gov",
    "marketplace.fedramp.gov",
    "csrc.nist.gov",
    "nist.gov",
    "learn.microsoft.com",
    "aws.amazon.com",
    "cloud.google.com",
    "github.com",
    "github.trust.page",
    "atlassian.com",
    "box.com",
    "servicenow.com",
)

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INTERNAL_PATH_RE = re.compile(
    r"(^|[\s\"'(])(?:\.{0,2}/)?(?:evidence|policies|procedures|vendor-boe|diagrams)/\S+",
    re.IGNORECASE,
)
UNSAFE_URL_RE = re.compile(r"(?i)(javascript:|data:|vbscript:|file:)")


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def embed(value: dict) -> str:
    return json.dumps(value, separators=(",", ":")).replace("</", "<\\/")


def _scrub_text(text: str, strict: bool) -> str:
    if not text:
        return ""
    cleaned = EMAIL_RE.sub("[contact redacted]", text)
    cleaned = IPV4_RE.sub("[network redacted]", cleaned)
    cleaned = INTERNAL_PATH_RE.sub(" ", cleaned)
    if UNSAFE_URL_RE.search(cleaned):
        if strict:
            raise SystemExit(f"Unsafe URL scheme in public text: {cleaned[:120]}")
        cleaned = UNSAFE_URL_RE.sub("", cleaned)
    return cleaned.strip()


def _audit_public_payload(payload: dict[str, Any], strict: bool) -> None:
    blob = json.dumps(payload).lower()
    if "evidence/" in blob or "vendor-boe/" in blob or "diagrams/" in blob:
        raise SystemExit("Public payload contains forbidden internal path markers")
    if strict:
        contact = ((payload.get("trust_center") or {}).get("security_contact") or "")
        scrubbed = json.dumps(payload)
        if contact:
            scrubbed = scrubbed.replace(contact, "")
        if EMAIL_RE.search(scrubbed):
            raise SystemExit("Public payload contains email addresses outside security_contact")
    if strict and IPV4_RE.search(json.dumps(payload)):
        raise SystemExit("Public payload contains IP addresses after redaction")


def _public_contact(value: str | None) -> str | None:
    if not value or not isinstance(value, str):
        return None
    cleaned = value.strip()
    if EMAIL_RE.fullmatch(cleaned):
        return cleaned
    return _scrub_text(cleaned, True) or None


def _public_attestations(attestations: list | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    allowed = {
        "framework",
        "level",
        "status",
        "status_date",
        "affirmation_current",
        "affirmation_date",
    }
    for item in attestations or []:
        if not isinstance(item, dict):
            continue
        row = {
            key: (
                _scrub_text(str(item[key]), True)
                if key != "affirmation_current" and isinstance(item.get(key), str)
                else item.get(key)
            )
            for key in allowed
            if key in item
        }
        rows.append(row)
    return rows


def _public_url(url: str, strict: bool) -> str | None:
    if not url or not isinstance(url, str):
        return None
    if UNSAFE_URL_RE.search(url):
        if strict:
            raise SystemExit(f"Unsafe URL rejected: {url}")
        return None
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return None
    host = (parsed.hostname or "").lower()
    if not any(host == suffix or host.endswith("." + suffix) for suffix in ALLOWED_URL_SUFFIXES):
        return None
    return url


def _public_roles(roles: dict | None) -> dict[str, Any]:
    public: dict[str, Any] = {}
    for slug, role in (roles or {}).items():
        if not isinstance(role, dict):
            continue
        entry: dict[str, Any] = {
            "title": _scrub_text(
                role.get("title") or slug.replace("_", " ").title(),
                True,
            )
        }
        resp = role.get("responsibilities")
        if isinstance(resp, list):
            entry["responsibilities"] = [_scrub_text(str(r), True) for r in resp[:5]]
        public[slug] = entry
    return public


def _public_policies(policies: list | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pol in policies or []:
        if not isinstance(pol, dict):
            continue
        rows.append(
            {
                "id": pol.get("id"),
                "title": pol.get("title"),
                "version": pol.get("version"),
                "reviewed": pol.get("reviewed"),
            }
        )
    return rows


def _public_inheritance(sources: list | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for src in sources or []:
        if not isinstance(src, dict):
            continue
        rows.append(
            {
                "id": src.get("id"),
                "provider": src.get("provider"),
                "cso": src.get("cso"),
                "fedramp_status": src.get("fedramp_status"),
                "crm_document": src.get("crm_document"),
                "verified": src.get("verified"),
            }
        )
    return rows


def _public_cmvp(certs: list | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cert in certs or []:
        if not isinstance(cert, dict):
            continue
        policy_url = _public_url(cert.get("security_policy", ""), strict=False)
        rows.append(
            {
                "certificate": cert.get("certificate"),
                "vendor": cert.get("vendor"),
                "module": cert.get("module"),
                "standard": cert.get("standard"),
                "status": cert.get("status"),
                "sunset": cert.get("sunset"),
                "security_policy": policy_url,
            }
        )
    return rows


def build_public_payload(program: dict, strict: bool) -> dict[str, Any]:
    org = program.get("organization") or {}
    assessment = program.get("assessment") or {}
    trust = program.get("trust_center") or {}

    payload: dict[str, Any] = {
        "generated_for": "public_trust_center",
        "organization": {
            "name": org.get("name"),
            "system_name": org.get("system_name"),
            "revision": org.get("revision"),
            "date": org.get("date"),
            "purpose": _scrub_text(org.get("purpose") or "", strict),
            "scope_narrative": _scrub_text(org.get("scope_narrative") or "", strict),
            "environment_narrative": _scrub_text(org.get("environment_narrative") or "", strict),
            "roles": _public_roles(org.get("roles")),
        },
        "assessment": {
            "level": assessment.get("level"),
        },
        "trust_center": {
            "published": trust.get("published", True),
            "last_reviewed": trust.get("last_reviewed") or org.get("date"),
            "security_contact": _public_contact(trust.get("security_contact")),
            "disclaimer": _scrub_text(
                trust.get("disclaimer")
                or "This page summarizes security posture for customers and partners. "
                "It is not a CMMC certification or FedRAMP authorization.",
                True,
            ),
            "attestations": _public_attestations(trust.get("attestations")),
            "public_documents": [],
        },
        "policies": _public_policies(program.get("policies")),
        "inheritance_sources": _public_inheritance(program.get("inheritance_sources")),
        "cmvp_certificates": _public_cmvp(program.get("cmvp_certificates")),
    }

    for doc in trust.get("public_documents") or []:
        if not isinstance(doc, dict):
            continue
        url = _public_url(doc.get("url", ""), strict)
        if url:
            payload["trust_center"]["public_documents"].append(
                {
                    "title": doc.get("title"),
                    "type": doc.get("type"),
                    "url": url,
                    "updated": doc.get("updated"),
                }
            )

    if strict:
        forbidden_top = {
            "requirements",
            "topology",
            "assets",
            "hardware_software",
            "conditional_status_date",
            "diagrams",
        }
        leaked = forbidden_top.intersection(payload.keys())
        if leaked:
            raise SystemExit(f"Public payload leak: forbidden keys present: {sorted(leaked)}")

    _audit_public_payload(payload, strict)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a public trust-center HTML page")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("trust-center.html"))
    ap.add_argument("--strict", action="store_true", default=True)
    ap.add_argument("--no-strict", action="store_false", dest="strict")
    ap.add_argument("--manifest", type=Path, default=None, help="Write redaction manifest JSON")
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data must parse to a mapping")

    source_hash = hashlib.sha256(
        json.dumps(program, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]

    public_payload = build_public_payload(program, strict=args.strict)
    public_payload["meta"] = {
        "generated_at": date.today().isoformat(),
        "source_hash": source_hash,
    }

    if not TEMPLATE.exists():
        sys.exit(f"Missing template: {TEMPLATE}")

    html_out = TEMPLATE.read_text(encoding="utf-8")
    html_out = html_out.replace("__PUBLIC_DATA__", embed(public_payload))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")

    if args.manifest:
        manifest = {
            "generated_at": public_payload["meta"]["generated_at"],
            "source_hash": source_hash,
            "redacted_sections": [
                "requirements",
                "topology",
                "assets",
                "hardware_software",
                "conditional_status_date",
                "diagrams",
                "organization.roles PII",
                "policies internal paths",
                "inheritance_sources boe_reference",
            ],
            "included_sections": list(public_payload.keys()),
        }
        args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.manifest}")

    org_name = html.escape(str((public_payload.get("organization") or {}).get("name", "Trust Center")))
    print(f"Wrote {args.out} (public trust center for {org_name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
