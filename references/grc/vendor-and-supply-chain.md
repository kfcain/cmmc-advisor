# Vendors, ESPs, and Supply Chain: Whose Compliance Is It Anyway?

> Source: 32 CFR 170.4, 170.17(c)(5) and (6), 170.18(c)(5) and (6),
> 170.19; DFARS 252.204-7012(b)(2)(ii)(D); DoD CIO Memorandum, FedRAMP
> Moderate Equivalency for Cloud Service Providers (December 21, 2023);
> DoD CIO, ESP scoping requirements presentation
> (dodcio.defense.gov/Portals/0/Documents/CMMC/TechImplementationCMMC-Rqrmnts.pdf)

## Overview

Your CMMC posture includes everyone who touches your CUI or the data that
protects it. The final rule made vendor treatment much clearer than the
proposed rule did, and mostly friendlier: external providers no longer
need their own CMMC certifications in most configurations, but their
services get assessed inside **your** scope, which means your contracts
with them must produce evidence you can hand an assessor.

Definitions that drive everything (32 CFR 170.4):

- **External Service Provider (ESP):** external people, technology, or
  facilities used for provision and management of IT or cybersecurity
  services on behalf of the organization. A provider is only an ESP for
  CMMC purposes if CUI or Security Protection Data is processed, stored,
  or transmitted on its assets.
- **Security Protection Data (SPD):** data stored or processed by
  Security Protection Assets used to protect the assessed environment:
  SIEM logs, EDR telemetry, configuration data, vulnerability status,
  passwords granting access to the in-scope environment.
- **Cloud Service Provider (CSP):** a provider offering cloud services
  (on-demand, shared-resource computing). The CSP versus non-CSP
  distinction changes which rule applies.

---

## The ESP Decision Matrix

Per the DoD CIO ESP scoping guidance and 32 CFR 170.17(c)(5)-(6) (Level 2)
and 170.18(c)(5)-(6) (Level 3):

| The provider handles | Provider is a CSP | Provider is not a CSP |
|---|---|---|
| **CUI** (with or without SPD) | Must be FedRAMP Moderate Authorized or FedRAMP Moderate equivalent per DFARS 7012(b)(2)(ii)(D) | Services are in your assessment scope and assessed as part of your assessment |
| **SPD only** (no CUI) | Services assessed within your scope as Security Protection Assets; no FedRAMP requirement | Services assessed within your scope as Security Protection Assets |
| **Neither CUI nor SPD** | Not an ESP for CMMC purposes | Not an ESP for CMMC purposes |

Consequences worth spelling out:

- **No standalone ESP certification requirement.** An MSP or MSSP does
  not need its own CMMC certification for you to use it. Its services are
  assessed within your assessment. (An ESP may voluntarily undergo its own
  assessment, which can simplify your evidence, but the rule does not
  demand it.)
- **Your SSP carries the relationship.** The use of the ESP, its
  relationship to you, and the services provided must be documented in
  your SSP and described in the ESP's service description and customer
  responsibility matrix (CRM).
- **Your connecting infrastructure is in scope.** Whatever on-premises
  gear connects to the CSP or ESP is part of your assessment scope, and
  the CRM's customer-side requirements must appear in your SSP.
- **The SIEM vendor question, answered.** An MSSP that only ingests your
  logs handles SPD, not CUI: assessed as a Security Protection Asset in
  your scope, no FedRAMP obligation. Put your log pipeline in the CRM and
  be ready to show how the MSSP's people and tooling meet the relevant
  requirements for the capability they provide.

---

## CSPs and FedRAMP Moderate Equivalency

When a cloud service stores, processes, or transmits CUI, DFARS
252.204-7012(b)(2)(ii)(D) gives exactly two doors:

1. **FedRAMP Moderate (or higher) Authorized**, per the FedRAMP
   Marketplace. No further assessment needed for the baseline question.
   See `fedramp-marketplace-guide.md` for finding and reading
   authorizations, and `fedramp-gap.md` for what FedRAMP does and does
   not cover relative to CMMC.
2. **FedRAMP Moderate equivalency** per the DoD CIO memo of December 21,
   2023. Equivalency is deliberately hard: 100 percent compliance with
   the current FedRAMP Moderate baseline, assessed by a
   FedRAMP-recognized 3PAO, evidenced by a full body of evidence (SSP,
   SAP, SAR, penetration test conducted annually, monthly scan regimes,
   ISCP, IRP, CMP, CIS workbook, continuous monitoring strategy and
   monthly summaries, and more). No POA&Ms from the 3PAO assessment are
   allowed; every finding must be closed and validated. DIBCAC reviews
   the body of evidence, and the CSP needs an annual 3PAO assessment to
   keep the claim alive.

