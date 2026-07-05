# GCC High Implementation Workbook: CMMC Objective Mapping

> Source: NIST SP 800-171A assessment procedures; CMMC Assessment Guide Level 2;
> references/modern-it/productivity/microsoft-365-gcc.md;
> references/data/gcch-workbook-manifest.json

## Overview

Practitioner GCC High rollouts follow a phased sequence: **scope the
boundary**, **secure identity**, **manage devices**, **protect data**, then
**operate monitoring and audit readiness**. Common phased GCC High rollout
guides organize Microsoft 365 GCC High configuration around that sequence.
This file maps those workstreams to CMMC
Level 2 **requirements** and **assessment objectives (AOs)** so advisors can
tie Entra, Intune, Purview, Defender, and Sentinel work to assessor evidence.

Machine-readable index: `references/data/gcch-workbook-manifest.json`.

Read tenancy selection and FedRAMP inheritance first in
`references/modern-it/productivity/microsoft-365-gcc.md`. Read CRM workflow
in `references/grc/inherited-controls-mapping.md`.

**Graph and Exchange endpoints.** GCC High automation uses US Gov endpoints:
`Connect-MgGraph -Environment USGov` and
`Connect-ExchangeOnline -ExchangeEnvironmentName O365USGovGCCHigh`. Wrong
environment strings are a common assessment finding (configuration applied
to the wrong tenant or wrong cloud instance).

---

## Phase 1: Scoping (workbook sections 2–8)

**Workbook intent:** Identify where CUI enters, moves, rests, and exits before
Conditional Access, Intune, or DLP can be targeted.

| Workbook workstream | GCC High / M365 mechanism | Primary requirements | Key AOs to examine |
|---------------------|---------------------------|--------------------|--------------------|
| CUI data flows and DFD | Exchange, SharePoint, Teams, ERP/PDM paths; tenant boundary export | AC.L2-3.1.3, SC.L2-3.13.1 | 3.1.3[a–d] CUI flow authorized/limitation; 3.13.1[a–b] boundary protection |
| People, technology, processes | Asset categories (CUI, SPA, CRMA, out-of-scope) | CM.L2-3.4.1, CM.L2-3.4.2 | 3.4.1[a–b] baseline configurations and inventories |
| External service providers | ESP/MSP access paths, CRM/BoE due diligence | AC.L2-3.1.3, MP.L2-3.8.1 | 3.1.3 outbound paths; vendor flowdown in SSP |
| Contractual / LOB intake | Controlled ingestion channels vs shadow IT | AC.L2-3.1.3, MP.L2-3.8.3 | 3.8.3[a] sanitization before release from controlled areas |
| Shared / conglomerate tenants | Ring-fencing CUI within a shared GCC High tenant | AC.L2-3.1.3, SC.L2-3.13.5 | 3.13.5 public-access separation |
| Migrate to GCC High | Separate tenancy; no commercial overlay | CM.L2-3.4.1 | Baseline for new enclave architecture |

**Evidence snippets (workbook patterns):**

- `TenantBoundary` export → SSP system identification, scoping narrative
- `GroupsUsers` (CUI-Users, CUI-Admins, CUI-AVD-Users) → AC.L2-3.1.1 account inventory
- `MailboxForwarding` review → AC.L2-3.1.3 unauthorized outbound CUI paths

Run `scripts/generate_diagrams.py` after updating program-data `topology`.
Validate forwarding and guest sharing against the DFD before assessment.

---

## Phase 2: Identity (workbook sections 9–18)

**Workbook intent:** Treat Entra ID as the control plane; CA and MFA before
device or data enforcement.

