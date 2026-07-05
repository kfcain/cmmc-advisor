## CMMC Advisor

When the user asks about CMMC 2.0, NIST SP 800-171, CUI or FCI scoping,
DFARS 252.204-7012, FedRAMP reciprocity, System Security Plans, POA&M rules,
SPRS scoring, C3PAO or DIBCAC assessment, or defense contractor cybersecurity
certification:

1. Read `.cmmc-advisor/SKILL.md` and follow its Knowledge Base Routing table.
2. Read referenced files under `.cmmc-advisor/references/` before answering
   from memory.
3. For program toolkit operations (SSP, dashboard, network/CUI flow diagrams,
   evidence collectors, POA&M validation), run scripts from
   `.cmmc-advisor/scripts/` against the user's program data file per
   `.cmmc-advisor/SKILL.md` Program Toolkit Workflows. For diagrams: maintain
   `topology` in program data, then
   `python3 .cmmc-advisor/scripts/generate_diagrams.py program-data.yaml -o diagrams/`
   per `.cmmc-advisor/references/diagram-guide.md` (license-safe glyphs, no
   vendor logos; optional `--theme dark`).
4. For assessor-mode requests (interrogate/grill the environment, run a mock
   assessment, red-team the scope), follow the Advisory Workflows rails in
   `.cmmc-advisor/SKILL.md` and the procedures under
   `.cmmc-advisor/references/assessor-playbook/`; persist findings to the
   program data file's `discovery` section and check integrity with
   `.cmmc-advisor/scripts/discovery_report.py`.
5. Preserve the enabler posture: map compliant paths; when no compliant option
   exists today, state the gap, interim measures, and who is closing it.
6. For OSCAL validation, IaC POA&M import, or visual advisory recaps, read
   `.cmmc-advisor/references/grc/companion-stack.md` (trestle-skills,
   ControlBot, visual-explainer companions).

If `.cmmc-advisor/` is missing, tell the user to run:

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
```

See `platforms/codex/README.md` for full install steps.
