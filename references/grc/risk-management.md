# Risk Management Program: The Layer Above the RA Domain

> Source: NIST SP 800-171 Rev 2 (3.11.1 through 3.11.3); NIST SP 800-30;
> 32 CFR 170.21, 170.24

## Overview

The RA domain file (`domains/ra-risk-assessment.md`) covers the three
Level 2 risk assessment requirements: periodic risk assessment
(RA.L2-3.11.1), vulnerability scanning (RA.L2-3.11.2), and remediation
(RA.L2-3.11.3). This file covers the program that makes those requirements
real: the risk register, the acceptance workflow, the operating cadence,
and how risk connects to the rest of your compliance machinery.

The distinction matters at assessment time. An assessor can verify a risk
assessment document exists (the practice). What separates a working
program from compliance theater (see `anti-patterns.md`) is evidence the
organization identifies risks continuously, decides about them at the
right level, and feeds decisions back into configuration, incident
response, and vendor management.

---

## Risk Register Design

A risk register is a living record of identified risks and their
disposition. For a CMMC-scoped environment, keep it small enough to
maintain and complete enough to defend. Recommended fields:

| Field | What it holds |
|---|---|
| ID | Stable identifier (RISK-2026-014) |
| Description | The risk in cause-event-consequence form |
| Source | How it surfaced: risk assessment, scan, incident, vendor change, audit |
| Affected assets | Tie to your asset inventory and CMMC scope categories |
| Related requirements | CMMC practice IDs the risk touches (e.g. AC.L2-3.1.5) |
| Likelihood / Impact | Simple scale (low/moderate/high) applied consistently |
| Disposition | Mitigate, accept, transfer, avoid |
| Owner | A named person, not a team |
| Decision authority | Who approved the disposition and when |
| Review date | When this entry gets re-examined |
| Linked artifacts | POA&M entry, SSP section, change ticket |

A worked example:

```
ID:              RISK-2026-014
Description:     Because engineering file servers allow SMBv1 for one
                 legacy CNC controller, an attacker on the internal
                 network could exploit known SMBv1 weaknesses to reach
                 CUI stored on the ENG-FS01 share.
Source:          Quarterly vulnerability scan, 2026-05-12
Affected assets: ENG-FS01 (CUI asset), CNC-07 (Specialized Asset)
Related reqs:    CM.L2-3.4.7, SC.L2-3.13.1, RA.L2-3.11.3
Likelihood:      Moderate     Impact: High
Disposition:     Mitigate. Isolate CNC-07 to purpose-specific VLAN,
                 disable SMBv1 on ENG-FS01 by 2026-08-01.
Owner:           J. Rivera (Infrastructure Lead)
Authority:       ISSM approved 2026-05-19
Review date:     2026-08-15
Linked:          CHG-3312, SSP section 3.13 update pending
```

Keep the register wherever your team already works (ticket system,
SharePoint list, GRC tool). The tool matters far less than the review
cadence and the named owners.

---

## Risk Acceptance Is Not a Compliance Verb

Risk acceptance is a legitimate outcome for risks inside your risk
management program. It is not a way to score a CMMC requirement.

Under the CMMC scoring methodology (32 CFR 170.24), a security requirement
is MET, NOT MET, or NOT APPLICABLE. There is no "risk accepted" finding.
An internal memo accepting the risk of not implementing FIPS-validated
cryptography does not change SC.L2-3.13.11 from NOT MET to anything else,
and it will not move your SPRS score. The only paths for a NOT MET
requirement are remediation or, where eligible, a POA&M entry under the
rules in `poam-management.md`.

Where acceptance does belong:

- **Residual risk after a control is implemented.** MFA is deployed
  (IA.L2-3.5.3 MET); the residual phishing risk of a legacy protocol
  exception for one service account is documented and accepted with an
  expiration date.
- **Risks outside requirement scope.** Business risks, availability
  risks, and threats the 110 requirements do not address still deserve
  register entries and decisions.
- **Prioritization decisions.** Which mitigations happen this quarter,
  which wait, and why.

Every acceptance needs a named authority at the right altitude (the ISSM
or executive sponsor for anything touching CUI protection), a rationale,
and a review date. Open-ended acceptances are how registers become
graveyards.

---

## Cadence and Triggers

RA.L2-3.11.1 requires periodic risk assessment. Under the CMMC model,
organization-defined intervals may not exceed one year (32 CFR 170.14(d)).
A defensible operating rhythm:

- **Annually:** full risk assessment refresh, aligned with your annual
  affirmation cycle (see `grc/continuous-monitoring.md`) so the Affirming
  Official signs with current information.
- **Quarterly:** register review. Close stale entries, re-examine
  acceptances hitting review dates, confirm mitigation progress against
  POA&M dates.
- **Event-driven, within days of:** a reportable or near-miss incident, a
  significant architecture or vendor change, a new contract bringing new
  CUI types into scope, or threat information relevant to your stack.

Record each cycle even when nothing changes: a dated one-page "reviewed,
no material change" note is evidence of a living program.

---

## Integration: Where Risk Decisions Flow

A register that talks to nothing is shelf-ware. Wire it to:

- **POA&M.** Every POA&M entry should trace to a register entry with the
  same owner and dates. When a POA&M item closes, the register entry
  records the residual state. See `poam-management.md`.
- **SSP.** Dispositions that change how a requirement is implemented
  trigger an SSP update (see `ssp-guidance.md` and
  `grc/program-governance.md` on change management).
- **Configuration management.** Mitigations land as change tickets;
  CM.L2-3.4.3 change tracking is the evidence trail.
- **Incident response.** IR lessons-learned feed new register entries;
  register context (what we accepted and why) speeds triage during an
  incident.
- **Vendor management.** ESP and CSP risks belong in the same register
  with the same discipline. See `grc/vendor-and-supply-chain.md`.
- **Level 3 trajectory.** If Level 3 is in your future, RA.L3-3.11.1e
  through 3.11.7e turn this program into a threat-informed, supply-chain-
  aware capability with never-POA&M-eligible components. Building the
  register habit now is the cheap part. See `level-3-expert.md`.

---

## What the Assessor Wants

For the RA requirements, expect requests for:

- The current risk assessment and the one before it (proving periodicity)
- The register itself, with entries showing source, owner, decision
  authority, and dates
- Scan results and the remediation trail for a sample of findings
  (RA.L2-3.11.2, 3.11.3)
- Evidence that a real event (incident, major change) produced a risk
  decision

The pattern assessors flag: a beautiful annual risk assessment PDF, an
empty register, and scan reports nobody triaged. Volume is not the goal;
traceability is.

---

## Key Takeaways for Contractors

1. Run one register with named owners, decision authorities, and review
   dates. Tie every entry to assets and practice IDs.
2. Risk acceptance never changes a CMMC finding. MET, NOT MET, or NOT
   APPLICABLE, with POA&M as the only deferral mechanism, under its own
   rules.
3. Annual full assessment, quarterly register review, event-driven
   updates. Intervals must not exceed one year.
4. Wire the register to POA&M, SSP, change management, IR, and vendor
   management so decisions leave marks where assessors look.
