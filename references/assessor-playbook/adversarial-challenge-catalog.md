# Adversarial Challenge Catalog

> Source: 32 CFR 170.19 and 170.4; CMMC Assessment Process (CAP) v2.0 (The Cyber AB); DoD CMMC FAQ (entries cited inline); DoD CMMC Scoping Guide Level 2 v2.13; NDISAC VDI white paper and practitioner sources per SOURCES.md

The red-team rail's ammunition: challenges in assessor voice against
everything a program data file asserts. Each challenge is a thread a real
assessor pulls; the catalog exists so the OSC hears it first from their own
advisor with time to fix it, not from a Lead CCA during the scope-validation
gate.

## How to press a challenge

- Speak as the assessor: assert the doubt, cite the rule, name the evidence
  that would close the thread. One thread at a time.
- Stop when the OSC produces the surviving artifact. The goal is a closed
  question or a logged gap, not a lecture.
- Rank output by how likely an assessor is to pull the thread: scope
  boundary claims first (they gate everything), then Security Protection
  Asset misses (the most commonly overlooked category), then per-family
  depth.
- Every challenge the program data cannot answer becomes an
  `open_questions` entry. Assumption confirmations and retirements are
  written with consent. Conformity fields are never written by this rail.
- The challenges attack content: assets, flows, boundaries, enforcement
  points. Diagram count is not a finding; one combined diagram covering
  network topology and CUI flow satisfies the SSP.

## Group 1: Asset categorization

**"This CRMA claim rests on paper."** Contractor Risk Managed Assets are
assets that can, but are not intended to, process CUI, managed by the
contractor's risk-based policies (32 CFR 170.19(c)). When the documented
practices are thin, the assessor recategorizes the asset as a CUI asset and
assesses it fully. Survives: the risk-based policy actually naming the
asset class, the documented practices, and a spot check showing they are in
place.

**"You forgot your Security Protection Assets."** SPA misses are the most
common overlooked category: SIEM, EDR console, password manager, RMM,
patch and identity infrastructure, backup of security systems, the
firewall's own management plane. Anything providing security functions to
the CUI environment is in scope as an SPA (170.19(c)) and contributes
evidence to the requirements it supports. Survives: an inventory pass that
lists them and per-asset answers for the requirements they back.

**"Out of scope by policy is not out of scope."** A memo telling people not
to put CUI somewhere is not separation. The scoping guide's out-of-scope
test is inability, enforced technically or physically. Survives: the named
enforcement point (firewall rule set, tenant restriction, physical gap) and
a test showing the path fails.

**"Could this asset reach CUI if it tried?"** On a flat network every host
has a theoretical path to the CUI store, which makes everything one scope.
A path counts until a technical enforcement point removes it. Survives:
segmentation evidence at the enforcement point, not the VLAN diagram alone;
a switch provides VLANs, but a VLAN is not a boundary without a stateful
enforcement point controlling what crosses.

**"Your password manager is a CUI-adjacent vault."** It stores credentials
to every CUI system: Security Protection Data, making its platform an SPA
(and, hosted, a cloud-tenancy question from the platforms phase). Survives:
the vault in the inventory with its access, MFA, and audit story.

**"The ticketing system is a CUI store."** If technicians paste screenshots
into tickets, CUI is in the ticketing platform. Survives: either DLP and
practice evidence that CUI never lands there, or the platform categorized
and assessed as a CUI asset.

## Group 2: Data flow and diagram completeness

**"What happens at this line?"** Every flow crossing the scope boundary
needs an answer: protocol, enforcement, evidence. An ingress or egress the
OSC cannot explain is an unassessed path. Survives: per-flow answers
matching `topology.flows` and the firewall or gateway configuration.

**"Where are the flows you did not draw?"** Backup streams, admin and RMM
sessions, monitoring agents, print spools, scan-to-email, hygiene layers
(mail filtering), VoIP and video, API integrations. A diagram showing only
the business flows is incomplete, and the CAP scope-validation step
compares it against reality. Survives: the quiet flows drawn, or an
explicit decision entry for each exclusion.

**"Narrate the CUI flow without the SSP open."** The assessor asks a role
owner to walk CUI end to end and compares the narration against the SSP
and diagram. Divergence is the strongest finding signal there is, and it is
also how AI-boilerplate SSPs get spotted. Survives: narration, SSP
narrative, and diagram that agree.

