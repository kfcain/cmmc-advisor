---
description: Attack the current scope, asset categorization, DFD, ESP story, and inheritance claims in assessor voice, ranked by thread-pull likelihood
argument-hint: "[program-data-path]"
disable-model-invocation: true
---

# Red-team scope: devil's advocate pass

Act as the skeptical Lead CCA at the scope-validation gate. The
challenge catalog is
`references/assessor-playbook/adversarial-challenge-catalog.md`; the
memory contract is in `references/assessor-playbook/README.md`. Resolve
these relative to the directory containing the plugin's SKILL.md.

## Locate the program data file

Same resolution as the grill command: `$ARGUMENTS` first token, then
`program.yaml` / `program-data.yaml` / `*.program.yaml` in the working
directory. With no file on hand: say there is nothing on file to attack,
offer the grill rail first, or attack a verbally described environment;
in that case create the minimal scaffold exactly as the grill command's
bootstrap step defines it, then persist what is learned into it.

## Session flow

1. Read the full program data: assets by 170.19(c) category, topology
   zones and flows, inheritance_sources, responsibility matrix, and the
   discovery section. Run
   `python3 <skill-root>/scripts/discovery_report.py <program-data>`
   when Bash is available.
2. Build the target list, highest-yield first:
   - every out-of-scope and CRMA claim
   - every inheritance assertion and its crm_ref
   - every boundary-crossing flow, and the quiet flows that are missing
     (backup, admin, hygiene, print/scan, monitoring)
   - every qa_log answer at confidence reported or assumed, and every
     stale answer the report flags
   - every ESP and each tool touching the boundary
   - unretired assumptions (each is a finding that has not happened yet)
3. Walk the challenge catalog group by group against the targets. Press
   one thread at a time in assessor voice: the challenge, the citation,
   the artifact that survives it. Let the user answer before moving on
   when running interactively; in report mode, mark each challenge
   survived, open thread, or finding-in-waiting from the data alone.
4. Emit the ranked challenge report in the catalog's output format,
   ending with the three threads to close before scheduling a C3PAO.
5. Write-back: new `open_questions` entries for every challenge the data
   could not answer (default behavior, announced up front). Substantive
   facts the user supplies while answering challenges append to
   `qa_log` under the standard memory contract (dated, confidence
   graded). Assumption confirmations and retirements only with
   consent. Never write conformity fields from this rail.
6. Run `discovery_report.py` after writes; fix any id-integrity errors.

## Rules

- Challenge content, not paperwork shape: one combined diagram covering
  network topology and CUI flow is fine; missing flows are not.
- Every challenge carries its citation (32 CFR 170.19, scoping guide,
  CAP, DoD CMMC FAQ entry); no vibes-based findings.
- Enabler posture even in adversary voice: every finding-in-waiting names
  the artifact or architecture change that closes it.
