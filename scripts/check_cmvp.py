#!/usr/bin/env python3
"""Validate FIPS claims against NIST CMVP data.

Backs SC.L2-3.13.11 (and every other FIPS-validated cryptography claim)
with live certificate state. Uses the NIST-CMVP-API project, a weekly
auto-updated static JSON mirror of the official CMVP registry, and prints
the official csrc.nist.gov certificate URL for every result.

The mirror is unofficial. Re-verify at csrc.nist.gov before citing a
certificate in an SSP or assessment.

Usage (from repo root):
    # Check every cmvp_certificates entry in a program data file
    python3 scripts/check_cmvp.py verify path/to/program-data.yaml

    # Also write verified status/sunset/policy URL back with a dated stamp
    python3 scripts/check_cmvp.py verify path/to/program-data.yaml --update

    # Find candidate certificates for in-scope crypto
    python3 scripts/check_cmvp.py find "bitlocker"
    python3 scripts/check_cmvp.py find "openssl" --vendor "OpenSSL"
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

SOURCES = [
    "https://raw.githubusercontent.com/ethanolivertroy/NIST-CMVP-API/main/api",
    "https://raw.githubusercontent.com/hackIDLE/nist-cmvp-api/main/api",
    "https://ethanolivertroy.github.io/NIST-CMVP-API/api",
    "https://hackidle.github.io/nist-cmvp-api/api",
]
OFFICIAL = "https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/{n}"


def fetch_json(path: str, base: str | None = None, timeout: int = 20):
    bases = [base] if base else SOURCES
    last_err = None
    for b in bases:
        url = f"{b}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8")), b
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            last_err = f"{url}: {e}"
    sys.exit(
        "could not reach the CMVP mirror on any source. Offline? Check "
        f"connectivity or pass --source. Last error: {last_err}"
    )


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def parse_sunset(s: str | None):
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def verify(args) -> int:
    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data must parse to a mapping (YAML or JSON object)")
    certs = program.get("cmvp_certificates") or []
    if not certs:
        print("no cmvp_certificates entries in the program data file; nothing to verify")
        return 0

    today = date.today()
    problems = 0
    for entry in certs:
        n = str(entry.get("certificate", "")).strip()
        if not n:
            print("SKIP  entry with no certificate number")
            problems += 1
            continue
        try:
            data, used = fetch_json(f"certificates/{n}.json", args.source)
        except SystemExit:
            raise
        cert = data.get("certificate", {})
        if not cert:
            print(f"FAIL  #{n}: no record found in the CMVP dataset")
            problems += 1
            continue
        status = cert.get("status", "Unknown")
        standard = cert.get("standard", "")
        module = cert.get("module_name", "")
        sunset = cert.get("sunset_date", "")
        sunset_d = parse_sunset(sunset)
        flags = []
        if status.lower() != "active":
            flags.append(f"status is {status}, not Active")
        if sunset_d and sunset_d <= today:
            flags.append(f"sunset date {sunset} has passed")
        elif sunset_d and (sunset_d - today).days <= 365:
            flags.append(f"sunset {sunset} is within a year; plan the successor module")
        claimed = (entry.get("module") or "").lower()
        if claimed and module and claimed not in module.lower() and module.lower() not in claimed:
            flags.append(f"module name mismatch: data file says '{entry.get('module')}', CMVP says '{module}'")
        verdict = "WARN" if flags else "OK"
        if any("not Active" in f or "has passed" in f or "mismatch" in f for f in flags):
            verdict = "FAIL"
            problems += 1
        print(f"{verdict:5s} #{n}: {module or entry.get('module', '')} | {standard} | {status}"
              f"{' | sunset ' + sunset if sunset else ''}")
        for f in flags:
            print(f"      - {f}")
        print(f"      official record: {OFFICIAL.format(n=n)}")
        if args.update:
            entry["status"] = status
            entry["standard"] = standard or entry.get("standard")
            if sunset:
                entry["sunset"] = sunset
            if cert.get("security_policy_url"):
                entry["security_policy_url"] = cert["security_policy_url"]
            entry["verified"] = today.isoformat() + " via NIST-CMVP-API mirror; re-verify at csrc.nist.gov"

    if args.update:
        out = args.program_data
        if out.suffix.lower() in (".yaml", ".yml"):
            import yaml
            out.write_text(yaml.safe_dump(program, sort_keys=False, allow_unicode=True), encoding="utf-8")
        else:
            out.write_text(json.dumps(program, indent=2), encoding="utf-8")
        print(f"\nwrote verification results back to {out}")

    print(f"\n{len(certs)} certificate(s) checked, {problems} problem(s). "
          "Re-verify at csrc.nist.gov before citing in an SSP.")
    return 1 if problems else 0


def find(args) -> int:
    data, used = fetch_json("modules.json", args.source)
    modules = data.get("modules", data if isinstance(data, list) else [])
    q = args.query.lower()
    vendor_q = (args.vendor or "").lower()
    hits = []
    for m in modules:
        name = (m.get("Module Name") or m.get("module_name") or "")
        vendor = (m.get("Vendor Name") or m.get("vendor_name") or "")
        if q in name.lower() or q in vendor.lower():
            if vendor_q and vendor_q not in vendor.lower():
                continue
            hits.append(m)
    if not hits:
        print(f"no active validated modules match '{args.query}'. Try a shorter keyword, "
              "or check historical-modules for retired validations.")
        return 1
    for m in hits[: args.limit]:
        n = m.get("Certificate Number") or m.get("certificate_number")
        print(f"#{n}: {m.get('Module Name') or m.get('module_name')} | "
              f"{m.get('Vendor Name') or m.get('vendor_name')} | "
              f"{m.get('standard', '')} | sunset {m.get('sunset_date', 'n/a')}")
        print(f"    official record: {OFFICIAL.format(n=n)}")
    if len(hits) > args.limit:
        print(f"({len(hits) - args.limit} more matches; raise --limit)")
    print("\nAdd chosen certificates to cmvp_certificates in the program data file, "
          "then run verify. Re-verify at csrc.nist.gov before citing in an SSP.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate FIPS claims against CMVP data")
    ap.add_argument("--source", help="override API base URL")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify", help="check cmvp_certificates in a program data file")
    v.add_argument("program_data", type=Path)
    v.add_argument("--update", action="store_true", help="write verified fields back with a dated stamp")
    f = sub.add_parser("find", help="search validated modules by keyword")
    f.add_argument("query")
    f.add_argument("--vendor", help="also require this vendor substring")
    f.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()
    return verify(args) if args.cmd == "verify" else find(args)


if __name__ == "__main__":
    sys.exit(main())
