# Printer and MFP Baselines

> Source: NIST SP 800-171 Rev 2 (MP, SC, AC, PE); CMMC scoping guidance
> (contractor risk managed assets)

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
