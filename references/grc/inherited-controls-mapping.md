# Inherited Controls: Mapping FedRAMP CRM and BoE onto Assessment Objectives

> Source: 32 CFR 170.17(c)(5)-(6), 170.18(c)(5)-(6); DFARS
> 252.204-7012(b)(2)(ii)(D); DoD CIO Memorandum, FedRAMP Moderate
> Equivalency for Cloud Service Providers (December 21, 2023); FedRAMP
> SSP Attachment 9 / Appendix J (Control Implementation Summary /
> Customer Responsibility Matrix conventions)

## Overview

When CUI lives on a FedRAMP-authorized platform, part of your CMMC
posture is implemented by the provider. The rule sanctions that
explicitly: inherited protections are demonstrated through the
provider's Customer Implementation Summary / Customer Responsibility
Matrix (CIS/CRM) and an associated body of evidence, and your on-premises
infrastructure connecting to the platform stays in your assessment scope
(32 CFR 170.17(c)(5) at Level 2, 170.18(c)(5) at Level 3).

This file is the working method for turning a provider's CRM (often
shipped as Appendix J of their FedRAMP SSP, or a CIS workbook) and BoE
into per-assessment-objective inheritance entries in your program data
file (`templates/program-data.schema.json`), which then flow into your
generated SSP and dashboard.

The failure mode this prevents is anti-pattern 14, inherited control
fantasy: claiming the platform "handles" a requirement no CRM row
actually assigns to the provider.

---

## What You Are Reading

- **CIS (Control Implementation Summary).** Per 800-53 control: who is
  responsible: the provider, the customer, or shared. Think of it as the
  index.
- **CRM (Customer Responsibility Matrix), FedRAMP Appendix J.** The
  customer-facing detail: for every control with a customer share, what
  the customer must configure, operate, or document. This is the
  load-bearing artifact for your SSP.
- **BoE (Body of Evidence).** The provider's assessment artifacts. For
  FedRAMP Authorized offerings, the Marketplace listing plus the CRM is
  usually sufficient for CMMC purposes; for equivalency claims, the
  full BoE defined in the DoD CIO memo (3PAO-assessed SSP, SAR, SAP,
  penetration tests, monthly scans, continuous monitoring summaries,
  with zero unresolved 3PAO-assessment POA&Ms) is mandatory. See
  `vendor-and-supply-chain.md`.

CRMs speak NIST SP 800-53 because FedRAMP does. Your assessment speaks
NIST SP 800-171 assessment objectives. The mapping is the work.

---

## The Method: CRM Row to Assessment Objective

For each 800-171 requirement you believe the platform helps with:

1. **Find the 800-53 relatives.** NIST SP 800-171 Rev 2 Appendix D maps
   each requirement to its source 800-53 controls (3.13.11 maps to
   SC-13; 3.1.1 to AC-2/AC-3/AC-17, and so on). Pull the CRM rows for
   those controls.
2. **Read the responsibility split, not the control title.** A CRM row
   for SC-13 marked "provider responsibility" for service-side
   encryption does not cover your endpoints. Split the claim at the
   objective level.
3. **Classify each assessment objective** (from
   `references/data/assessment-objectives.json` or the
   `references/assessment-objectives/` files):
   - **inherited**: the provider fully satisfies the objective inside
     the authorization boundary, and the CRM says so. You cite the CRM
     row; your narrative says what you inherited and from where.
   - **shared**: the provider covers part; you operate the rest
     (configuration, enforcement, records). Record the customer share
     explicitly; that share is what the assessor tests on your side.
   - **customer**: the CRM assigns it to you, or the objective concerns
     assets outside the boundary (your endpoints, your people, your
     procedures). No inheritance entry at all.
4. **Record it in the program data file** under the objective:

