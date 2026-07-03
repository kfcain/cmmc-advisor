# CMMC Level 1 Quickstart: The FCI-Only Path

> Source: FAR 52.204-21; 32 CFR 170.14, 170.15, 170.19, 170.22;
> CMMC Assessment Guide Level 1 v2.13; CMMC Scoping Guide Level 1 v2.13

## Overview

Level 1 is the CMMC path for organizations that handle Federal Contract
Information (FCI) but no Controlled Unclassified Information (CUI). FCI is
information not intended for public release that is provided by or generated
for the Government under contract, excluding information the Government
releases publicly and simple transactional data like payment processing
(48 CFR 4.1901, 32 CFR 170.4).

If you hold DoD contracts or purchase orders, you almost certainly handle
FCI. Level 1 is the floor, not an option. The good news: it is achievable in
weeks, not months, and requires no third party. You self-assess annually
against 15 basic safeguarding requirements and affirm the result in the
Supplier Performance Risk System (SPRS).

Related reading: `levels-and-assessment.md` for level selection,
`scoping-and-cui.md` for the FCI vs CUI distinction, and the six domain
files with Level 1 counterparts under `domains/`.

---

## The 15 Level 1 Requirements

Level 1 comprises the 15 basic safeguarding requirements of FAR
52.204-21(b)(1), identified in 32 CFR 170 and the CMMC Assessment Guide
Level 1 by their FAR clause paragraph. The deprecated CMMC Model v2.0
described Level 1 as 17 practices using 800-171-style numbers; the final
rule replaced that scheme. The legacy column below exists so you can read
older gap assessments without confusion.

| Requirement | Name | Legacy Model v2.0 ID | Implementation guidance |
|---|---|---|---|
| AC.L1-b.1.i | Authorized Access Control | AC.L1-3.1.1 | `domains/ac-access-control.md` (AC.L2-3.1.1) |
| AC.L1-b.1.ii | Transaction and Function Control | AC.L1-3.1.2 | `domains/ac-access-control.md` (AC.L2-3.1.2) |
| AC.L1-b.1.iii | External Connections | AC.L1-3.1.20 | `domains/ac-access-control.md` (AC.L2-3.1.20) |
| AC.L1-b.1.iv | Control Public Information | AC.L1-3.1.22 | `domains/ac-access-control.md` (AC.L2-3.1.22) |
| IA.L1-b.1.v | Identification | IA.L1-3.5.1 | `domains/ia-identification-auth.md` (IA.L2-3.5.1) |
| IA.L1-b.1.vi | Authentication | IA.L1-3.5.2 | `domains/ia-identification-auth.md` (IA.L2-3.5.2) |
| MP.L1-b.1.vii | Media Disposal | MP.L1-3.8.3 | `domains/mp-media-protection.md` (MP.L2-3.8.3) |
| PE.L1-b.1.viii | Limit Physical Access | PE.L1-3.10.1 | `domains/pe-physical-protection.md` (PE.L2-3.10.1) |
| PE.L1-b.1.ix | Manage Visitors and Physical Access | PE.L1-3.10.3, 3.10.4, 3.10.5 | `domains/pe-physical-protection.md` (PE.L2-3.10.3 through 3.10.5) |
| SC.L1-b.1.x | Boundary Protection | SC.L1-3.13.1 | `domains/sc-system-comms.md` (SC.L2-3.13.1) |
| SC.L1-b.1.xi | Public-Access System Separation | SC.L1-3.13.5 | `domains/sc-system-comms.md` (SC.L2-3.13.5) |
| SI.L1-b.1.xii | Flaw Remediation | SI.L1-3.14.1 | `domains/si-system-information-integrity.md` (SI.L2-3.14.1) |
| SI.L1-b.1.xiii | Malicious Code Protection | SI.L1-3.14.2 | `domains/si-system-information-integrity.md` (SI.L2-3.14.2) |
| SI.L1-b.1.xiv | Update Malicious Code Protection | SI.L1-3.14.4 | `domains/si-system-information-integrity.md` (SI.L2-3.14.4) |
| SI.L1-b.1.xv | System and File Scanning | SI.L1-3.14.5 | `domains/si-system-information-integrity.md` (SI.L2-3.14.5) |

Note the consolidation: PE.L1-b.1.ix covers visitor escort, physical access
logs, and physical access devices, which the old model counted as three
separate practices. That is why 17 became 15 with no requirement dropped.

The Level 1 requirements protect FCI. The corresponding Level 2 requirements
protect CUI with the same control language. Implement once, and the work
counts toward Level 2 if CUI ever enters your environment.

---

## Annual Self-Assessment and Affirmation

The Level 1 process under 32 CFR 170.15:

1. **Define your CMMC Assessment Scope** (see Scoping below).
2. **Assess all 15 requirements** using the criteria in the CMMC Assessment
   Guide Level 1 and the assessment methods of NIST SP 800-171A adapted for
   FCI: examine artifacts, interview people, test mechanisms.
3. **Record a finding per requirement:** MET, NOT MET, or NOT APPLICABLE
   as defined in 32 CFR 170.24. Every requirement must land on MET or NOT
   APPLICABLE to achieve the CMMC Status of Final Level 1 (Self).
4. **Submit results in SPRS**, including at minimum: CMMC Level, CMMC
   Status Date, CMMC Assessment Scope, all CAGE codes associated with the
   in-scope information systems, and the compliance result
   (32 CFR 170.15(a)(1)(i)).
