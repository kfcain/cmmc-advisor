# CMMC Advisor

A multi-platform agent skill for working through CMMC 2.0 (Cybersecurity Maturity Model Certification) compliance. Built for defense contractors who deliver services to the U.S. Government and need clear, actionable guidance on cybersecurity certification requirements. Ships adapters for Claude Code, Cursor, and Codex from one knowledge base.

## Philosophy

This skill exists to help businesses succeed in delivering great services to the U.S. Government in a compliant way. It is not a tool to say no. It is a tool to say **how**.

When a compliant path exists, the skill maps it clearly. When no compliant option exists today, the skill identifies the gap, describes who in the industry is working on closing it, and estimates when options may become available. Legitimate gaps in the market deserve honest answers, not dead ends.

## What This Covers

All three CMMC levels: Level 1 (Foundational), Level 2 (Advanced), Level 3 (Expert). 14 domains, 110 practices with full implementation guidance mapped from NIST SP 800-171 Rev 2, plus a dedicated Level 1 quickstart for FCI-only shops (the 15 FAR 52.204-21 requirements, annual self-assessment, SPRS affirmation) and a full Level 3 reference covering all 24 NIST SP 800-172 enhanced requirements with DoD-assigned ODPs, DIBCAC assessment process, Level 3 scoping, and POA&M limits. Assessment preparation for self-assessment, C3PAO, and DIBCAC paths. CUI scoping covering boundary definition, FCI vs CUI, and enclave strategies. SSP guidance and POA&M management.

Modern IT compliance mapping for real-world stacks:

- Cloud platforms. AWS GovCloud, Azure Government, GCP Assured Workloads, and hybrid patterns.
- Productivity suites. Microsoft 365 GCC and GCC High, Google Workspace, Atlassian Government Cloud, ServiceNow GCC, GitHub Enterprise, Box for Government.
- AI services. FedRAMP-authorized (Amazon Bedrock GovCloud, Azure OpenAI Government, Vertex AI Assured Workloads), self-hosted (Coder, on-prem LLM, air-gapped), and AI dev tools (Claude Code, Copilot Enterprise, Cursor, Windsurf, Continue).
- Endpoint management. macOS, Windows STIG baselines, remote work.

A program toolkit: a machine-readable dataset of all 110 requirements and 320 NIST SP 800-171A assessment objectives (with SPRS weights and assessment methods), a program data file schema that tracks per-objective conformity, narratives, evidence links, inheritance, and POA&M items, and a generator that produces a complete AO-level System Security Plan in Markdown or DOCX.

A GRC program layer covering the risk management program (register design, acceptance workflow, cadence), continuous monitoring between assessments (control owners, annual affirmations, SPRS score maintenance, drift detection), vendor and supply chain treatment (ESP/MSP/MSSP rules under the final rule, FedRAMP Moderate equivalency, subcontractor flowdowns), and program governance (roles, policy lifecycle, change management, 72-hour DIBNet incident reporting readiness).

Contractor-specific guidance by company size (small, medium, large) and socioeconomic set-aside (SDVOSB, 8(a), WOSB/EDWOSB, HUBZone).

FedRAMP Marketplace practitioner guide with curated category short-lists, search guidance, and coverage-gap analysis.

Rev 3 transition context (current Rev 2 requirements with Rev 3 awareness).

Anti-patterns catalog: sixteen named compliance-theater patterns across documentation, tool, scope, and assessment categories.

Assessor-mode rails: a Lead CCA persona on the OSC's side of the table. Scope discovery interrogation across twelve phases (contracts, people, locations, tenancy seams, endpoints, dev/DevOps/AI, physical media, OT, ESP access paths, audit and SIEM operations, data flows, backup/DR) with persistent per-OSC memory in the program data file; CAP-faithful mock assessments with the scope-validation gate first and objective-level scoring; and a devil's-advocate rail that attacks asset categorization, DFD completeness, enclave integrity, ESP stories, and inheritance claims with a citation behind every challenge. Installed as a plugin these are `/cmmc-advisor:grill`, `/cmmc-advisor:mock-assess`, and `/cmmc-advisor:red-team-scope`.

See [ROADMAP.md](ROADMAP.md) for the staged expansion into multi-framework federal GRC coverage (policy-to-control mapping, 800-53/FedRAMP crosswalks, OSCAL, FedRAMP 20x, evidence automation).