```yaml
inheritance:
  source: gcch            # id from inheritance_sources
  type: shared
  crm_ref: SC-13 rows 3-7
  customer_note: Customer enforces FIPS mode on endpoints via Intune
```

   with the platform declared once under `inheritance_sources` (provider,
   CSO, FedRAMP status, CRM document and version, BoE location,
   verification date).
5. **Keep the evidence pairing.** For every inherited or shared
   objective: the CRM extract (or row citation) plus your customer-side
   evidence. The generated SSP prints the inheritance line under the
   objective; the dashboard's Inheritance view shows every objective
   mapped to each source.

## Worked Example Rows

| Objective | Platform says (CRM) | Classification | Your side |
|---|---|---|---|
| 3.13.11[a] FIPS-validated cryptography employed | SC-13: provider uses FIPS-validated modules service-side | shared | BitLocker FIPS mode on endpoints, CMVP cert number in the CMVP table |
| 3.3.1[a-c] audit records at defined events | AU-2/AU-12: platform generates service audit logs | shared | You define the event set, retain and review the logs, cover non-platform systems |
| 3.10.1[a] authorized physical access individuals identified | PE-2: provider datacenters in boundary | inherited (for datacenter assets) | Your office spaces are still fully yours |
| 3.5.3[a-b] MFA for local and network access | IA-2: platform supports MFA | customer | Supports is not enforces: your Conditional Access policy is the control |
| 3.1.1[d] access limited to authorized users | AC-2/AC-3: platform enforces your directory decisions | shared | Group membership, access requests, and reviews are yours |

The pattern to internalize: platforms mostly inherit **facility and
service-infrastructure** objectives, share **mechanism** objectives, and
almost never touch **process and people** objectives (policies, reviews,
training, screening, incident procedures). If your mapping shows most of
the 320 objectives inherited, the mapping is wrong.

---

## Rules That Bound the Exercise

- **CUI on the platform requires FedRAMP Moderate or equivalency**
  (DFARS 7012(b)(2)(ii)(D); 170.17(c)(5)). Inheritance from a
  non-authorized commercial service is not a thing, whatever its SOC 2
  says (anti-pattern 11).
- **Your connecting infrastructure is in scope** and the CRM's
  customer-side requirements must be documented or referenced in your
  SSP (170.17(c)(5)(iii)).
- **At Level 3, every one of the 24 enhanced requirements applies in
  every environment where CUI flows**, and anything inherited must be
  demonstrated via CIS/CRM plus BoE naming who implements what
  (170.18(c)(5)). See `../level-3-expert.md`.
- **Re-verify on a cycle.** Authorization status and CRM versions
  change; the `verified` date on each inheritance source follows the
  same dated-verification convention as `SOURCES.md`, and drift review
  (`continuous-monitoring.md`) re-checks it.

## Workflow for This Skill

When a user provides a CRM, CIS workbook, or BoE index:

1. Declare the platform under `inheritance_sources` in their program
   data file, capturing document name, version, and BoE location.
2. Walk the affected requirements family by family, proposing a
   classification per assessment objective with the CRM row citation,
   and drafting the customer-share note wherever the answer is shared.
3. Never mark an objective inherited without a CRM row to cite. If the
   CRM is silent, the objective is customer-owned until the provider
   documents otherwise; say so plainly.
4. Regenerate the SSP and dashboard so the inheritance lines and the
   Inheritance view reflect the mapping, and add the CRM extracts to
   the evidence tree.

---

## Key Takeaways for Contractors

1. Inheritance is demonstrated, not assumed: CRM row plus BoE, rendered
   per assessment objective in your SSP.
2. Classify at the objective level: inherited, shared with an explicit
   customer share, or customer. Facility and service objectives
   inherit; mechanisms share; process and people stay yours.
3. CUI on a platform means FedRAMP Moderate Authorized or the full
   equivalency body of evidence, nothing softer.
4. Your connecting infrastructure and every customer-side CRM
   requirement remain in your assessment scope.
5. Date-stamp and re-verify: CRM versions and authorization status are
   perishable facts.
