# FedRAMP 20x, FRMR, and KSI Vendor Due Diligence

> Source: FedRAMP 20x program (fedramp.gov/20x); FedRAMP Consolidated Rules
> 2026 (github.com/FedRAMP/rules); FedRAMP RFC-0006 (Key Security Indicators);
> RFC-0022 (Leveraging External Frameworks); RFC-0024 (Rev 5 Machine-Readable
> Packages); DFARS 252.204-7012(b)(2)(ii)(D); DoD CIO FedRAMP Moderate
> Equivalency Memorandum (December 21, 2023)

## Overview

FedRAMP is moving from narrative SSP packages toward **machine-readable
authorization data** and **Key Security Indicators (KSIs)**: capability-based
outcomes a cloud service provider demonstrates continuously, not only at
initial authorization. CMMC contractors still assess against NIST SP 800-171
objectives; FedRAMP CRMs still speak NIST SP 800-53. Phase 4 adds the public
layer between those worlds.

This file is the practitioner method for reading FRMR/KSI artifacts during
vendor due diligence without treating Marketplace authorization as proof of
KSI automation or trust-center maturity.

**Enabler posture.** When a vendor's public certification data is immature,
map what you can verify today (Marketplace status, CRM, public trust page),
name the gap, and document interim customer-side controls until the vendor
publishes machine-readable certification data.

---

## What Changed in FedRAMP 20x

| Era | Authorization artifact | Contractor reads |
|-----|------------------------|------------------|
| Rev 5 agency path (current majority) | Word/PDF SSP + CRM Appendix J + Marketplace listing | CRM rows mapped via `references/data/800-53-crosswalk.json` |
| FedRAMP 20x (Classes A/B/C pilot) | KSI validation + hosted certification data (trust center/API) | Public trust center + KSI catalog crosswalk to 800-53 |
| Both | Marketplace export for package status | `scripts/build_fedramp_snapshot.py` or `build_frmr_snapshot.py` |

Rev 5 and 20x coexist during transition. A GCC High tenant today is almost
certainly Rev 5 agency path; a new LI-SaaS vendor may be 20x Class A. Read
the Marketplace package metadata before assuming which path applies.

---

## Machine-Readable Sources in This Repo

| Artifact | Generator | Purpose |
|----------|-----------|---------|
| `references/data/frmr-snapshot.json` | `scripts/build_frmr_snapshot.py` | KSI catalog from Consolidated Rules + merged vendor checklist |
| `references/data/frmr-snapshot.manifest.json` | (curated) | Vendor trust-center URLs, KSI due diligence steps |
| `references/data/fedramp-snapshot.json` | `scripts/build_fedramp_snapshot.py` | Live Marketplace authorization fields |
| `references/data/800-53-crosswalk.json` | `scripts/build_800_53_crosswalk.py` | CMMC requirement ↔ 800-53 control mapping |

Regenerate before SSP citation or prime/customer review:

```bash
python3 scripts/build_frmr_snapshot.py
python3 scripts/build_fedramp_snapshot.py
```

Do not scrape fedramp.gov HTML for automation; use the JSON repositories
listed in `SOURCES.md`.

---

## Reading the KSI Catalog

The Consolidated Rules JSON exposes KSIs grouped by theme (IAM, CNA, SVC,
MLA, CMT, PIY, RPL, INR, CED, SCR, and others). Each indicator carries:

- **id** (e.g. `KSI-IAM-ELP`)
- **statement** (capability outcome)
- **controls_800_53** (underlying NIST SP 800-53 Rev 5 controls in OSCAL id form)

**Workflow for CRM inheritance:**

1. Identify the 800-53 controls in the CRM row you are evaluating.
2. Look up those controls in `800-53-crosswalk.json` **control_index** to find
   CMMC requirements and assessment objectives.
3. Optionally cross-reference KSIs that cite the same 800-53 controls in
   `frmr-snapshot.json` to understand FedRAMP 20x capability framing.
4. Record inherited/shared conformity in program data with the CRM row citation
   per `references/grc/inherited-controls-mapping.md`.

KSIs do not replace CRM rows for CMMC. They explain what FedRAMP 20x expects
CSPs to demonstrate over time.

**CMMC reciprocity.** FedRAMP authorization (Rev 5 or 20x Class C/D) does **not**
currently grant CMMC certification or eliminate C3PAO assessment. Inheritance flows
through **CRM rows** mapped to assessment objectives only. FedRAMP program Phase 4
may refine reciprocity language; until DoD acquisition policy changes, document
customer-side controls and CRM citations per `references/grc/solution-selection.md`.

---

## Trust Center and Certification Data Sharing

FedRAMP 20x expects authorized services to host **certification data** on a
public trust center with programmatic access (replacing legacy secure-repository
models for many artifacts). Publicly verifiable checks a contractor can run
today:

1. **Marketplace link** resolves and shows Active authorization for the exact
   package ID (not a similarly named product).
2. **Public trust center URL** loads and documents authorization scope.
3. **Programmatic access** documentation exists (API, open data feed, or stated
   roadmap with date).
4. **CRM / customer responsibility matrix** available under contract or
   standard customer channel (not always on the public web).
5. **Change notification** commitment documented (SCN process or vendor equivalent).

The manifest field `ksi_due_diligence` in `frmr-snapshot.manifest.json` lists
corpus-curated checklist steps per vendor. These are **public verification
steps**, not proof of private KSI pass/fail.

When a vendor publishes only PDF compliance letters and no machine-readable
feed, note the gap in your vendor file and rely on CRM + Marketplace until
RFC-0024 timelines apply (Rev 5 packages shifting to required machine-readable
submission).

---

## External Framework Mapping (RFC-0022)

Vendors mapping SOC 2, ISO/IEC 27001, or other frameworks to FedRAMP must map
at least **13 named KSIs** in both human-readable and machine-readable form with
source links. For CMMC contractors:

- Use ISO alignment at the **800-53 layer** via NIST OLIR (see
  `references/multi-framework-crosswalk.md`), not by asserting ISO covers CMMC
  requirements directly.
- When a vendor publishes a framework mapping page, trace through 800-53 to
  CMMC via the crosswalk.

---

## Rev 5 vs 20x Decision Tree

```
Need a cloud service for CUI?
  └─ DFARS 7012 requires FedRAMP Moderate or equivalent
       └─ Check Marketplace package (build_fedramp_snapshot.py)
            ├─ Active Rev 5 Agency / JAB authorization?
            │    └─ Obtain CRM → map 800-53 rows → CMMC objectives
            └─ FedRAMP 20x Class A/B/C labeling present?
                 └─ Public trust center + KSI catalog available?
                      ├─ Yes → run ksi_due_diligence checklist + CRM
                      └─ No  → interim: CRM + contractual SCN; document gap
```

---

## What This Skill Does Not Have

- Private KSI validation telemetry or secure-repository packages
- Authority to accept FedRAMP equivalency (contracting officer decision)
- Nonpublic 3PAO SAR content
- Guaranteed live trust-center API access for every vendor (verify per vendor)

When those are missing, the compliant path is honest documentation of customer-
side implementation and inherited controls with CRM citations, not hedging or
refusal.

---

## Related Files

- `references/grc/vendor-and-supply-chain.md`: ESP matrix, equivalency memo BoE
- `references/fedramp-gap.md`: CMMC to FedRAMP narrative and 800-53 tables
- `references/multi-framework-crosswalk.md`: OSCAL and ISO bridge
- `scripts/generate_trust_center.py`: your outward-facing trust center page