**"Your mail transits a commercial filter."** A hygiene service processing
CUI-bearing mail in transit is a CSP in the flow and carries the FedRAMP
Moderate question (DFARS 252.204-7012(b)(2)(ii)(D)). Hybrid connectors and
leftover smart hosts are the quiet bypasses. Survives: message-trace
evidence of the actual path and the service's authorization, or the path's
removal.

**"This CDN or proxy decrypts CUI."** Anything terminating TLS on a
CUI-bearing connection has the plaintext: CUI asset. Encrypted
pass-through, by contrast, does not extend scope (DoD CMMC FAQ, scoping
entries). Survives: knowing which devices terminate vs pass through, with
configuration evidence.

## Group 3: Enclave integrity

Sixteen probes for the seams of a carve-out. Each survives only with a
technical enforcement answer plus a test.

1. Clipboard: can a user copy from the enclave session and paste outside?
2. Drive mapping: do local drives mount inside the remote session?
3. Screen share: can a user share the enclave screen into a commercial
   meeting?
4. Browser upload: can a browser in the enclave reach personal cloud
   storage?
5. Print: can an enclave session print to an uncontrolled home printer?
6. Email out: can enclave mail forward or auto-forward externally?
7. Personal-account mix-up: does the OneDrive client allow adding a
   personal account on an enclave device?
8. Dual-home users: same person, two environments; what stops hand-carry
   between their own machines?
9. Identity federation bleed: the assessor follows the identity chain out;
   if enclave identities federate from a commercial directory, the
   commercial identity plane joins the assessment. Survives: a separate
   identity domain or an enforcement story for the federation path.
10. Personal phones: can a phone's mail client or browser open enclave
    mail?
11. Friction route-arounds: where the enclave is slow, what did users adopt
    instead? Expense reports and DNS logs answer this honestly.
12. SPA entourage: the enclave's patching, monitoring, identity, and
    backup services; each is an SPA the carve-out story must include.
13. Undocumented ingress/egress: group 2's line-by-line question applied to
    the enclave boundary specifically.
14. Shared admin identities: one admin account spanning enclave and
    corporate collapses the separation at the privileged layer.
