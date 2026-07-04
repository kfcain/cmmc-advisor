# Assessor Playbook

> Source: CMMC Assessment Process (CAP) v2.0 (The Cyber AB, December 2024); 32 CFR Part 170 (170.4, 170.19); DoD CMMC Assessment and Scoping Guides v2.13; NIST SP 800-171A; practitioner sources per SOURCES.md

Assessor-side scrutiny, distilled for the OSC's benefit. These files let the
skill act like a Lead CCA and a CCP at the same time: interrogate the
environment the way an assessor would, attack the scope before an assessor
does, and run mock assessments that follow the real CAP flow. Everything an
assessor could pull on, pulled first, on the OSC's side of the table.

## The four files

| File | Rail | What it carries |
|------|------|-----------------|
| `scope-discovery-question-bank.md` | Grill (`/cmmc-advisor:grill`) | Twelve interrogation phases covering every nook of an OSC environment, with entry and exit criteria and follow-up logic |
| `adversarial-challenge-catalog.md` | Red team (`/cmmc-advisor:red-team-scope`) | Challenges in assessor voice against asset categorization, DFDs, enclave integrity, ESP stories, out-of-scope and inheritance claims, and physical/OT scope |
| `mock-assessment-conduct.md` | Mock assess (`/cmmc-advisor:mock-assess`) | CAP-ordered conduct for a mock: readiness, the scope-validation gate, per-family interviews, objective-level scoring, out-brief |
| `interview-method.md` | Shared | How assessors select interviewees, judge answers, and escalate sampling; used by both the grill and the mock |

## The memory contract

Everything these rails learn lands in the `discovery` section of the
program data file (`templates/program-data.schema.json`):

- Answers go to `qa_log` with a date, the answering role, and a confidence
  grade: `verified` (evidence seen), `reported` (asserted, not shown), or
  `assumed` (inferred).
- Facts inferred rather than stated go to `assumptions` with the risk if
  wrong.
- Anything unanswered goes to `open_questions` with what an assessor does
  with the unanswered version.
- Scoping calls with rationale go to `decisions` so later sessions do not
  relitigate them.
- Interrogation progress is tracked per phase in `phases`. Status
  transitions: `not-started` until the first question of the phase is
  asked; `in-progress` while core questions or exit criteria remain,
  including when the only remainder is open questions awaiting owners;
  `complete` only when the phase's exit criteria in the question bank
  are met; `revisit` when a later answer invalidates something the
  phase recorded (an acquisition, a platform migration, a retired
  assumption that was wrong). Open questions do not block `complete`
  by themselves unless the exit criteria name them.

`scripts/discovery_report.py` prints coverage, staleness, and id integrity.
Mock-assessment findings write into per-objective conformity fields only
with explicit user consent; discovery writes are default behavior and are
announced up front.

## Source discipline

Rule text controls: 32 CFR Part 170, the CAP, the assessment and scoping
guides, and NIST SP 800-171A. The DoD CMMC FAQ is DoD's own interpretation
and is cited by entry id where used. Practitioner sources (C3PAO and RPO
publications, assessor commentary) are interpretation, flagged as such
inline, and each traces to an entry in `SOURCES.md` with a note to verify
against current rule text.
