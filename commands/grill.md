---
description: Interrogate the OSC environment like a Lead CCA, one discovery phase at a time, and persist everything learned to the program data file
argument-hint: "[program-data-path] [phase]"
disable-model-invocation: true
---

# Grill: scope discovery interrogation

Act as a Lead CCA running scope discovery. The question bank is
`references/assessor-playbook/scope-discovery-question-bank.md` (twelve
phases); interview craft is
`references/assessor-playbook/interview-method.md`. Resolve these
relative to the directory containing the plugin's SKILL.md.

## Locate the program data file

1. `$ARGUMENTS` first token, if given.
2. Otherwise look in the working directory for `program.yaml`,
   `program-data.yaml`, then any `*.program.yaml`.
3. If none exists, say so and offer to bootstrap one: ask for the
   organization name, system name, and CMMC level, then write a minimal
   `program.yaml` conforming to `templates/program-data.schema.json`:

   ```yaml
   organization:
     name: <org name>
     system_name: <system name>
   assessment:
     level: "2"
   requirements: {}
   discovery:
     updated: "<today>"
     phases: {}
     qa_log: []
     assumptions: []
     open_questions: []
     decisions: []
   ```

   Leave `phases` empty (the report treats absent phases as
   not-started). Quote every date as a string; unquoted YAML dates
   parse as date objects and fail schema validation. The level may be
   a quoted string or an integer. Never write into the plugin's own
   `templates/` directory.

## Session flow

1. Run `python3 <skill-root>/scripts/discovery_report.py <program-data>`
   when Bash is available; otherwise read the `discovery` section
   directly. Report phase coverage and pick up where it left off.
2. Choose the phase: `$ARGUMENTS` second token if given, else the first
   phase whose status is `revisit` or `in-progress`, else the first
   `not-started` phase in bank order. One phase per session by default;
   offer to continue when the phase completes early.
3. Interrogate per the bank's core questions and follow-up logic. Ask one
   question at a time. Push for focused answers (named documents, named
   mechanisms, named owners) per the interview method; accept "I need to
   check" and log it rather than accepting a guess.
4. Record as you go, per the memory contract in
   `references/assessor-playbook/README.md`:
   - every answer to `discovery.qa_log` (id `QA-NNNN`, date, phase,
     answered_by, confidence: verified only when evidence was shown,
     reported when asserted, assumed when inferred)
   - inferences to `discovery.assumptions` with risk_if_wrong
   - unanswered items to `discovery.open_questions` with owner and
     why_it_matters
   - scoping calls to `discovery.decisions`
   - update `discovery.phases.<id>` status and summary, and
     `discovery.updated`
5. When answers change the asset inventory or topology, propose the exact
   edit (asset name, 170.19(c) category, notes, discovery_refs; topology
   nodes and flows) and apply it only on confirmation.
6. Close the session with: the discovery report summary, the phase's exit
   criteria met or missed, and the top three open questions with owners.
7. When the session summary exceeds terminal-friendly size (roughly 4+ rows
   in a table), offer a visual-explainer HTML recap per
   `references/grc/companion-stack.md` and `platforms/visual-explainer/`.

## Rules

- Assessor posture, enabler voice: every gap found comes with the next
  step, never a bare refusal.
- Do not write per-objective conformity fields from this rail.
- Do not restate asset-baseline content; point to
  `references/modern-it/asset-baselines/` for per-asset hardening depth.
- Run `discovery_report.py` after writes; fix any id-integrity errors it
  reports before ending the session.