**Companion stack:** optional trestle-skills, ControlBot, and visual-explainer
repos extend OSCAL validation, IaC POA&M import, and advisory HTML recaps.
See [references/grc/companion-stack.md](references/grc/companion-stack.md).
Most evidence collectors emit sample/`live_stub` output until the org wires
live APIs or external GRC inspector plugins (Meridian covers live GCP ConMon).

**Capability guide:** open [docs/capability-guide.html](docs/capability-guide.html) in a browser for a self-contained map of every feature, script, dataset, platform adapter, and known limitation in this repository.

## Installation

One knowledge base (`SKILL.md` + `references/` + `scripts/`). Pick your platform.
Full cross-platform notes: [platforms/README.md](platforms/README.md).

### Claude Code

Plugin (skill plus the assessor-mode slash commands):

```
/plugin marketplace add kfcain/cmmc-advisor
/plugin install cmmc-advisor@cmmc-advisor
```

Or copy the repo as a plain skill:

```bash
git clone https://github.com/kfcain/cmmc-advisor.git
cp -r cmmc-advisor ~/.claude/skills/cmmc-advisor
# or project-scoped: cp -r cmmc-advisor .claude/skills/cmmc-advisor
```

Details: [platforms/claude/README.md](platforms/claude/README.md)

### Cursor

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
mkdir -p .cursor/skills .cursor/rules
ln -sf ../../.cmmc-advisor .cursor/skills/cmmc-advisor
ln -sf ../../.cmmc-advisor/platforms/cursor/rules/cmmc-advisor.mdc .cursor/rules/cmmc-advisor.mdc
```

Details: [platforms/cursor/README.md](platforms/cursor/README.md)

### Codex / OpenAI agents

Add the CMMC Advisor submodule, then merge the bootstrap block from
[platforms/codex/AGENTS.md](platforms/codex/AGENTS.md) into your project
`AGENTS.md`.

Details: [platforms/codex/README.md](platforms/codex/README.md)

### GRC platforms (Vanta, Drata, Secureframe, Paramify)

Connect vendor MCP servers **and** the local cmmc-advisor MCP in your compliance
program repo. Import platform monitor data into `program-data.yaml`; regenerate
SSP/dashboard/SPRS from the same file.

Details: [references/grc/grc-platform-mcp-bridge.md](references/grc/grc-platform-mcp-bridge.md) and [platforms/toolkit/mcp.json](platforms/toolkit/mcp.json)

## Usage Examples

```
"What CMMC level do I need for a DoD subcontract that handles CUI?"

"We use Google Workspace and macOS. Can we achieve Level 2 compliance?"

"Design a CUI enclave for a 30-person company using AWS GovCloud."

"What evidence do I need to collect for the Access Control domain?"

"We want to use AI coding tools in our development workflow. What are the compliant options?"
```

## Sources

Every factual claim in this skill traces to a publicly available source. See [SOURCES.md](SOURCES.md) for the complete provenance list.

Primary sources include:
- NIST SP 800-171 Revision 2 and SP 800-171A (Assessment Procedures)
- 32 CFR Part 170 (CMMC Program Final Rule) and 48 CFR acquisition rule
- CMMC Assessment Guide Level 2 (dodcio.defense.gov)
- DoD CSP SRG v1r1 (public.cyber.mil) for DoD Impact Level reciprocity
- FedRAMP Marketplace (fedramp.gov) for authorization status
- NIST CMVP Validated Modules Registry (csrc.nist.gov) for FIPS validation
- SBA regulations (13 CFR Parts 121/124/126/127/128) for contractor profiles
- Cloud provider compliance documentation (AWS, Microsoft, Google Cloud)
- Vendor trust centers for each named product

Compliance facts that depend on current authorization state (per-service FedRAMP status, per-model availability, vendor product scope) carry dated verification stamps inline, typically "verified 2026-04-21 via [URL]." Re-verify at the primary source before citing in an SSP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Key requirement: every factual claim must cite a public source.

## Disclaimer

This skill provides compliance guidance based on publicly available documentation. It is not legal advice, it is not a substitute for professional cybersecurity consultation, and it does not constitute an official assessment or certification. Always verify guidance against current authoritative sources and consult qualified professionals for your specific situation.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Lloyd Evans.

Free to use, modify, and redistribute, including commercially. If you fork, adapt, or build on this skill, keep the copyright notice and license text intact. Attribution in a visible place (README, about page, skill frontmatter) is appreciated but not legally required beyond what the license specifies.
