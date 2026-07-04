# Mock Assessment Conduct

> Source: CMMC Assessment Process (CAP) v2.0 (The Cyber AB, December 2024); 32 CFR 170.17 and 170.19; NIST SP 800-171A; CMMC Assessment Guide Level 2 v2.13; Cyber AB CCA Certification Blueprint

How to run a mock assessment that behaves like the real thing. The
structure follows the CAP v2.0 phases (Conduct the Pre-Assessment;
Assess Conformity to Security Requirements; Complete and Report
Assessment Results; Issue Certificate and Close Out POA&M), compressed
for a mock. The
engine is `scripts/generate_mock_assessment.py`; this file is the conduct
around it. Interview craft lives in `interview-method.md`; POA&M and
closeout rules stay in `grc/assessment-operations.md` and
`poam-management.md`.

## What a mock is and is not

A mock predicts findings; it grants nothing. Two differences from a real
assessment cut in the OSC's favor and should be used:

- A real Lead CCA who reaches an adverse readiness determination delivers
  it in writing without remedial advice; conflict-of-interest rules bar
  the assessment team from consulting. A mock has no such bar: every
  finding here ends with remediation direction.
- A real assessment samples. A mock can go wider on the families the
  discovery record says are weak, because nothing is at stake yet.

What a mock must copy from the real thing: the scope gate, role-owner
interviews, objective-level scoring, and the evidence standard
(adequacy: the right evidence; sufficiency: enough of it).

## Step 1: Readiness check

Before any interview, verify the package an assessor would ask for on day
one:

1. SSP mapped to the objective level, all 320 objectives, not 110
   practice-level paragraphs. No rule requires an objective-level SSP;
   the mock demands it because scoring happens per objective, and OSCs
   that estimate scores from practice-level SSPs routinely land far
   lower when each objective is judged on its own.
2. Evidence mapped objective to document, section, and paragraph. Handing
   over a policy binder and inviting the assessor to find it fails the
   sufficiency standard.
3. Asset inventory by 170.19(c) category, network topology, and CUI flow
   documented (one combined diagram covering both network topology and CUI
   flow is fine; missing content is not).
4. All CAGE codes and physical locations enumerated; every CAGE code
   must be accounted for in the assessment's sampling approach and
   locations with differing controls draw samples (CAP 2.11-2.12).
5. The responsibility matrix and provider CRMs for every ESP and inherited
   claim.
6. `scripts/discovery_report.py` clean: untouched phases and open
   questions are scope-validation failures waiting to happen.

A mock can proceed with gaps here; log each as a finding first.

## Step 2: The scope-validation gate

The CAP makes scope validation a Phase 1 hard gate: the Lead CCA validates
the CMMC Assessment Scope against 32 CFR 170.19, and disagreements are
resolved before conformity assessment begins. The mock does the same, and
never starts family interviews first.

Run the asset-categorization, data-flow, and out-of-scope/inheritance
groups of `adversarial-challenge-catalog.md` (groups 1, 2, and 5)
against the program data file. Outcomes per challenge: survived,
not-applicable (nothing claimed), or logged as a scope finding
persisted to `discovery.open_questions` with an owner, matching the
red-team rail's write path. A scope finding that would move an asset
between categories changes which requirements apply, which is exactly
why the gate precedes the families.

Short-circuit rule: when a readiness gap makes an entire challenge
group unanswerable (no topology on file means every group 2 challenge
fails vacuously), log the gap once, mark the group blocked, and move
on; do not generate one finding per challenge for the same missing
artifact.

## Step 3: In-brief

Five minutes, in character:

- Scope being assessed (system name, boundary sentence, locations).
- Method: examine, interview, test per objective; objective-level scoring;
  MET requires every applicable objective MET.
- Who speaks: role owners answer their own functions
  (`interview-method.md`); it is fine to say "I need to check" and
  follow up; guessing is worse.
- Memory contract: answers land in the discovery log; conformity fields
  are written only with consent at the out-brief.