Practitioner translation: treat "FedRAMP equivalent" claims with the same
skepticism as "military-grade encryption." Ask the vendor for the 3PAO
SAR and the body-of-evidence index before you architect around the
service. If they send a marketing letter instead, the service cannot hold
CUI. Anti-pattern 14 (inherited control fantasy) and anti-pattern 11
(commercial cloud with policy controls) in `anti-patterns.md` both live
here.

Remember also that 7012 requires the CSP to support cyber incident
reporting, malware submission, media preservation, forensic access, and
damage assessment. Equivalency covers the baseline; these clause
obligations ride along and belong in your contract with the CSP.

---

## Flowdowns to Subcontractors

Prime contractors carry the compliance topology of their whole team:

- **DFARS 252.204-7012 flows down** to subcontractors whose performance
  involves covered defense information. The sub needs the same
  safeguarding and incident reporting obligations.
- **DFARS 252.204-7021 flows down** the CMMC status requirement
  appropriate to the information the subcontractor will handle: a sub
  seeing only FCI needs Level 1; a sub receiving CUI needs the Level 2
  status the contract specifies.
- **Verify before award and at option exercise.** Primes should check a
  sub's CMMC status and affirmation currency (via SPRS, or by requiring
  the sub to produce it) before flowing CUI. An expired conditional
  status or a missing annual affirmation makes the sub ineligible, and
  discovering that mid-performance is a program problem, not just a
  compliance problem.
- **Minimize what you flow.** The cheapest subcontractor compliance is
  the CUI they never receive. Strip attachments to what the sub needs,
  mark properly, and prefer collaboration inside your own enclave
  (sub logs into your environment) over shipping CUI into theirs.

---

## Vendor Due Diligence: What to Ask Before Signing

For any MSP, MSSP, or SaaS that will sit inside your scope:

1. **A real customer responsibility matrix.** Per-requirement, naming who
   does what, in a form you can lift into your SSP. If the vendor cannot
   produce one, you will be writing it during your assessment week.
2. **Their compliance posture, in evidence.** For CSPs holding CUI:
   FedRAMP Marketplace listing or the equivalency body of evidence. For
   non-CSP ESPs: how their people, facilities, and tooling meet the
   requirements relevant to the service (screening for PS, MFA and
   privileged access handling for AC/IA, their own logging for AU).
3. **Access architecture.** How their technicians reach your
   environment: dedicated accounts in your tenant (preferred, so your
   AC/IA/AU controls apply) versus their shared tooling (which drags
   their stack into your scope).
4. **Incident cooperation terms.** 72-hour reporting support, forensic
   access, log retention matching your 7012 obligations. See
   `grc/program-governance.md`.
5. **Exit and data return.** Where your CUI and SPD live at termination,
   and how they are destroyed to MP.L2-3.8.3 standards.
6. **Change notification.** Contractual obligation to notify you of
   material changes: subprocessors, hosting moves, authorization status
   changes. Wire notifications into your drift review
   (`grc/continuous-monitoring.md`).

Track each vendor in the risk register (`grc/risk-management.md`) with an
owner and a review date, and re-verify authorization-dependent facts on a
cycle; the dated verification stamp convention in `SOURCES.md` applies to
your own vendor records too.

If Level 3 is in your trajectory, the stakes rise: RA.L3-3.11.6e and
3.11.7e make supply chain risk response and planning never-POA&M-eligible
requirements, and DIBCAC assesses ESP-delivered capabilities inside your
scope. See `level-3-expert.md`.

---

## Key Takeaways for Contractors

1. A provider is only an ESP if your CUI or SPD touches its assets. CSPs
   with CUI need FedRAMP Moderate or true equivalency; everyone else gets
   assessed inside your scope, no standalone certification required.
2. The customer responsibility matrix is the load-bearing document. No
   CRM, no deal.
3. Equivalency means a 3PAO-assessed, POA&M-free, annually revalidated
   body of evidence, not a vendor letter.
4. Flow down 7012 and the right CMMC level to subs, verify their status
   and affirmations, and flow the minimum CUI necessary.
5. Vendor risk lives in the same register, with the same owners-and-dates
   discipline, as everything else.
