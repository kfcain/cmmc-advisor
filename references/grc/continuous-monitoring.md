# Continuous Monitoring: Staying Assessment-Ready Between Assessments

> Source: 32 CFR 170.15 through 170.18, 170.22; DFARS 252.204-7019,
> 252.204-7020, 252.204-7021; NIST SP 800-171 Rev 2 (3.12.3)

## Overview

Certification is a snapshot. The obligations are continuous. Between the
triennial assessments (Level 2 and Level 3; Level 2 Self is also
triennial per 32 CFR 170.16) and Level 1's annual self-assessment,
three clocks keep running:

1. **Annual affirmations** in SPRS by your Affirming Official
   (32 CFR 170.22).
2. **Accuracy obligations** on your SPRS information under DFARS
   252.204-7019/7020, and the government's standing right to a DIBCAC
   investigation under 7020, whose results supersede your CMMC status.
3. **CA.L2-3.12.3**, the security requirement to monitor controls on an
   ongoing basis, which your own SSP describes.

This file describes the operating model that keeps all three honest:
control owners, evidence refresh, drift detection, and score maintenance.
Point-in-time readiness is anti-pattern 13 in `anti-patterns.md`; this is
the antidote.

---

## The Control-Owner Model

Assign every one of the 110 requirements (and the 15 Level 1 requirements,
and at Level 3 the 24 enhanced requirements) a named owner. Not a
department. A person, with a deputy for coverage.

The owner's job, per requirement:

- Knows what the SSP says about how the requirement is implemented
- Keeps the implementation matching the SSP (or triggers the change
  process when it must diverge; see `grc/program-governance.md`)
- Refreshes evidence on a schedule (below)
- Raises drift, exceptions, and risk entries when reality moves

A small shop may have three people owning everything; that is fine. The
failure mode is diffuse ownership, where every control belongs to "IT"
and none of them has been looked at since the assessment.

**Evidence refresh schedule.** Sort requirements into three buckets:

| Bucket | Examples | Refresh |
| --- | --- | --- |
| Machine-generated, always current | Audit logs (AU), config baselines (CM), MFA enforcement (IA) | Verify collection quarterly; sample monthly |
| Periodic artifacts | Training records (AT), access reviews (AC.L2-3.1.1), scan and remediation records (RA) | Produce on their natural cycle; owner confirms currency quarterly |
| Slow-moving documents | Policies, procedures, diagrams, agreements | Annual review, versioned, dated |

Store evidence the way `evidence-collection.md` describes, organized by
requirement, so an assessor request or a DIBCAC investigation is a
retrieval exercise rather than an archaeology project. Remember the
retention floor from certification assessments: hashed assessment
artifacts must be kept six years from the CMMC Status Date
(32 CFR 170.17(c)(4), 170.18(c)(4)).

---

## Annual Affirmations

Per 32 CFR 170.22 and DFARS 252.204-7021:

- **Who:** the Affirming Official, a senior representative responsible
  for CMMC compliance with authority to affirm continuing compliance.
  Name one, name a successor process, and keep contact info current in
  SPRS.
- **When:** upon achieving a Conditional status (where applicable), upon
  achieving a Final status, after every POA&M closeout, and annually
  after the Final status date. Every level, every year, including
  Level 1.
- **What:** an attestation that the organization has implemented and
  will maintain all applicable requirements for all systems in the
  assessment scope.
- **Consequence of lapse:** an expired or missing affirmation makes you
  ineligible for awards requiring that CMMC status, and a false
  affirmation is False Claims Act territory for both company and
  signer.

Treat the affirmation as the annual output of the monitoring program, not
a standalone signature. A defensible packet for the Affirming Official:
current SSP version and change log, POA&M status, the year's risk
assessment (see `grc/risk-management.md`), drift findings and their
resolutions, and vendor compliance confirmations (see
`grc/vendor-and-supply-chain.md`). The official signs what the program
proved.

Put all recurring dates on one compliance calendar: affirmation
anniversaries per scope, self-assessment refresh, triennial
reassessment lead time (start C3PAO scheduling 9 to 12 months out;
capacity is finite), POA&M 180-day deadlines, and evidence cycles.

---

## SPRS Score Maintenance

For contractors under DFARS 252.204-7019/7020, the NIST SP 800-171 DoD
Assessment score in SPRS must be current (not older than three years,
and accurate for the covered systems). Beyond the letter of the clause,
practical rules:

- **Rescore on material change.** Infrastructure moves, new enclave, a
  requirement that regressed from implemented to partial: recompute and
  resubmit rather than letting SPRS assert a stale 110.
- **Score drift is real.** A migration that drops FIPS-validated
  encryption in one segment moves SC.L2-3.13.11, a 3 or 5 point swing.
  Wire the change process to ask "does this move any requirement's
  status?" before approval.
- **Keep the basis of the score.** The scoresheet, per-requirement
  status, and date behind every SPRS submission should be reproducible;
  that is exactly what a DIBCAC review will ask for.

---

## Drift Detection

Certification-day compliance decays through ordinary operations. Watch
the four classic channels:

1. **Configuration drift.** Compare running state to documented baselines
   (CM.L2-3.4.1, 3.4.2) on a schedule; alert on unauthorized change
   (CM.L2-3.4.3). Endpoint and cloud posture tools make this cheap; see
   `modern-it/`.
2. **People drift.** Joiners, movers, leavers versus access lists
   (AC.L2-3.1.1), privileged role membership (AC.L2-3.1.5), and training
   currency (AT). Quarterly access review is the floor.
3. **Vendor drift.** ESP staffing changes, CSP service changes,
   FedRAMP authorization status changes for services you inherit
   controls from. Re-verify the entries in your responsibility matrix on
   a cycle. See `grc/vendor-and-supply-chain.md` and the dated
   verification stamps convention in `SOURCES.md`.
4. **Scope drift.** New projects, new data flows, shadow SaaS. A CUI
   flow that grew outside the boundary is the most expensive drift there
   is (anti-pattern 9). Re-ask the scoping questions from
   `scoping-and-cui.md` whenever the business changes shape.

Every drift finding gets one of three exits: fix it, run it through
change management with an SSP update, or write it into the risk register
with an owner and a date.

---

## Key Takeaways for Contractors

1. Three standing obligations survive certification: annual affirmations
   (170.22), accurate SPRS data (7019/7020, with DIBCAC's 7020
   investigation right), and ongoing monitoring (CA.L2-3.12.3).
2. Name a control owner for every requirement and put evidence refresh
   on a schedule with three buckets: machine-generated, periodic, and
   slow-moving.
3. Make the affirmation the annual output of the program: the Affirming
   Official signs a packet, not a blank line.
4. Rescore SPRS on material change, and keep the reproducible basis for
   every submitted score.
5. Hunt drift in four channels: configuration, people, vendors, scope.
   Every finding ends in a fix, a managed change, or a risk entry.