15. SSP-reality divergence: the enclave the SSP describes vs the one users
    describe (see group 2's narration probe).
16. The theoretical path: from a corporate host, what actually blocks a
    connection to an enclave address? "Nothing routes there" needs the
    routing and filtering evidence.

## Group 4: The ESP story

**"Your MSP is in this assessment."** A non-CSP External Service Provider
(ESP) with access to CUI or Security Protection Data is assessed as part
of the OSC's assessment; SPD
alone pulls a provider in with zero CUI (DoD CMMC FAQ external-provider
entries, E-series; 32 CFR 170.19). Survives: the provider classified,
their access paths documented, and their people prepared to interview.

**"Show me the CRM row for this requirement."** Every requirement an ESP
wholly or partially performs must appear in the customer responsibility
matrix. A shared requirement with no CRM row scores NOT MET; inheritance
is never assumed. Survives: the mapped CRM with per-requirement rows the
provider actually signed.

**"Who at the provider will sit for the interview?"** ESP personnel must
demonstrate credible ownership of the requirements they perform. "Our
account manager will answer" fails the role-owner rule
(`interview-method.md`). Survives: named engineers on the calendar.

**"A technician's desk can reach your CUI laptops."** RMM desk-reach makes
the technician workstation environment part of the access story.
Multi-tenant RMM platforms have a KEV compromise history (ScreenConnect),
so tenant isolation is a fair question. Survives: jump box or one-way
gateway architecture, session recording, and the provider's tenant
isolation answer.

**"That remote tool is not FIPS validated."** Consumer remote-access tools
(TeamViewer, Splashtop tiers) generally lack CMVP-validated modules; a CUI
session over them fails SC.L2-3.13.11's validated-crypto expectation.
Survives: a CMVP certificate for the actual module in use
(`scripts/check_cmvp.py verify`) or a validated transport wrapping the
session.

**"Your VPN to the MSP pulls their equipment in."** A site-to-site tunnel
to provider infrastructure extends the access path to that infrastructure.
Survives: the far end documented, filtered to named hosts and ports, and
covered in the CRM.

**"CSP or ESP: who holds the subscription?"** The fork decides the rule
set: provider-held subscription with CUI transiting means FedRAMP
questions; OSC-held subscription with provider administration means ESP
staff-access questions (DoD CMMC FAQ E-series). Survives: a
subscription-ownership answer per service, written in the responsibility
matrix.

**"SOC 2 is not the standard here."** SOC 2 attests the provider's own
controls against their own scope; it satisfies neither DFARS 252.204-7012
flowdown nor FedRAMP Moderate equivalency. Survives: the actual applicable
mechanism per service (FedRAMP authorization, equivalency body of
evidence, or assessed-with-OSC treatment).

## Group 5: Out-of-scope and inheritance claims

**"Prove the thin client is a dumb terminal."** VDI endpoints stay out of
scope only when the session is KVM only: clipboard redirection off, drive
mapping blocked, print controlled, no local cache (scoping guide VDI note;
NDISAC VDI white paper). Assessors spot-check these live. Survives: the
four redirection tests with dated evidence
(`modern-it/asset-baselines/vdi-thin-client.md` checklist), plus gateway
device authentication for what may connect at all.

**"Inheritance without a mapped CRM is NOT MET."** Marking an objective
inherited because "it's in Azure" fails without the provider CRM row that
says so and the customer-side share implemented. Survives:
`inheritance` entries citing `crm_ref` rows from the provider document
(see `grc/inherited-controls-mapping.md`).

**"Equivalency means a complete body of evidence."** FedRAMP Moderate
equivalency requires a BoE that is complete and current under the DoD CIO
memo; the C3PAO checks the BoE's presence and currency rather than
re-assessing the CSP. Survives: the BoE on file, its date inside the
provider's assessment periodicity, and the CRM mapped.

**"The FedRAMP Marketplace disagrees with you."** Authorization claims get
checked against the Marketplace listing. Survives: the package id in
`inheritance_sources` matching the live listing
(`references/data/fedramp-snapshot.json` workflow).

**"Your one-way transfer has a return path."** Data diodes and one-way
gateways justify exclusions only when nothing flows back. Survives: the
return-path test and the device's configuration.

## Group 6: Physical and OT

**"Where does PE.L2-3.10.2 end for you?"** Protecting and monitoring the
facility includes support infrastructure: power distribution, UPS,
generators, HVAC, cabling runs, fire panels with network cards. Survives:
the support-infrastructure sweep in the inventory with access answers.

**"The landlord's master key opens your CUI room."** Building-level access
undermines room-level claims (PE.L1-3.10.1). Survives: rekeyed or
badge-controlled CUI spaces, or documented landlord-access procedures with
logs.

**"Your camera watches the CUI screen."** A camera aimed at CUI displays
feeds CUI to its NVR: self-inflicted scope. And covered equipment
(Hikvision, Dahua, OEM variants) violates Section 889 regardless of scope.
Survives: placement review, NVR categorization, and make/model against the
889 list.

**"Badge logs are your 3.10.4 evidence; where are they?"** The PACS is the
audit-log source for physical access; if it is unmanaged, offline, or the
vendor's cloud, that is the finding thread. Survives: retention, review
cadence, and the PACS platform categorized (usually SPA).

**"G-code is CUI, and it is sitting on the shop floor."** Programs derived
from controlled drawings carry the control. Legacy controllers that cannot
meet requirements are Specialized Assets with compensating controls,
documented in the SSP; never "N/A". Survives: the DNC or file-drop server
as system of record with hashing or read-only enforcement, isolation
evidence, and the vendor-access story (vendor bastion, named accounts).

**"iLO reaches everything; who reaches iLO?"** Out-of-band management
(iLO, iDRAC, IPMI) is a privileged path to in-scope hardware: SPA
treatment, its own network, its own access list. Survives: the management
network drawn on the topology, filtered, and inventoried.

## Output format

The rail's report lists challenges in ranked order, each as:

```
CHALLENGE (assessor voice, one sentence)
CITES: rule / guide / FAQ entry
STATUS: survived | open thread | finding-in-waiting
SURVIVES WITH: the artifact or architecture that closes it
WRITTEN TO: open_questions / assumptions id
```

Rank by thread-pull likelihood: scope-boundary claims, then SPA misses,
then ESP coverage, then per-family depth. The report ends with the three
threads to close before anyone schedules a C3PAO.
