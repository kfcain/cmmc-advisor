# Program Governance: Roles, Rhythms, and the Paper That Proves Them

> Source: 32 CFR 170.4, 170.22; DFARS 252.204-7012(c) through (g);
> NIST SP 800-171 Rev 2 (3.12.1 through 3.12.4)

## Overview

Controls fail quietly when nobody owns the program. This file covers the
governance layer: who holds which role, how policy becomes procedure
becomes evidence, how IT change stays synchronized with compliance
documents, and the incident reporting obligations that have to work at
2 a.m. on a Saturday.

Control-level content stays where it belongs: `domains/ca-security-assessment.md`
for the CA requirements, `domains/ir-incident-response.md` for IR
requirements, `ssp-guidance.md` for the SSP itself. This file is about
making those artifacts belong to someone.

---

## Roles

Titles vary; accountabilities should not. Map these to real names, even
if one person holds three of them:

- **Executive sponsor.** Owns the budget and the risk appetite. Signs off
  on risk acceptances above the ISSM's altitude
  (`grc/risk-management.md`).
- **Affirming Official (32 CFR 170.22).** The senior official who affirms
  continuing compliance in SPRS after each assessment and annually. This
  is a named individual with personal exposure; give them a real
  evidence packet (`grc/continuous-monitoring.md`), not a signature line.
- **ISSM-equivalent (program owner).** Runs the compliance program:
  owns the SSP, the POA&M, the risk register, assessment relationships,
  and this governance rhythm. In small shops this is often the same
  person as the Affirming Official; document that explicitly.
- **ISSO-equivalent / control owners.** Operate and evidence specific
  requirements per the control-owner model in
  `grc/continuous-monitoring.md`.
- **Incident commander (on-call).** Authority to invoke the IR plan,
  including the DIBNet reporting duty below, without waiting for a
  Monday meeting.

**Small-shop reality:** a 12-person company might assign executive
sponsor and Affirming Official to the CEO, ISSM duties to the operations
lead, and control ownership across two engineers plus the MSP (with the
MSP's duties pinned in the responsibility matrix; see
`grc/vendor-and-supply-chain.md`). That is a perfectly assessable
structure if it is written down, current, and each person can describe
their piece in an interview. What fails assessments is the org chart
nobody recognizes. See `contractor-profiles.md` for sizing patterns.

---

## Policy Lifecycle: Policy, Procedure, Evidence

Assessors walk a three-link chain, and anti-pattern 1 in
`anti-patterns.md` (policy pyramid without procedures) is them finding
link two missing:

1. **Policy** states intent and assigns authority ("all remote access to
   the CUI enclave requires MFA; the ISSM approves exceptions").
2. **Procedure** states how, concretely, for your stack ("enable
   Conditional Access policy CA-04; exceptions via ticket type SEC-EXC
   with ISSM approval; review exceptions monthly").
3. **Evidence** proves it happened (the CA-04 export, the exception
   tickets, the monthly review notes).

Lifecycle rules that keep the chain honest:

- Version control every policy and procedure: owner, approval date,
  review date, change history. The document history is itself evidence
  for CA.L2-3.12.1 through 3.12.4.
- Annual review minimum, aligned to the affirmation cycle. Also review
  on stack changes: a procedure referencing decommissioned tooling is an
  interview landmine.
- Write procedures at the altitude of the person executing them. If the
  new hire cannot run it, it is a policy wearing a procedure's clothes.
- Retire formally. Superseded documents get an end date and leave the
  active set; assessors sampling from your policy library should never
  pull two contradictory versions.

`policy-mapper`-style traceability (which requirement does each policy
statement serve?) pays for itself at assessment time; at minimum,
maintain a mapping table from each of the 110 requirements to its policy
and procedure homes.

---

## Change Management of the Compliance Posture

CM.L2-3.4.x governs technical change control. Governance adds one
question to every change: **does this move a compliance fact?** Build
these triggers into the change template:

| Change | Compliance action |
|---|---|
| New system or service in the CUI flow | Scope review (`scoping-and-cui.md`), SSP boundary and diagram update, vendor matrix if external |
| Security control implementation changes | SSP implementation statement update; rescore if a requirement's status moves (`grc/continuous-monitoring.md`) |
| New vendor or vendor service change | ESP matrix pass (`grc/vendor-and-supply-chain.md`), CRM update |
| Personnel change in a named role | Role map update; SPRS contact update if the Affirming Official changed |
| Enclave expansion, office move, new site | Scoping and PE evidence refresh |

The SSP is a living document; 32 CFR 170 expects assessment against the
SSP you actually operate. A quarterly "SSP delta review" (walk the change
log, confirm every compliance-relevant change landed in the document) is
cheap insurance against the worst assessment-day discovery: an accurate
network and an outdated SSP describing a different one.

---

## Incident Reporting Obligations: The 72-Hour Machine

DFARS 252.204-7012(c) through (g) creates duties that must work under
stress. Program-level readiness, before anything happens:

- **A DoD-approved Medium Assurance Certificate in hand.** Reporting to
  DIBNet (dibnet.dod.mil) requires one; obtaining it takes days you will
  not have during an incident. Verify it is current, and know which
  workstation it is installed on.
- **Know the clock.** Rapid report to DoD via DIBNet within **72 hours**
  of discovery of any cyber incident affecting covered defense
  information or the contractor's ability to perform operationally
  critical support. Discovery starts the clock, not root cause
  confirmation. Report with what you know; supplement later.
- **Preservation duty:** preserve and protect images of all known
  affected information systems and relevant monitoring/packet capture
  data for at least **90 days** from submission of the cyber incident
  report, to allow DoD to request media (7012(e)).
- **Malware handling:** if malicious software is found and isolated,
  submit it to the DoD Cyber Crime Center (DC3) per instructions, not to
  the contracting officer (7012(d)).
- **Access cooperation:** be prepared to give DoD access to additional
  information and equipment for forensic analysis and damage assessment
  (7012(f) and (g)).
- **Flowdown symmetry:** subcontractors report up. Your subs need your
  incident contact and the obligation, in writing, to notify you when
  they report to DIBNet, so the prime's own reporting stays coherent.

Drill it. A tabletop twice a year that runs the first 72 hours (declare,
preserve, report, notify the prime or subs, engage the MSSP per contract)
is the difference between a controlled report and an improvised one. The
control-level IR content (IR.L2-3.6.1 through 3.6.3) lives in
`domains/ir-incident-response.md`; the incident response plan template
questions live there too.

One scoping note: an incident is also a compliance event. It triggers a
risk register entry (`grc/risk-management.md`), possibly an SSP change,
and shows up in the next affirmation packet. Close that loop
deliberately.

---

## Key Takeaways for Contractors

1. Name the roles: sponsor, Affirming Official, ISSM-equivalent, control
   owners, incident commander. One person may hold several; paper must
   say so and interviews must match.
2. Keep the policy, procedure, evidence chain versioned, reviewed
   annually, and written at operator altitude. Maintain a
   requirement-to-policy mapping table.
3. Every change asks: does this move a compliance fact? Quarterly SSP
   delta reviews keep the document matching the network.
4. Build the 72-hour machine in advance: current Medium Assurance
   Certificate, DIBNet procedure, 90-day preservation, DC3 malware path,
   sub-to-prime notification, and tabletop drills.