| Workbook topic | GCC High mechanism | Primary requirements | Key AOs |
|----------------|-------------------|----------------------|---------|
| Sovereign cloud / endpoints | USGov Graph, `.onmicrosoft.us`, GCC High licensing | CM.L2-3.4.1 | Documented architecture baseline |
| Identity foundation | User/group model, admin roles, break-glass | AC.L2-3.1.1, AC.L2-3.1.5 | 3.1.1[a–c] authorized users/processes/devices; 3.1.5[a] least privilege |
| Phishing-resistant MFA | FIDO2/WHfB, CA auth strength | IA.L2-3.5.3, IA.L2-3.5.4 | 3.5.3[a–d] MFA; 3.5.4 replay resistance where applicable |
| Directory sync | Entra Connect to on-prem (hybrid path) | IA.L2-3.5.1, IA.L2-3.5.2 | 3.5.1[a] identification; 3.5.2[a] authentication |
| Entra security settings | Legacy auth block, guest settings | AC.L2-3.1.8, AC.L2-3.1.7 | 3.1.8[a] unsuccessful logon handling; 3.1.7[a] privileged functions |
| Identity governance | Access reviews, PIM, lifecycle | AC.L2-3.1.5, PS.L2-3.9.2 | 3.1.5; 3.9.2 transfer/termination |
| Cross-tenant collaboration | B2B, cross-tenant access, guest controls | AC.L2-3.1.3, SC.L2-3.13.1 | 3.1.3 external connection controls |
| Conditional Access | Device compliance + MFA gates for CUI groups | AC.L2-3.1.1, IA.L2-3.5.3, AC.L2-3.1.18 | 3.1.18[a] mobile device connection control |

**Assessor evidence:** CA policy exports (report-only then enforced), auth
method registration reports, PIM activation logs, guest access reviews,
break-glass test records. Collectors: `entra-signins`, `entra-conditional-access`
(see `references/modern-it/security-operations/microsoft-graph-evidence.md`).

---

## Phase 3: Devices (workbook sections 19–42)

**Workbook intent:** Intune-managed endpoints and AVD session hosts as CUI
access paths; compliance gates before CA allows access.

| Workbook topic | Mechanism | Primary requirements | Key AOs |
|----------------|-----------|----------------------|---------|
| Device architecture / Autopilot | Entra Join, hybrid, rings | CM.L2-3.4.1, CM.L2-3.4.2 | 3.4.1[a–b]; 3.4.2[a] configuration enforcement |
| AVD (sovereign / enclave) | Session hosts in GCC High, network isolation | AC.L2-3.1.18, SC.L2-3.13.1 | 3.1.18 remote access; 3.13.1 boundary |
| Open Intune Baseline | Layered security/compliance profiles | CM.L2-3.4.6, CM.L2-3.4.7 | 3.4.6 least functionality; 3.4.7 ports/protocols |
| BitLocker / FIPS mode | Encryption at rest, CMVP-validated modules | SC.L2-3.13.11, MP.L2-3.8.1 | 3.13.11[a] FIPS cryptography; run `check_cmvp.py` |
| Defender for Endpoint | ASR, AV, EDR onboarding | SI.L2-3.14.2, SI.L2-3.14.4, SI.L2-3.14.5 | 3.14.2[a–c] malicious code protection |
| LAPS / local admin | Least privilege on endpoints | AC.L2-3.1.5 | 3.1.5[a] |
| Device hygiene / lifecycle | Stale device cleanup, compliance reporting | CM.L2-3.4.1, SI.L2-3.14.6 | 3.14.6[a] monitoring |
| Intune audit evidence | Policy assignment and compliance exports | CM.L2-3.4.2 | 3.4.2[a] enforcement evidence |

**Evidence snippets:** `InventoryDevices`, `IntunePolicies` CSV exports;
Defender onboarding status; BitLocker recovery key escrow proof.

---

## Phase 4: Data protection (workbook sections 43–57)

**Workbook intent:** Purview labels, DLP, and governance for CUI at rest and in
motion across Exchange, SharePoint, OneDrive, Teams.