## Step 4: Per-family conduct

Generate the pack, then interview against it:

```bash
python3 scripts/generate_mock_assessment.py program.yaml --family AC -o exports/mock-ac
```

Conduct rules, mirroring the CAP's assessment phase:

- **E-I-T triad per objective.** The pack lists examine, interview, and
  test objects from the assessment-objective dataset. Evidence from the
  three methods must agree; a policy that says one thing while the admin
  describes another is a finding even when each looks fine alone.
- **Depth and coverage escalate on weakness.** A real assessment increases
  its sample the moment evidence looks questionable. Copy that: one vague
  answer on account reviews means pulling more accounts, not moving on.
- **Testing is the preferred method** where the guide expects hands-on
  verification: session lock, USB mount, clipboard redirection, FIPS mode.
  Ask for the demonstration, not the description of it.
- **Practice-based questions beat policy recital.** Ask for the artifact
  of the thing that should have happened recently: the access review from
  the in-scope quarter, the log review from a named week, the last
  incident-response test. These cannot be answered from a well-written
  policy alone.
- **Physical objectives get flagged, not skipped.** CAP P.11 lists
  eighteen objectives where the assessment team should consider the
  optimal logistical approach (virtual vs in-person): CM.L2-3.4.5[d];
  MA.L2-3.7.2[d]; MP.L2-3.8.1[c][d]; MP.L2-3.8.4[a][b];
  PE.L1-3.10.1[b][c][d]; PE.L2-3.10.2[a][b][c][d];
  PE.L1-3.10.3[a][b]; PE.L1-3.10.5[b][c]; and the SC.L2-3.13.12
  collaborative-computing objective. In a remote mock, simulate what
  can be simulated (camera walk-through) and mark the rest "requires
  on-site validation" rather than MET.
- **Score as you go.** Per assessment objective: MET, NOT MET, NOT
  APPLICABLE (with the justification an assessor would accept), or NEEDS
  EVIDENCE (mock-only status: the claim is plausible and the artifact was
  not produced). A practice is MET only when every applicable objective
  is.

## Step 5: Daily checkpoint

End each family or each day with two lists:

- **Contradiction register:** every place examine, interview, and test
  disagreed, with both versions. These become findings unless resolved.
- **Evidence debt:** every NEEDS EVIDENCE with a named owner and artifact.
  In a real assessment the window for additional evidence on NOT MET
  items is bounded: 10 business days following the active assessment
  period (CAP 2.15; 32 CFR 170.17(c)(2)); rehearse producing artifacts
  inside days, not weeks.

## Step 6: Out-brief and findings report

The report, in assessor structure:

1. **Scope validation results** first: challenges run, survived, findings.
2. **Per-objective results** by family: status, method basis (what was
   examined, who was interviewed, what was tested), and the finding
   narrative for every NOT MET in determination language ("the
   organization did not demonstrate that...").
3. **SPRS delta:** computed score from the mock results vs the score
   currently asserted, using the DoD methodology weights
   (`scripts/generate_dashboard.py` computes it from the program data).
4. **POA&M eligibility preview:** which NOT METs could ride a POA&M under
   32 CFR 170.21 and which (the never-POA&M list, point values above the
   threshold) could not; `scripts/validate_poam.py` checks this.
5. **Remediation direction** per finding, the part a real adverse
   determination would omit.
6. **The re-test list:** what to re-verify before the real assessment,
   starting with everything scored NEEDS EVIDENCE and every contradiction.

## Step 7: Writing results back

Findings live in the report by default. With explicit consent at the
out-brief, write per-objective `conformity` and `statement` fields into
the program data file, and stamp each written objective with a `qa_log`
entry recording that the value came from a mock assessment on that date.
Open questions and assumptions raised during the mock are written as part
of the default memory contract, announced at the in-brief.

Re-run after writes:

```bash
python3 scripts/discovery_report.py program.yaml
python3 scripts/validate_poam.py program.yaml
```
