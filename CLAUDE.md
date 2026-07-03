# Project Instructions for AI Agents

This repository distributes the `cmmc-advisor` Claude Code skill. It ships a full SKILL.md plus a `references/` knowledge base, and carries its own eval runner under `evals/` so the skill's answer quality is measurable against curated scenarios and a rubric.

## Scope

Do not treat this repo as a general code project. It is a content-first artifact:

- `SKILL.md` defines the advisor persona, routing table, advisory workflow rails, and program toolkit workflows.
- `references/` holds every factual claim the skill cites: all 14 domain files, the assessment-objective layer (`assessment-objectives/`, all 320 NIST SP 800-171A objectives), levels (including `level-1-quickstart.md` and `level-3-expert.md`), scoping, SSP/POA&M/evidence guidance, the GRC program layer (`grc/`), the Rev 2 to Rev 3 crosswalk, FedRAMP mapping, and modern IT mapping. Machine-readable data lives under `references/data/` (assessment-objectives.json, fedramp-snapshot.json).
- `templates/` and `scripts/` carry the program toolkit: the program data schema and sample, the AO-level SSP structure and generator, and the self-contained HTML program dashboard and its generator. These are part of the distribution.
- `evals/` tests the skill's answers against real CMMC scenarios. The runner loads the real SKILL.md with Read/Grep/Glob enabled so routing is exercised; `evals/runner/lint.py` is the deterministic voice/citation lint that CI runs (`.github/workflows/content-lint.yml`).
- `SOURCES.md` lists the public DoD and NIST sources behind every factual claim. Any new factual assertion must cite a source in `SOURCES.md` before it lands.

## Philosophy

From `README.md`: this skill is an enabler, not a gatekeeper. When a compliant path exists, map it clearly. When no compliant option exists today, identify the gap honestly, describe who is working on closing it, estimate when options may become available, and suggest interim measures.

Every change must preserve that posture. Answers that block, hedge, or refuse without offering a path forward are failures regardless of factual accuracy.

## Evals

The eval runner at `evals/runner/` invokes Claude as the subject (using the skill), captures the answer, runs a deterministic precheck for required CMMC vocabulary and voice discipline, then scores the answer against a rubric via a second Claude call.

Usage (run from repo root):
```bash
pip install -r evals/runner/requirements.txt
python -m evals.runner.runner evals/scenarios/level-2-scoping-basic.yaml
```

Add scenarios under `evals/scenarios/` as YAML. Add rubrics under `evals/rubrics/` as Markdown. The format is intentionally small so contributors can extend coverage without harness work.

## Source discipline

Every factual claim in the skill (control text, assessment procedures, CMMC level definitions, acronyms, deadlines) must trace to a source in `SOURCES.md`. Interpretive guidance (when to choose which cloud, how to draft an SSP narrative) does not require citation but must not contradict cited sources.

When an AI agent edits any file under `references/` or `SKILL.md`, it must:
1. Verify the factual claim is already in `SOURCES.md` or add the source there.
2. Prefer linking to the authoritative URL over paraphrasing memory.
3. Flag any claim it cannot source rather than guessing.

## Voice

Same voice discipline as the wider Igris-family content: no em dashes, no slop words (delve, utilize, tapestry, paradigm, leverage as verb, etc.), no hedging filler ("It's worth noting", "Importantly"), no teacher voice ("Let me explain"). The skill speaks practitioner-to-practitioner to compliance officers, security engineers, and contracting officers.

## When to use which agent

- Content work on `SKILL.md` or `references/`: edit directly; run `python3 evals/runner/lint.py` and the eval runner to confirm no regression on existing scenarios.
- All 14 domain files exist, plus the full assessment-objective layer. New content should extend coverage (ROADMAP.md phases) with at least one eval scenario per new capability.
- Factual data changes (AO dataset, crosswalk, SPRS weights): regenerate from primary sources programmatically and re-verify counts (110 requirements, 320 objectives, -203 floor; crosswalk 77 + 33 = 110, 97 Rev 3); never hand-edit numbers from memory.
- Eval runner changes: small repo, direct edits are fine; tests are the scenario runs themselves.

## What this repo does NOT carry

- No hooks, no agents dir, no settings.json, no soul.md. This is a skill distribution, not a Claude Code harness host. Harness-level governance (hooks, agents, settings) lives in the author's separate Claude Code harness repo and is out of scope here.
