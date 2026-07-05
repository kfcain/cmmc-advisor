# Printer and MFP Baselines

> Source: NIST SP 800-171 Rev 2 (MP, SC, AC, PE); CMMC scoping guidance
> (contractor risk managed assets); FedRAMP Marketplace (Canon, Xerox MPS packages);
> PaperCut MF/Hive product documentation (customer-hosted; no FedRAMP package)

## Scoping

Printers rarely store CUI as a system of record, but they are a common **CUI
egress path** and often sit on the same VLAN as CUI workstations.

| Placement | Typical category | Treatment |
|-----------|------------------|-----------|
| CUI VLAN, CUI print permitted | CUI or CRM | Full MP + AC controls; no guest access |
| Same network as CUI, CUI print prohibited | Contractor risk managed | Document risk controls; block routes |
| VDI-only, redirection disabled | Out of scope for local home printer | Session policy evidence |
| Secure print release in enclave | CUI | Queue encryption, badge release |

See `../endpoints/remote-work.md` for VDI printer redirection.

## FedRAMP managed print services (Canon, Xerox)

When the **print services management plane** is SaaS and touches CUI job metadata,
use a Rev 5 Moderate (Class C) Marketplace package:

| Vendor | Package ID | Notes |
|--------|------------|-------|
| **Canon Office Cloud Managed Print Services** | FR1923039219 | Rev5 Moderate; fleet/usage plane |
| **Xerox Managed Print Services for US Government** | FR1730334049 | Rev5 Moderate; Gov MPS boundary |

FedRAMP covers the **vendor cloud**, not automatic compliance of every device.
Document which MFPs are under MPS vs local print. Full catalog:
`../security-operations/dib-fedramp-security-tools.md` (Managed print section).

## PaperCut MF / Hive (on-prem or customer-hosted)

**PaperCut** has **no FedRAMP Marketplace listing** at last export. It is widely
used as a **print release and quota layer** in front of Canon, Xerox, HP, and
other MFPs. Compliance is **OSC-operated**:

1. Host PaperCut on a hardened print server (CIS benchmark, patching, MFA on admin).
2. Block VDI/home USB print paths that bypass PaperCut when CUI hardcopy is prohibited.
3. Export job logs and secure-release configuration for MP.L2-3.8.x evidence.
4. Do not cite FedRAMP for PaperCut; cite configuration and audit exports.

Hosted PaperCut offerings run in the **vendor's cloud** unless you self-host;
treat non-FedRAMP hosted PaperCut like any other non-authorized SaaS touching CUI
metadata (generally avoid for CUI, or keep CUI print off that path).

## Baseline expectations

1. **Inventory:** every MFP with IP, VLAN, firmware version, and whether CUI
   printing is authorized.
2. **Network:** no flat routing from guest Wi-Fi to printer management interface;
   admin UI not internet-exposed.
3. **Authentication:** pull print or AD-integrated print where CUI hardcopy is
   required; disable open file shares on MFP scan-to-folder unless encrypted
   and access-controlled.
4. **Hardcopy:** MP.L2-3.8.3 cover sheets, controlled pickup, shred bins for
   CUI misprints.
5. **Firmware:** MA.L2-3.7.6 patch cadence for devices on CUI network segments.
6. **Logging:** print audit if available; tie to AU correlation where feasible.

## Evidence to collect

- Network diagram showing printer segment and ACLs
- Print server or Universal Print policy export
- MFP admin password policy and last firmware update record
- Sample secure-release configuration
- CRM risk memo if printer shares a subnet with CUI but CUI print is blocked

## Program data

```yaml
contractor_risk_managed:
  - name: HP MFP Floor-2
    baseline_profile: printer-mfp
    location: Building A, CUI adjacent VLAN
    baseline_validation:
      validated: "2026-06-15"
      cui_print_allowed: false
      controls: [vlan_acl, admin_mfa, no_scan_to_email]
```

## Common mistakes

- "We don't print CUI" while VDI allows redirection to home USB printers
- Unpatched MFP firmware on CUI VLAN (assessor scans management port)
- Scan-to-email on MFP as shadow IT file transfer
