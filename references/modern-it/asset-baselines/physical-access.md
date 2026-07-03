# Physical Access: Badges, Readers, Keys, and Evidence

> Source: NIST SP 800-171 Rev 2 Section 3.10; CMMC Assessment Guide;
> FIPS 201 (PIV) where applicable

## Assets in scope

Badge readers, door controllers, PIV/CAC readers, key boxes, visitor management
kiosks, and CCTV covering CUI areas are **security protection** or **CUI
adjacent** assets. They implement PE.L2-3.10.1 through 3.10.5 and support
PE.L2-3.10.6 for alternate sites.

Cross-domain: PS (personnel eligibility), IA (badge-to-account binding), MP
(hardcopy at reception).

## Baseline expectations

### PE.L2-3.10.1 / 3.10.5 (access limit and devices)

- Named access list reconciled with HR at least quarterly
- Badge issuance and revocation within defined SLA (same day termination)
- Server/network room controlled by separate credential from general office
- Key control log for mechanical keys; dual control for master keys

### PE.L2-3.10.3 / 3.10.4 (visitors and logs)

- Visitor escort procedure for CUI areas
- Retained access logs (badge reads) with timestamp and door ID
- Export sample covering assessment period

### Badge readers and API evidence

Modern PACS (Lenel, CCURE, Genetec, Honeywell, etc.) expose REST or ODBC
exports. Collector stub: `physical-access-pacs`.

Collect:

- Door / reader inventory with zone mapping to CUI rooms
- Last 90 days badge event sample (redact PII in assessor package per policy)
- Alarm/event configuration for forced door, propped door
- Photo of visitor log template or VMS export

### Keys and mechanical fallback

- Key register: key ID, door, custodian, issue/return dates
- Re-key event after lost master documented

### Alternate work sites (PE.L2-3.10.6)

Physical controls at home (clean desk, screen privacy, no household members
viewing CUI) documented separately; badge readers apply to **facility** only.
See `../endpoints/remote-work.md`.

## Program data

```yaml
security_protection:
  - name: Lenel OnGuard CUI doors
    vendor: Lenel
    baseline_profile: physical-access-pacs
    baseline_validation:
      validated: "2026-06-18"
      cui_doors: [Server Room, Eng Lab]
      log_retention_days: 365
```

## Common mistakes

- Badge system logs exist but nobody can produce them at assessment
- Shared reception PC logged in as admin for visitor kiosk
- CCTV retained 7 days when IR playbook assumes 90 days
