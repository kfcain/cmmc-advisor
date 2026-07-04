# Level 1 Affirmation Readiness: Fast, Gated, Defensible

> Source: 32 CFR 170.15, 170.19(d), 170.22; FAR 52.204-21; DoD CMMC
> Assessment Guide Level 1 v2.13; 31 U.S.C. 3729-3733 (False Claims
> Act); DOJ Civil Cyber-Fraud Initiative and settlement releases per
> SOURCES.md (Legal and Enforcement section)

Level 1 is the fastest path in CMMC: 15 security requirements from FAR
52.204-21 (the model's 17 practices), an annual self-assessment you run
yourself, results entered in SPRS, no C3PAO, no waiting. A small
FCI-only shop can be legitimately done in weeks. This file exists
because the same speed makes Level 1 the easiest place to sign a false
statement to the federal government. The fast path works only with the
gates in front of it.

This is compliance guidance, not legal advice; involve counsel on FCA
exposure questions.

## Why the affirmation is the serious part

Every self-assessment ends with an affirmation: a senior official (the
Affirming Official, who per 32 CFR 170.22 is responsible for ensuring
compliance) affirms continuing compliance with all requirements,
electronically, in SPRS, after the assessment and annually thereafter.
That is a representation to the government, renewed every year, with a
name on it.

The False Claims Act is the enforcement mechanism. Since the DOJ Civil
Cyber-Fraud Initiative (announced October 6, 2021 by Deputy Attorney
General Lisa Monaco) the Department has used the FCA specifically
against contractors that knowingly misrepresent cybersecurity
practices. The mechanics that matter to a small contractor:

- Treble damages plus a per-claim civil penalty (currently $14,308 to
  $28,619 per claim after DOJ's 2025 inflation adjustment), and every
  invoice under the contract can count as a claim.
- Qui tam: any insider (31 U.S.C. 3730) can file on the government's
  behalf and keep 15 to 30 percent of the recovery. The relators in
  the cases below were a cybersecurity director, a CIO, and staff
  engineers. The person most likely to know your affirmation is wrong
  has a financial incentive to say so.
- The CMMC final rule preamble acknowledged commenters' FCA concerns
  and answered that DoD lacks authority to change the FCA. The
  exposure is not hypothetical preamble text; it is enforcement
  practice:

| Case | Year | Amount | What was misrepresented |
|------|------|--------|------------------------|
| Aerojet Rocketdyne | 2022 | $9M | DFARS 252.204-7012 / NIST 800-171 compliance while signing DoD and NASA contracts; qui tam by its own cybersecurity director |
| Verizon Business | 2023 | ~$4.1M | Required security controls (including FIPS-validated crypto) on a federal internet service; self-disclosed and earned cooperation credit |
| Insight Global | 2024 | $2.7M | Data security on public-health contact-tracing work; qui tam by a staff member |
| Penn State | 2024 | $1.25M | SPRS scores and implementation timelines across 15 contracts; non-equivalent cloud provider; qui tam by a lab CIO |
| MORSECORP | 2025 | $4.6M | Submitted SPRS score of 104 when a consultant later scored -142; left it uncorrected for years |
| Georgia Tech Research Corp | 2025 | $875K | Submitted an SPRS score premised on a "fictitious" environment that applied to no real system |

The pattern across every case: the score or attestation described an
environment that did not exist as described. Nobody in the table was
pursued because a control failed; they were pursued for saying it
existed.

## The gated fast path

Four gates. Each is cheap compared to the table above. Everything
learned persists to the program data file's `discovery` section so the
work survives staff turnover and feeds next year's cycle.

**Gate 1: Scope truth (the hidden-CUI check).** The most dangerous L1
mistake is not a weak control; it is self-scoping as FCI-only while
CUI actually flows. Run the grill rail's contracts-cui phase
(`references/assessor-playbook/scope-discovery-question-bank.md`
Phase 1) against three recent deliverables, the contract clauses, and
what actually arrives from the government or the prime. DFARS 7012 in
the contract is the signal to look harder, not proof either way
(`references/scoping-and-cui.md`). If CUI appears, stop: you are
having a Level 2 conversation, and affirming Level 1 anyway is the
Georgia Tech fact pattern. Record the check's outcome as a dated
`qa_log` entry; it is the artifact that shows the scoping was
diligent, not assumed.

**Gate 2: Objective-level gap assessment.** All 15 requirements must
be MET; Level 1 permits no POA&Ms (32 CFR 170.15), so any gap is a
blocker, not a milestone. Assess at the assessment-objective level
using the AG L1 objectives (the L1 counterpart rows in
`references/assessment-objectives/`), not by reading the 15 one-line
requirements and nodding. The scrutiny rails apply at L1: run the
red-team rail against the file (the categorization and physical
challenges bite hardest for small shops) and a mock pass on the six
families L1 touches.

**Gate 3: Evidence per practice, dated.** For each requirement,
capture the artifact that shows it operating: the firewall rule
export, the visitor log page, the sanitization record, the account
list against the HR roster. Intentions and policy statements are what
the settlements were built on. `scripts/generate_l1_package.py`
assembles the package and refuses to bless a requirement with no
evidence on file.

**Gate 4: The affirmation packet.** Before anyone clicks in SPRS:
name the Affirming Official in the program data file and brief them
that the affirmation is their representation, renewed annually; hand
them the package from Gate 3 plus the Gate 1 scoping record; calendar
the annual re-run (the affirmation recurs annually per 170.22, and an
affirmation on stale facts is the MORSECORP fact pattern). Verizon's
entry in the table is the other lesson: discovering a problem and
self-disclosing earned measurable credit.

## Automating the cycle

```bash
python3 scripts/generate_l1_package.py program.yaml -o exports/l1-package
```

The package generator reads the program data file, maps the 15 FAR
requirements through the model's 17 practices to their Level 2
identifiers (from `references/data/assessment-objectives.json`), and
emits the self-assessment worksheet with per-requirement status,
evidence on file, and the affirmation-readiness verdict. It exits
nonzero, listing the blockers, when any mapped requirement is not MET,
lacks evidence, or the Gate 1 scoping record is missing. Run it before
the first affirmation and every year before the re-affirmation; green
output plus the evidence bundle is the packet the Affirming Official
signs on.

The rest of the toolkit applies unchanged: the grill rail builds the
discovery memory, `scripts/discovery_report.py` shows staleness before
each annual cycle, and the dashboard renders the L1 program the same
way it renders L2.

## When not to self-attest

- Gate 1 found CUI, or flows nobody can explain: resolve scope first
  (`references/scoping-and-cui.md`, `level-1-quickstart.md` "Are You
  Actually Level 1?").
- Any requirement is not MET: fix it first. There is no conditional
  status and no POA&M at Level 1; affirming around a known gap is the
  exact conduct the Civil Cyber-Fraud Initiative exists to reach.
- The package describes the environment you intend to build this
  quarter: affirm after it exists. Every case in the table is a
  version of affirming the intended environment instead of the real
  one.

The same logic scales up: a Level 2 self-assessment's SPRS score and
affirmation carry identical FCA mechanics with 110 requirements'
worth of surface. The gates here are the L1-sized version of the full
assessor-mode rails; use those (`references/assessor-playbook/`) when
the contract is Level 2.
