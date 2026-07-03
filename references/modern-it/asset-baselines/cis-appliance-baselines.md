# CIS and STIG Baselines for Appliances Without FedRAMP

> Source: CIS Benchmarks (cisecurity.org); DISA STIGs (public.cyber.mil); NIST SP 800-171
> Rev 2; CMMC Assessment Guide; vendor hardening guides (Palo Alto, Fortinet, Cisco);
> references/modern-it/asset-baselines/network-firewall-wlan.md

## Overview

Many CMMC assessment scope assets **never appear on the FedRAMP Marketplace**: on-premises
firewalls, switches, WLAN controllers, badge systems, printers, and OT devices. DFARS
7012 FedRAMP rules apply to **cloud service providers**, not your FortiGate or Catalyst
switch.

For these assets, the compliant path is:

1. **Industry baselines**: CIS Benchmarks (where published) or DISA STIGs (where mandated
   or adopted)
2. **Vendor hardening guides**: supported OS/firmware versions only
3. **Asset-baseline chapters** in this repo: scoping, FIPS, evidence collectors
4. **Program data**: `baseline_profile`, `baseline_validation`, topology in SSP

Do not claim FedRAMP inheritance for on-prem appliances. Map practices to **your**
implementation and evidence.

---

## Selection order

| Priority | Source | When to use |
|----------|--------|-------------|
| 1 | **DISA STIG** | US DoD contractor; Windows/RHEL/Network devices with published STIG |
| 2 | **CIS Benchmark** | Vendor/OS has CIS profile (AWS, Azure, Cisco, VMware, etc.) |
| 3 | **Vendor security baseline** | STIG/CIS absent; use vendor "best practice" + CMMC objective mapping |
| 4 | **Compensating controls** | Legacy device cannot meet baseline; document risk acceptance |

Record which baseline you adopted in the SSP system security plan and in `baseline_profile`
on the asset row.

---

## Firewalls and NGFW

See **`network-firewall-wlan.md`** for FIPS scoping (pass-through vs crypto endpoint).

| Baseline element | Evidence |
|------------------|----------|
| Deny-by-default segmentation rules | Policy export (FortiGate/PAN-OS collector stubs) |
| Admin MFA and role separation | Admin audit + IAM narrative |
| FIPS-cc mode **only** where SC.L2-3.13.11 applies | CMVP certificate in program data |
| Firmware support lifecycle | Vendor support contract |

**CIS:** Cisco and some NGFW platforms have CIS-adjacent hardening; map to CM.L2-3.4.x and
SC.L2-3.13.x families.

---

## Network switches and routing

Switches rarely process CUI content; they often appear as **security protection** or
**out-of-scope** pass-through per DoD CMMC FAQ F-Q4 when CUI is encrypted and the switch
provides no SSP-described security function.

| Baseline element | Evidence |
|------------------|----------|
| 802.1X or port security on CUI VLANs | Switch config export |
| Disable unused ports / default VLAN | Config + change ticket |
| Management plane restricted | ACL on management SVI |
| STIG (if Cisco IOS/IOS-XE in scope) | STIG scan or manual checklist |

Document **in-scope vs out-of-scope** per port/VLAN in topology (`generate_diagrams.py`).

---

## WLAN controllers and access points

Full baseline: **`network-firewall-wlan.md`** (WPA3-Enterprise, guest isolation).

| Baseline element | Evidence |
|------------------|----------|
| CUI SSID on dedicated VLAN | Controller SSID map |
| No PSK on CUI WLAN | Config export |
| Rogue AP detection cadence | Controller report |
| Collector | `wlan-controller` stub in on-prem-inspectors |

---

## Physical access (PACS)

See **`physical-access.md`**. FedRAMP does not cover on-prem badge systems.

| Baseline element | Evidence |
|------------------|----------|
| Badge issuance/revocation tied to HR | Access review export |
| Visitor procedures | PE policy + sample logs |
| Collector | `physical-access-pacs` stub |

---

## Printers and MFPs

See **`printers-mfp.md`**. Treat as CUI assets if they store/process CUI print jobs.

---

## OT / industrial

See **`specialized-ot.md`**. CIS Controls IG implementations may apply at program level;
device baselines are vendor-specific.

---

## Mapping baselines to CMMC objectives

1. List asset in program data `topology` with 32 CFR 170.19(c) category.
2. Assign `baseline_profile` from `asset-baseline-manifest.json`.
3. Run `python3 scripts/validate_asset_baselines.py program-data.yaml`.
4. Link examine/interview evidence per `references/evidence-collection.md`.

For cloud-adjacent tools, prefer **FedRAMP Marketplace** selection per
`references/grc/solution-selection.md` before defaulting to CIS-only posture.

---

## Anti-patterns

- **FedRAMP sticker on firewall.** Marketplace authorization does not apply to your
  on-prem NGFW.
- **CIS checklist without evidence.** Assessors examine configuration exports, not intent.
- **Fleet-wide FIPS-cc** on segmentation-only devices (see network-firewall-wlan.md).
