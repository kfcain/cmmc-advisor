# Solution Selection: FedRAMP Marketplace, 20x Classes, and On-Prem Fallbacks

> Source: FedRAMP Marketplace (marketplace.fedramp.gov); FedRAMP Consolidated Rules
> 2026 (fedramp.gov/preview/2026/certification/); FedRAMP 20x program (fedramp.gov/20x/);
> DFARS 252.204-7012(b)(2)(ii)(D); DoD CIO FedRAMP Moderate Equivalency Memorandum
> (December 21, 2023); 32 CFR Part 170; CIS Benchmarks (cisecurity.org); DISA STIGs
> (public.cyber.mil)

## Overview

When gaps drive tool or cloud purchases, contractors need a repeatable selection method:

1. **Cloud SaaS touching CUI** → FedRAMP **Rev 5 Moderate** authorization **or**
   **FedRAMP 20x Class C (Moderate impact)** with an active Marketplace listing.
2. **Mission-critical / high-impact cloud** → **Rev 5 Class D (High)** path (20x Class D
   pilot timeline per FedRAMP program announcements; verify current fedramp.gov).
3. **ITAR-controlled technical data** → FedRAMP High / IL5-class posture **plus**
   contractor-side US-person and export-control overlays (ITAR is not satisfied by
   FedRAMP alone). GCC High, AWS GovCloud IL5 patterns: productivity and cloud-platform
   references.
4. **On-prem appliances** (firewall, switch, WLAN, PACS) → **no FedRAMP**; use **CIS
   Benchmarks**, **DISA STIGs**, vendor hardening guides, and asset-baseline chapters here.

Pair with `references/fedramp-marketplace-guide.md` for search patterns and category
short-lists, and `scripts/recommend_solutions.py` for gap-family hints from program data.

**No product endorsement.** Gap hints and Marketplace examples are **decision
aids**, not endorsements. The skill does not recommend or prefer any vendor;
contractors remain responsible for fit, authorization scope, and procurement.

---

## FedRAMP Rev 5 vs 20x Class C / Class D

| Path | Impact | CMMC contractor use | Marketplace signal |
|------|--------|---------------------|-------------------|
| **Rev 5 Agency/JAB authorization** | Low / Moderate / High | **Primary path today** for DFARS 7012 CSPs | Authorized at Moderate or High |
| **FedRAMP 20x Class C** | Moderate (enterprise services) | Accept when **Active** listing shows Class C Moderate | Class C certification label |
| **FedRAMP 20x Class A/B** | LI-SaaS / agency-specific | Usually not the CUI enclave core; verify scope | Class label on package |
| **Rev 5 Class D (High)** | High | High-impact CUI, many IL5-class workloads | High authorization |
| **20x Class D** | High | **Not generally available on 20x path yet**; Rev5 Class D remains the High path per Consolidated Rules 2026 preview | Watch fedramp.gov Phase 4 announcements |

**Practical rule for ISSMs:** For a CSP storing, processing, or transmitting CUI, require
**Moderate-equivalent** minimum: Rev 5 Moderate **or** 20x **Class C Moderate** with CRM
you can map to CMMC objectives. For workloads requiring **High** reciprocity at the cloud
plane, require **Rev 5 High (Class D)** until your vendor documents an accepted 20x High path.

Regenerate snapshots before citing:

```bash
python3 scripts/build_fedramp_snapshot.py
python3 scripts/build_frmr_snapshot.py
```

---

## No CMMC reciprocity with FedRAMP 20x (today)

**CMMC certification** and **FedRAMP authorization** are separate programs. No DoD rule
currently auto-awards CMMC status from a FedRAMP 20x Class C or KSI package.

What you **can** do today:

- **Inherit** provider-implemented controls via **CRM Appendix J** rows mapped to CMMC
  assessment objectives (`references/grc/inherited-controls-mapping.md`).
- **Reduce duplicate evidence** when CRM rows and your monitors align (Vanta/Drata +
  `import_grc_snapshot.py`).
- **Track 20x vendors** with `references/fedramp-20x-ksi-due-diligence.md` for due
  diligence, not as a substitute for C3PAO assessment.

FedRAMP program materials describe **future reciprocity refinement** (Phase 4 goals). Until
DoD publishes binding reciprocity in acquisition or assessment policy, treat 20x as a
**vendor authorization modernization**, not a CMMC pass-through.

---

## ITAR and Class D

**ITAR** (22 CFR Parts 120-130) is a separate export-control regime from CMMC and FedRAMP.

- **FedRAMP High / Class D** addresses **high-impact cloud authorization**, not automatic
  ITAR compliance.
- **ITAR overlays** (US-person access, technical data handling, contractual commitments)
  appear in **GCC High**, **Google Assured Controls Plus ITAR addendum**, and contractor
  policies. See productivity and cloud-platform references.
- Do **not** route ITAR technical data through **Moderate-only** or non-authorized SaaS
  because a monitor passes in Vanta. Class C Moderate is for **Moderate-impact CUI**, not
  a substitute for export-control counsel on ITAR scope.

When the user asks "ITAR only for Class D," read that as: **high-sensitivity and many
ITAR-adjacent cloud workloads require High/IL5-class cloud offerings (Rev5 Class D path),
not Moderate/Class C alone**, plus contractor personnel rules.

---

## Marketplace workflow (with program context)

1. Run **`python3 scripts/recommend_solutions.py program-data.yaml --format md`** from
   gap families.
2. Open **`references/fedramp-marketplace-guide.md`** for the category short-list.
3. Search **marketplace.fedramp.gov** with **Authorized** filter and exact product name.
4. Record package ID, impact level, and **Rev 5 vs 20x class** in `inheritance_sources`
   or vendor notes in program data.
5. Obtain **CRM** under contract; map rows before marking objectives inherited.
6. For **on-prem gaps** in SC/PE/CM families, pivot to CIS/STIG chapter below.

Executive view: **`python3 scripts/generate_executive_brief.py program-data.yaml`**
 surfaces top gaps, points at stake, and these hints in one HTML file for leadership.

---

## When FedRAMP does not exist (appliances and OT)

Use **`references/modern-it/asset-baselines/cis-appliance-baselines.md`** for:

- Firewalls / NGFW
- Network switches and routing
- WLAN controllers
- Physical access (PACS)
- Printers, OT, industrial devices

Document **compensating controls** and **evidence exports** in program data; do not invent
FedRAMP inheritance for bare metal.

---

## GRC platform note

Vanta, Drata, Secureframe, and Hyperproof may **monitor** your environment without being
the CUI store. If the **RMM/agent or GRC SaaS** can reach CUI systems or hold CUI
narratives, apply the same **Moderate / Class C** floor as any other CSP
(`references/modern-it/asset-baselines/msp-rmm-tools.md`).

Multi-MCP sync: `references/grc/grc-platform-mcp-bridge.md`.

---

## Related files

- `references/fedramp-marketplace-guide.md`: search and categories
- `references/fedramp-gap.md`: DFARS 7012 and inheritance narrative
- `references/fedramp-20x-ksi-due-diligence.md`: KSI/trust center due diligence
- `references/contractor-profiles.md`: cost framework for executive briefs
- `scripts/generate_executive_brief.py`: leadership HTML
- `scripts/generate_trust_center.py`: **public** page (no gaps)
