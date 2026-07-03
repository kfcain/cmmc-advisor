# Roadmap: From CMMC Advisor to Federal GRC Capability

The current release is CMMC-complete: all three levels, all 320
assessment objectives, the GRC program layer, the Rev 2 to Rev 3
crosswalk, and the program toolkit (AO-level SSP generation, the
program dashboard, inherited-controls mapping). The phases below stage
the expansion into a broader federal GRC capability. Each phase lands
with sources in `SOURCES.md`, routing rows in `SKILL.md`, and at least
one eval scenario, per `CLAUDE.md`.

## Phase 2: Policy-to-Control Mapping Register (PCMR) — DELIVERED

Shipped: `references/grc/policy-mapping.md` (method and gap taxonomy),
the `policies` section of the program data schema with a worked sample,
the dashboard's Policies view (computed coverage, overdue reviews,
uncovered-requirements list), and the `grc-policy-mapping` eval
scenario. Remaining depth for a later pass: statement-level mapping
(individual policy clauses to assessment objectives) and automated
policy-document parsing.

## Phase 3: Multi-Framework Crosswalks and OSCAL — DELIVERED

Shipped: `references/data/800-53-crosswalk.json` (110 requirements, 127
unique 800-53 controls, FedRAMP Moderate baseline membership from NIST
OSCAL content), `scripts/build_800_53_crosswalk.py` (regenerator from
Appendix D tables + baseline fetch), `references/multi-framework-crosswalk.md`
(method, ISO 27001 notes, OSCAL workflow), `scripts/generate_oscal_ssp.py`
(OSCAL SSP emission with inheritance components and back-matter), SKILL.md
routing and toolkit workflow rows, CI crosswalk integrity check, and the
`toolkit-oscal-crosswalk` eval scenario. Narrative depth remains in
`references/fedramp-gap.md`; the dataset is the machine-readable layer.

## Phase 4: FedRAMP 20x and Trust Center Interop — DELIVERED

Shipped: `scripts/build_frmr_snapshot.py` and
`references/data/frmr-snapshot.manifest.json` (KSI catalog from FedRAMP
Consolidated Rules JSON merged with Marketplace vendor fields),
`references/fedramp-20x-ksi-due-diligence.md` (FRMR/KSI/trust-center due
diligence method), `scripts/generate_trust_center.py` and
`templates/program-trust-center.html` (deny-by-default public page from
program data), `references/grc/trust-center.md` (public vs internal
content rules), `trust_center` schema section, SKILL.md routing and toolkit
workflow rows, CI FRMR snapshot integrity check, and the
`fedramp-20x-ksi-due-diligence` eval scenario.

## Phase 5: Evidence Automation — DELIVERED

Shipped: `references/data/evidence-collector-manifest.json` (14 collectors
across Microsoft Graph/GCC High, AWS GovCloud, GCP SCC, CrowdStrike, Zscaler,
Prisma Access, Duo, Splunk), `scripts/collect_evidence.py` (orchestrator with
`--dry-run` pipeline), `scripts/merge_findings.py` (GRC Engineering Club
Finding bridge via 800-53 crosswalk), `scripts/evidence_lib.py`,
`references/grc/evidence-automation.md`, `references/modern-it/security-operations/`
(hub, Microsoft Graph, cloud-native inspectors), dashboard Evidence freshness
view and SPRS submission diff, extended program data schema (collector metadata,
`sprs_submission`), eval scenario `toolkit-evidence-collectors.yaml`.

Also shipped in this pass: platform-specific evidence buckets
(`evidence/<bucket>/<family>/<req>/`), all 14 collector modules under
`scripts/collectors/` with Vanta-style env profiles (`env_config.py`,
`--env-check`), and `scripts/export_sprs.py` (JSON + optional CSV scoresheet
for SPRS portal entry).

Remaining: wire live HTTP clients per collector (or rely on external GRC
inspector plugins), finer AO-letter mapping in merge_findings, reconciliation
with cmmc-dfd plugins when reachable.

Early delivery (pre-Phase 5): CMVP validation (`scripts/check_cmvp.py`) and
diagram capability (`scripts/generate_diagrams.py`).

## Phase 6: Assessment Operations

- Mock-assessment mode: generate interview scripts and evidence
  requests per family from the examine/interview/test data, then score
  answers at the objective level.
- POA&M lifecycle automation: closeout evidence packets assembled from
  the program data file.
- Reconciliation with the author's wider portfolio (cmmc-l2-master,
  policy-mapper, jumpstart-generator, remediation-tracker skills;
  myctrl.tools and grclanker interop) as those sources become reachable
  from the working environment.

## Not Planned

Anything requiring nonpublic sources, paid feeds, or assessment
authority this skill does not have. The enabler posture and the
public-source provenance rule in `CLAUDE.md` bound every phase.