5. **Affirm.** The Affirming Official, the senior representative responsible
   for CMMC compliance, submits an affirmation in SPRS attesting that the
   organization has implemented and will maintain all applicable requirements
   (32 CFR 170.22).
6. **Repeat annually.** Both the self-assessment and the affirmation recur
   every year to maintain the CMMC Status.

The affirmation carries legal weight. False affirmations expose the company
and the Affirming Official personally to False Claims Act liability. Treat
the annual cycle as an operational commitment, not paperwork. See
`grc/continuous-monitoring.md` for keeping the posture real between cycles.

There are no documentation requirements for the Level 1 self-assessment
itself (no SSP is required at Level 1), but keep your evidence: assessors
of a future Level 2 effort, prime contractors, and your own next annual
cycle all benefit from organized artifacts.

---

## No POA&Ms at Level 1

32 CFR 170.15(a)(1) is explicit: no Plans of Action and Milestones are
permitted for Level 1. There is no Conditional Level 1 status. If a
requirement is NOT MET, fix it, then complete the self-assessment.

Practical consequence: do not submit a Level 1 self-assessment with known
gaps and a plan to fix them later. That is a false affirmation, not a
compliance strategy. See `poam-management.md` for how POA&Ms work at
Levels 2 and 3.

---

## Level 1 Scoping

Per 32 CFR 170.19(b) and the CMMC Scoping Guide Level 1:

- **In scope:** every asset that processes, stores, or transmits FCI.
  Process means the asset uses FCI (accessed, entered, edited, generated,
  printed). Store means FCI at rest, including paper. Transmit means FCI
  in motion between assets.
- **Out of scope:** assets that do not process, store, or transmit FCI.
- **Specialized Assets are out of scope at Level 1:** IoT and IIoT devices,
  Operational Technology, Government Furnished Equipment, Restricted
  Information Systems, and Test Equipment are not assessed at Level 1 even
  when they touch FCI. This is more lenient than Level 2, where Specialized
  Assets enter the scope discussion; do not carry Level 1 scoping
  assumptions into a Level 2 effort.

There is no asset categorization exercise at Level 1 and no scoping
documentation requirement. In practice, a one-page inventory of where FCI
lives (email, file shares, accounting system, laptops) is worth maintaining
anyway; it makes the annual reassessment and any future Level 2 gap
analysis faster.

---

## Are You Actually Level 1?

The most expensive scoping mistake is assessing at Level 1 when your
contracts put CUI in your environment. Check before you commit:

- **DFARS 252.204-7012 in the contract** signals CUI. Level 2 applies.
- **A DD Form 254** (Contract Security Classification Specification)
  attached to the contract signals classified or CUI handling requirements.
- **CUI markings** on drawings, specifications, or technical data you
  receive. Export-controlled technical data (ITAR/EAR) is CUI.
- **You generate technical data** under a defense contract, even if nobody
  marked anything. Ask your contracting officer in writing what the
  information is, and keep the answer.

If none of those apply and the contract carries only FAR 52.204-21, Level 1
is your requirement. If the answer is ambiguous, ask the contracting
officer and document the response. Guessing in either direction costs
money: over-scoping buys a Level 2 program you may not need, under-scoping
risks contract eligibility and False Claims Act exposure.

---

## Cheapest Compliant Path

Level 1 does not require government cloud, FedRAMP-authorized services, or
specialized tooling. FAR 52.204-21 carries no FedRAMP or DFARS 7012
obligations. A small shop can reach Level 1 with:

1. **Commercial cloud email and files** (Microsoft 365 Business, Google
   Workspace) with MFA enforced for all users. This covers identification,
   authentication, and much of access control.
2. **A business-grade firewall or router** with default-deny inbound. That
   plus the cloud provider's boundary controls addresses SC.L1-b.1.x.
3. **Separate public web presence** from internal systems (hosted website,
   not a server in the office) for SC.L1-b.1.xi and AC.L1-b.1.iv.
4. **Automatic OS and application updates** everywhere, plus the built-in
   endpoint protection (Defender, XProtect) kept current, for the four SI
   requirements.
5. **A locked office and a visitor sign-in sheet** for the two PE
   requirements. A paper log is acceptable evidence.
6. **Cross-cut shredder and a disk-wipe step** in your laptop retirement
   checklist for MP.L1-b.1.vii.

Budget reality: for a 5 to 20 person shop already on commercial cloud, the
gap is usually MFA enforcement, update discipline, and writing down who has
access to what. Expect days of effort, not weeks, and near-zero new license
cost. If CUI is anywhere on the horizon, see `contractor-profiles.md` and
`modern-it/productivity/README.md` before buying anything, so purchases
carry forward to Level 2.

---

## Key Takeaways for Contractors

1. Level 1 is 15 requirements from FAR 52.204-21, self-assessed annually,
   affirmed in SPRS by your Affirming Official. Identifiers run
   AC.L1-b.1.i through SI.L1-b.1.xv; 17-practice lists are the deprecated
   model.
2. No POA&Ms, no conditional status. Everything MET or NOT APPLICABLE, or
   no Level 1 status.
3. Scope is every asset touching FCI; Specialized Assets are excluded at
   Level 1.
4. Verify you are not actually a Level 2 shop before you start. DFARS
   7012, CUI markings, or export-controlled technical data mean CUI.
5. Commercial cloud plus MFA, updates, and basic physical controls gets a
   small FCI-only shop there in days. Every Level 1 control carries
   forward to Level 2.