| Workbook topic | Mechanism | Primary requirements | Key AOs |
|----------------|-----------|----------------------|---------|
| Protection architecture | Label + DLP + encryption stack | MP.L2-3.8.1, MP.L2-3.8.2, SC.L2-3.13.16 | 3.8.1[a] media marking; 3.8.2[a] access restriction |
| Asset inventory (data) | Purview asset discovery | CM.L2-3.4.1 | 3.4.1[b] inventory |
| Sensitivity labels | Auto-labeling, encryption | MP.L2-3.8.1, MP.L2-3.8.2 | 3.8.1–3.8.2 |
| DLP policies | Block exfil to personal cloud, unapproved domains | AC.L2-3.1.3, MP.L2-3.8.2 | 3.1.3 flow control |
| Structured data governance | SharePoint site architecture for CUI | AC.L2-3.1.3, SC.L2-3.13.8 | 3.13.8 transmission confidentiality |
| Insider risk / IR hooks | Purview insider risk, case routing | IR.L2-3.6.1, SI.L2-3.14.3 | 3.6.1[a] incident handling capability |
| Secure collaboration | Guest sharing restrictions, Teams policies | AC.L2-3.1.22, AC.L2-3.1.3 | 3.1.22 public content control |

**Assessor evidence:** Label policy exports, DLP hit summaries (sample redacted),
auto-labeling simulation results, eDiscovery hold configs where used for legal
hold (not a substitute for MP controls).

---

## Phase 5: M365 security and audit readiness (workbook sections 58–61)

**Workbook intent:** Threat defense, centralized logging, assessor-ready packages.

| Workbook topic | Mechanism | Primary requirements | Key AOs |
|----------------|-----------|----------------------|---------|
| Threat defense | Defender for Office 365, anti-phishing | SI.L2-3.14.2, SI.L2-3.14.3 | 3.14.3[a] security alerts |
| SIEM strategy | Microsoft Sentinel, log routing | AU.L2-3.3.5, SI.L2-3.14.6 | 3.3.5[a–c] audit review/correlation; 3.14.6 monitoring |
| Audit readiness | Unified audit log retention, export cadence | AU.L2-3.3.1, AU.L2-3.3.6 | 3.3.1[a] audit events; 3.3.6 reduction/reporting |
| Continuous monitoring | CA.L2-3.12.3 security control monitoring | CA.L2-3.12.3 | 3.12.3[a] monitor controls |

**AU.L2-3.3.5 note:** 5 SPRS points; not POA&M-eligible under 32 CFR 170.21.
Close correlated review gaps before assessment or accept score impact.

Export SPRS diff with `scripts/export_sprs.py`; refresh dashboard Evidence
freshness tab after collector runs.

---

## Workbook appendices (sections 63–88)

| Appendix area | Maps to | Evidence use |
|---------------|---------|--------------|
| Compliance control matrix (§63) | All families | SSP control narrative alignment |
| Intune policy exports (§64–65) | CM, SI, SC | Baseline enforcement proof |
| Defender appendices (§66–70) | SI | EDR/ASR configuration |
| BitLocker, LAPS, Firewall (§72–74) | SC, AC, CM | Endpoint hardening |
| Audit/event logging (§76) | AU | Local and forwarded logs |
| AVD runbooks (§84–87) | AC, SC | Remote CUI access architecture |
| Licensing matrix (§88) | CM, planning | Feature availability for GCC High SKUs |

Treat appendix policy exports as **candidate** baselines. The organization must
document deviations, ownership, and validation tests per CM.L2-3.4.1 and
CM.L2-3.4.3 change control.

---

## Advisor workflow

1. Confirm GCC High (not GCC commercial) for DFARS-scope CUI per
   `microsoft-365-gcc.md`.
2. Walk workbook phases in order; do not skip scoping to Intune baselines.
3. For each configuration change, record: requirement IDs, objective letters,
   evidence path, owner, and validation test.
4. Update program-data.yaml conformity **only after** ISSM review; use
   `inheritance` blocks with CRM row citations for provider shares.
5. Regenerate SSP, dashboard, and diagrams; run `validate_poam.py` before
   conditional status.
6. For IaC repos in the same program, export ControlBot profile:
   `python3 scripts/export_controlbot_profile.py program-data.yaml -o .controlbot/profile.yaml`

---

## Related references

- `references/modern-it/productivity/microsoft-365-gcc.md` (capability depth)
- `references/modern-it/security-operations/microsoft-graph-evidence.md`
- `references/modern-it/endpoints/remote-work.md` (AVD/VDI scoping)
- `references/grc/companion-stack.md` (ControlBot import after IaC review)
- `references/assessment-objectives/{ac,ia,cm,sc,si,au,mp}.md` (full AO lists)
