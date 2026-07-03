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

## Phase 4: FedRAMP 20x and Trust Center Interop

Track FedRAMP's machine-readable direction (FRMR artifacts, Key
Security Indicators) alongside the Rev 5 baselines.

- New: FRMR snapshot support next to
  `scripts/build_fedramp_snapshot.py`; guidance for reading KSI-based
  packages during vendor due diligence; a portable public trust-center
  page generated from the program data file (the outward-facing twin of
  the internal dashboard).

## Phase 5: Evidence Automation

Close the gap between "evidence links" and live proof.

- New: guidance for collecting evidence from Microsoft Graph API and
  cloud-native inspectors (Entra ID, Intune, Defender, Sentinel) mapped
  to assessment objectives; collectors write into the program data
  file's evidence arrays with timestamps; a dashboard freshness view
  (evidence older than its refresh bucket per
  `references/grc/continuous-monitoring.md`).
- DELIVERED early: CMVP certificate validation for every FIPS claim
  (scripts/check_cmvp.py verify/find against the NIST-CMVP-API mirror,
  official registry cited per result) and the diagram capability
  (topology data model, generate_diagrams.py network + CUI flow DFD
  outputs, dashboard Diagrams view, references/diagram-guide.md).
  Remaining here: a dashboard-to-SPRS diff that flags when the computed
  score diverges from the last submitted score, and reconciliation with
  the author's cmmc-dfd plugins and the cmmc.kylecain.dev Diagram Hub
  once reachable.

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
