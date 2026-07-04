---
description: Run a CAP-faithful mock assessment with the scope-validation gate first, objective-level scoring, and a findings out-brief
argument-hint: "[program-data-path] [family]"
disable-model-invocation: true
---

# Mock assess: CAP-faithful dry run

Act as the assessment team lead for a mock. Conduct rules are in
`references/assessor-playbook/mock-assessment-conduct.md`; interview
craft in `references/assessor-playbook/interview-method.md`; challenge
material in `references/assessor-playbook/adversarial-challenge-catalog.md`.
Resolve these relative to the directory containing the plugin's SKILL.md.

## Locate the program data file

Same resolution as the grill command: `$ARGUMENTS` first token, then
`program.yaml` / `program-data.yaml` / `*.program.yaml` in the working
directory. With no file, offer the grill rail first; a mock needs
something on file to assess.

## Session flow

1. **Readiness check** per the conduct guide: SSP at objective level,
   evidence mapped to document and section, inventory by category,
   network topology and CUI flow documented, CAGE codes and locations,
   CRMs for every ESP. Log gaps as findings; proceed anyway if asked.
2. **Scope-validation gate.** Run the categorization, DFD, and
   out-of-scope/inheritance groups of the challenge catalog against the
   program data. Do not start family interviews until each challenge is
   survived or logged as a scope finding. If the user asks to skip to a
   family, explain the gate (CAP Phase 1 resolves scope disputes before
   conformity assessment) and get explicit confirmation to proceed with
   the gate unfinished, logging that decision.
3. **In-brief** per the conduct guide: scope sentence, method, role-owner
   rule, memory contract (open questions and assumptions write by
   default; conformity writes only with consent at the out-brief).
4. **Per-family conduct.** Family from `$ARGUMENTS` second token, else
   let the user pick, weakest-first per the discovery record. Generate
   the pack with
   `python3 <skill-root>/scripts/generate_mock_assessment.py <program-data> --family <X>`
   when Bash is available; otherwise interview from the assessment
   objectives in `references/data/assessment-objectives.json` and the
   family file under `references/assessment-objectives/`. Apply E-I-T
   triad rules, sampling escalation on vague answers, test-preferred
   verification, and flag the CAP in-person objectives as
   requires-on-site rather than MET.
5. **Score per objective**: MET, NOT MET, NOT APPLICABLE (with the
   justification an assessor would accept), or NEEDS EVIDENCE. A practice
   is MET only when every applicable objective is. Keep the contradiction
   register and evidence-debt list as you go.
6. **Out-brief** per the conduct guide: scope results first, then
   per-objective results with method basis and determination-language
   findings, SPRS delta, POA&M eligibility preview
   (`python3 <skill-root>/scripts/validate_poam.py <program-data>`),
   remediation direction per finding, and the re-test list.
7. **Write-back with consent.** Ask once at the out-brief: write mock
   results into per-objective conformity and statement fields? On yes,
   write them and stamp each written objective with a qa_log entry
   (mock-sourced, dated). Open questions and assumptions write by
   default. Re-run `discovery_report.py` and `validate_poam.py` after
   writes.

## Rules

- A mock ends with remediation direction; say plainly that a real Lead
  CCA delivering an adverse determination cannot provide it, and this is
  the OSC's chance to use that difference.
- Never present mock results as certification outcomes.
- Score at the objective level only; no practice-level shortcuts.
