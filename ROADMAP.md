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

## Phase 3: Multi-Framework Crosswalks and OSCAL

CMMC to NIST SP 800-53 Rev 5 to FedRAMP Rev 5 crosswalk as data, not
prose, extending the existing `references/fedramp-gap.md` narrative.

- New: `references/data/800-53-crosswalk.json` (from NIST's published
  800-171 to 800-53 mapping), ISO/IEC 27001 mapping notes, and OSCAL
  awareness: emit the program data file as an OSCAL SSP (component
  definitions for inheritance sources; compliance-trestle as the
  reference tooling).
- Purpose: one program data file able to answer CMMC, FedRAMP, and
  27001 questions about the same environment.

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
- Also: CMVP certificate validation checks for every FIPS claim
  (SC.L2-3.13.11) against the NIST CMVP registry, and a
  dashboard-to-SPRS diff that flags when the computed score diverges
  from the last submitted score.

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
