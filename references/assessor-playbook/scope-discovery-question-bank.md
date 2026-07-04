# Scope Discovery Question Bank

> Source: 32 CFR 170.19 and 170.4; CMMC Assessment Process (CAP) v2.0 (The Cyber AB); DoD CMMC Scoping Guide Level 2 v2.13; DoD CMMC FAQ (entries cited inline); practitioner sources per SOURCES.md

The grill rail's ammunition: twelve interrogation phases that walk every nook
of an OSC environment the way a Lead CCA validates scope in CAP Phase 1.
Scope validation is a hard gate in a real assessment; disagreements about
asset categorization must be resolved before conformity assessment begins,
so every question here is cheaper to answer now than during Phase 1.

## How to run an interrogation

- One phase per sitting is a good default. Depth beats coverage; a phase is
  done when its exit criteria are met, not when its questions run out.
- Every answer becomes a `qa_log` entry with a date and the answering role.
  Answers asserted without evidence get `confidence: reported`; anything
  inferred goes to the `assumptions` register with the risk if wrong.
- Unanswered questions go to `open_questions` with an owner. An assessor
  treats an unanswered scoping question as a thread to pull; so does the
  red-team rail.
- When an answer changes the asset inventory or topology, propose the exact
  edit to the program data file and write it on confirmation.
- Per-asset hardening depth lives in `references/modern-it/asset-baselines/`;
  this bank finds the assets, the baselines interrogate their configuration.

## Phase 1: contracts-cui

**Entry criteria:** none; always start here. **Exit criteria:** every active
contract's CUI obligations are known; CUI types and markings are named; any
export-control trigger is identified; the answer to "where does CUI enter?"
is written.

Core questions:

1. Which contracts carry DFARS 252.204-7012, 7019, 7020, or 7021, and which
   carry only FAR 52.204-21? The clause set decides the level conversation.
2. What CUI categories flow under each contract (CTI, export controlled,
   naval nuclear, other)? Who marks it, and have you seen actual markings?
3. Is any of it ITAR or EAR technical data? Export control triggers
   US-persons handling requirements from those regimes; that is an ITAR/EAR
   consequence, not a blanket CMMC rule, and it drives cloud tenancy choices
   (see `modern-it/cloud-platforms/`).
4. How does CUI arrive: contracting officer email, DoD SAFE, a prime's
   portal, physical mail, hand carry at a customer site?
5. Do you generate CUI (drawings, test results, G-code derived from
   controlled drawings) or only receive it?
6. Which CAGE codes and which legal entities perform on these contracts?
   Every CAGE code and physical location in scope gets sampled in a real
   assessment (CAP sampling rules).

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "We only handle FCI" | Hidden-CUI check: ask for three recent deliverables and the DD Form 254 or contract attachments; run the `level-1-quickstart.md` decision test |
| "The prime sends us drawings by email" | Which mailbox, which tenant, who else is on the distribution, does it forward anywhere |
| "ITAR applies" | Foreign-national access anywhere in IT support, including the MSP's offshore helpdesk; tenancy (GCC High or equivalent US-persons backing) |
| "We make parts from their drawings" | The G-code and CAM files derived from controlled drawings are CUI; jump to Phase 8 (specialized-ot) |

Writes: `organization.scope_narrative`, `discovery.qa_log`, contract-driven
entries in `assets.cui`.

## Phase 2: people

**Entry criteria:** Phase 1 CUI types known. **Exit criteria:** every role
that touches CUI or administers in-scope systems is named; remote and
foreign-national exposure is written; no "spokesperson" gaps (the org chart
names a real owner for every function an assessor will interview).

Core questions:

1. Who touches CUI day to day, by role? Who administers the systems that
   protect it? Assessors interview role owners, not spokespeople.
2. Who works remotely, from where, and on what equipment? Home offices that
   process CUI are in-scope locations.
3. Any foreign nationals in the company, in IT support, or at any ESP in the
   support chain? (Consequential under ITAR/EAR per Phase 1; also shapes
   AC and PS answers.)
4. Are any users dual-homed across the CUI environment and a commercial
   environment (two accounts, two machines, one person)? Dual-home users are
   a classic enclave bleed path.
5. Who holds privileged access, and are any admin identities shared?
6. Subcontractors: who receives CUI downstream, and what flows down to them?

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "IT is outsourced" | Jump the whole MSP question set from Phase 9 into this sitting's open questions |
| "A few people work from home" | For each: equipment owner, print capability at home, household member access, VPN vs VDI path |
| "Everyone has one account" | Whether that identity also signs into out-of-scope systems; identity is the bleed path assessors follow first |

Writes: `organization.roles`, `discovery.qa_log`, `open_questions` for
unnamed owners.

## Phase 3: locations

**Entry criteria:** people and contracts mapped. **Exit criteria:** every
site where CUI is stored, processed, transmitted, or discussed is listed
with its physical-control story; colo and landlord arrangements are written.

Core questions:

1. List every location: HQ, plants, sales offices, home offices, colos,
   customer sites, vehicles used for transport. All CAGE codes and physical
   locations get sampled (CAP).
2. For each colo: where does their perimeter end and yours begin? Cage or
   rack lock ownership, escort rules, right to audit in the contract.
3. Who else can enter CUI spaces: landlord master keys, cleaning crews,
   building engineers, shared-floor tenants?
4. Where is CUI discussed out loud? Conference rooms with always-on video
   or transcription devices are an overlooked scope entry.
5. Do employees travel with CUI on devices? Which countries?

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "We rent our data center space" | The colo's physical controls back your PE answers only as far as the contract and evidence go; ask for the SOC 2 or equivalent and check what it covers vs your cage |
| "The landlord has master keys" | How PE.L1-3.10.1 limits access to the CUI space specifically, not the building |
| "Home offices, yes" | Per-site: locked storage, shredding, who else lives there; see `modern-it/asset-baselines/physical-access.md` |

Writes: location fields on assets, `discovery.qa_log`, PE-related
`open_questions`.

## Phase 4: platforms-tenants

**Entry criteria:** CUI types and entry points known. **Exit criteria:**
every cloud tenant and SaaS product in the CUI path is named with its
FedRAMP story; every seam between commercial and government environments
has a technical enforcement answer, not a policy answer.

Core questions:

1. Which exact services hold CUI: tenant type (commercial M365, GCC, GCC
   High, AWS GovCloud, GCP Assured Workloads), not just vendor names. A CSP
   storing, processing, or transmitting CUI must meet FedRAMP Moderate or
   equivalency (DFARS 252.204-7012(b)(2)(ii)(D)).
2. If the org runs split tenancy (commercial plus government), what
   technically stops CUI from landing in the commercial side? Assessors
   probe the daily-use seam: Teams meetings, OneDrive sync clients, shared
   calendars. "We told people not to" is a policy answer.
3. Where does identity live? A hybrid AD Connect chain that syncs into a
   commercial tenant while CUI lives in GCC High hands the assessor an
   identity path out of the enclave.
4. Device management: which MDM instance manages CUI endpoints? GCC High
   Intune is a separate instance; commercial-managed devices reaching into a
   government tenant is a finding-in-waiting.
5. Email hygiene layers: does mail transit a commercial filtering service
   (Mimecast, Proofpoint) before reaching the government tenant? A service
   that processes CUI in transit is a CSP in the flow. Check hybrid
   connectors and legacy smart hosts left over from migrations.
6. Anything that terminates TLS on CUI traffic (CDN, WAF, SSL-inspecting
   proxy, VPN concentrator) decrypts CUI and is a CUI asset. Encrypted
   pass-through does not extend scope (DoD CMMC FAQ; see also the
   encryption-is-not-separation point below).
7. Shadow SaaS sweep: expense reports, SSO app catalog, browser extensions,
   DNS logs. What tools did engineering adopt without a review, including
   AI assistants and file-conversion sites?
8. Post-migration residue: are commercial accounts, licenses, sync clients,
   or mail routes from the pre-migration environment still active?

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "Commercial M365" with CUI confirmed | FedRAMP Moderate baseline question for each service in the path; commercial EXO/SPO/Teams do not carry it |
| "We have both tenants" | Name the technical enforcement at every seam: conditional access, tenant restrictions, DLP, sync-client blocks |
| "Encryption separates it" | Encryption protects confidentiality in transit; it is not logical separation for scoping (DoD CMMC FAQ) |
| "Our SSO covers everything" | Everything the CUI identity can reach is a candidate asset; walk the app list |

Writes: `assets.cui` / `assets.security_protection`,
`inheritance_sources`, tenancy notes, `open_questions` per unverified seam.

## Phase 5: endpoints

**Entry criteria:** platforms mapped. **Exit criteria:** every device class
that can render CUI is inventoried with its management story; BYOD and
mobile answers are technical, not policy; any VDI carve-out claim has its
test evidence identified.

Core questions:

1. Enumerate device classes: corporate laptops/desktops, mobile, tablets,
   lab machines, loaners, executives' second devices. Which are in the CUI
   path and how are they managed?
2. Can personal phones read CUI-bearing mail or Teams? Native mail profiles
   and browser access count. If yes, they are CUI assets today regardless
   of what the SSP says.
3. BYOD: is it blocked technically (conditional access, app protection) or
   by policy memo?
4. VDI/thin-client carve-outs: the endpoint stays out of scope only when
   the session is KVM only. Assessors test clipboard redirection, drive
   mapping, print redirection, and local cache on the spot. What evidence
   shows those are blocked? (See `modern-it/asset-baselines/vdi-thin-client.md`.)
5. USB story: "prove a USB stick cannot mount" is a live test an assessor
   can run at any sampled endpoint. What enforces it?
6. Forgotten hosts: compare the asset inventory against DHCP leases, switch
   MAC tables, backup job lists, and EDR consoles. Machines those systems
   know about and the inventory does not are the classic finding.

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "Phones just get email" | Which mail client, which protection policy, can attachments be saved or forwarded to personal apps |
| "Thin clients are out of scope" | The four redirection tests plus gateway device authentication; who validated them and when |
| "We image everything the same way" | Baseline drift: how images stay aligned with the documented configuration (CM.L2-3.4.1/3.4.2) |

Writes: `assets` by category with `baseline_profile` pointers,
`discovery.qa_log`, VDI `decisions` entries.

## Phase 6: dev-ai

**Entry criteria:** platforms and endpoints mapped. **Exit criteria:**
the developer and DevOps population is inventoried with its CUI
exposure; the toolchain (repos, CI/CD, registries, secrets) is
categorized; every AI tool in use is either sanctioned or blocked by a
named enforcement point, not a policy memo.

Core questions:

1. Who writes software here: developers, DevOps, data scientists,
   contractors? What CUI do they touch: source code derived from
   controlled specifications, test data seeded from CUI, IaC holding
   environment secrets?
2. Developer workstations: same baseline as the fleet, or a privileged
   exception ("developers have local admin")? Exceptions are bypass
   paths for every enforcement layer below; see
   `modern-it/asset-baselines/development-sdlc.md` for the workstation
   baseline row.
3. The toolchain: which repo platform and whose tenancy, which CI/CD
   system, artifact registries, package proxies, secrets managers?
   Shared CI runners carry the SC.L2-3.13.4 shared-resource question
   (CUI build artifacts leaking to non-CUI jobs); build systems that
   deploy to CUI environments are Security Protection Asset
   candidates.
4. AI inventory, sanctioned side first: which AI services are approved
   for CUI-adjacent work, and on what basis
   (`modern-it/ai-services/fedramp-ai-services.md`,
   `ai-dev-tools.md`)? Self-hosted models are in scope with a
   contractor-authored boundary (`self-hosted-ai.md`); "it's local so
   it doesn't count" is wrong in both directions.
5. AI inventory, shadow side: what do expense reports, the SSO app
   catalog, browser extensions, and DNS logs show people actually
   using? This extends the Phase 4 shadow-SaaS sweep to the tools
   engineering adopts fastest.
6. The enforcement question: walk me from a CUI laptop to chatgpt.com.
   What stops the request, by name? Layers per
   `modern-it/ai-services/README.md` (Blocking unsanctioned AI and
   SaaS): DNS filtering or secure web gateway, CASB and DLP,
   conditional access and tenant restrictions, device-based rules
   (MDM app control, managed browser), application-layer egress
   rules.
7. If there is no traditional firewall: name the cloud-native stack
   that is the boundary (AWS security groups, Network Firewall, SCPs;
   Azure NSGs, Azure Firewall, Conditional Access; GCP VPC Service
   Controls, Context-Aware Access) or the SASE/SWG that fills the
   role, per `modern-it/asset-baselines/network-firewall-wlan.md`
   (No NGFW section).

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "Policy prohibits unsanctioned AI" | The policy-is-not-separation rule: name the technical layer, show the rule export, run the live test that fails |
| "We're cloud-only, no firewall" | The named native enforcement stack per platform, and what covers off-network laptops (SWG agent, device rules) |
| "We use Zscaler / a SASE" | Is the SWG documented as the boundary enforcement point; does it terminate TLS on CUI (then it is a CUI asset); is the tunnel module FIPS-validated (SC.L2-3.13.11, `scripts/check_cmvp.py`) |
| "Developers need local admin" | What that exempts them from (agent removal, proxy bypass, extension installs) and the compensating monitoring |
| "Copilot/Cursor is approved" | Whose approval, which tier and routing, and the prompt-context exposure analysis per `ai-dev-tools.md` |

Writes: `assets` (dev and build systems, AI platforms by category),
`topology.flows` (egress paths), `decisions` (the sanctioned-AI list),
`open_questions` per unverified enforcement layer.

## Phase 7: physical-media

**Entry criteria:** locations known. **Exit criteria:** paper, print, scan,
mail, removable media, and camera/badge systems all have owners and
dispositions; the MFP fleet's network position and scan paths are written.

Core questions:

1. Where does CUI exist on paper: printed drawings on the shop floor,
   travelers, QA records, shipping paperwork? Who reconciles and destroys?
2. Printers and MFPs: which devices can print or scan CUI, what network
   segment are they on, and where does scan-to-email relay? A printer that
   touches CUI is in scope along with its segment (see
   `modern-it/asset-baselines/printers-mfp.md`).
3. Mail and shipping: how does physical CUI enter and leave? MP.L2-3.8.5
   wants control and accountability during transport.
4. Removable media: USB, external drives, camera cards on the shop floor.
   Sanitization before disposal or reuse (MP.L2-3.8.3), marking, and the
   live can-it-mount test from Phase 5.
5. Cameras and badge systems: camera placement (a camera aimed at CUI
   screens puts its NVR in the CUI conversation), storage location, vendor.
   Section 889 bans covered equipment (Hikvision, Dahua and their OEMs);
   badge/PACS logs are the PE.L1-3.10.4 audit-log source.
6. Fax, if it exists, and analog lines generally.

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "Scan-to-email is on" | The exact relay target and whether it transits a commercial mail system; this is the classic quiet bypass |
| "We shred eventually" | Accumulation points, locked consoles, destruction records |
| "Cameras are the landlord's" | Feed access, retention, make/model against the 889 list |

Writes: `assets` (MFPs, NVRs, PACS), media-handling `qa_log` entries,
`open_questions` for unverified scan/mail paths.

## Phase 8: specialized-ot

**Entry criteria:** locations and endpoints mapped. **Exit criteria:** every
OT, IoT, GFE, and test-equipment asset is categorized; legacy-system
compensating controls are documented rather than waved at; management
interfaces are accounted for.

Core questions:

1. CNC, test benches, PLCs, HMIs, DNC servers: which run on unsupported
   operating systems, and which touch CUI-derived data? G-code and CAM
   files derived from controlled drawings are CUI.
2. Specialized Assets are documented in the SSP and asset inventory and
   handled per the scoping guide; they are never "N/A". What compensating
   controls surround the ones that cannot meet requirements directly
   (isolation, one-way transfer, read-only system of record)?
3. Where do programs live between the engineering network and the machines?
   The DNC or file-drop server is a CUI asset; hashing or read-only
   enforcement is the integrity story.
4. Vendor access to OT: who dials in, through what (vendor bastion, shared
   TeamViewer?), and under whose account?
5. Government-furnished equipment: inventoried, marked, and covered by
   which requirements per the contract?
6. Out-of-band management: iLO, iDRAC, IPMI, serial consoles. These are
   privileged management paths; where do they terminate and who reaches
   them? (Security Protection Asset treatment; see
   `modern-it/asset-baselines/specialized-ot.md`.)

Writes: `assets.specialized`, compensating-control notes, `decisions` on
categorization calls.

## Phase 9: esps-access-paths

**Entry criteria:** platforms and people mapped. **Exit criteria:** every
external provider is classified (CSP vs non-CSP ESP), every tool touching
the boundary is listed, personnel and fourth parties are named, and the
CRM answer for every shared requirement exists or is an open question.

Core questions:

1. List every provider: MSP, MSSP, SOC, backup operator, helpdesk,
   consultants with admin rights. An ESP handling Security Protection Data
   is in the assessment even with zero CUI (DoD CMMC FAQ, external-provider
   entries; 32 CFR 170.19 ESP treatment).
2. CSP or ESP fork: who holds the subscription for each service? If the
   provider holds it and CUI transits, the FedRAMP question applies; if you
   hold it and they administer, it is ESP staff access to your environment.
3. Enumerate every tool that touches the boundary: RMM, EDR, SIEM, backup
   agent, remote access, ticketing, documentation platform (IT Glue and
   peers hold your credentials and diagrams: Security Protection Data).
4. RMM desk-reach: can a technician's desk open a session to a CUI asset?
   Then the path from that desk is in the access story; jump boxes and
   one-way gateways are the usual mitigations. Multi-tenant RMM compromise
   is an active threat pattern (ScreenConnect KEV history), so ask what
   isolates your tenant.
5. Remote access tools: TeamViewer, Splashtop and consumer-grade tools
   generally do not run FIPS-validated cryptography; what protects CUI
   sessions (SC.L2-3.13.11)?
6. Does a VPN connect your network to MSP equipment? The equipment at the
   far end enters the conversation.
7. Named personnel: which provider staff have access, and will they show up
   to be interviewed? ESP personnel must demonstrate credible ownership of
   the requirements they perform in a real assessment; the CRM must cover
   every wholly or partially performed requirement.
8. Fourth parties: who does your MSP outsource to (after-hours NOC,
   offshore helpdesk)?
9. Artifact retention: assessment artifacts are retained hashed for six
   years; who holds them and where?

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "Our MSP handles everything" | The responsibility matrix requirement by requirement; "everything" means the CRM is either comprehensive or fictional |
| "They use their own tools" | Each tool's tenancy, FedRAMP status if it holds CUI or SPD in their cloud, and the desk-reach question |
| "They're SOC 2 certified" | SOC 2 does not satisfy 7012 or FedRAMP Moderate equivalency; map what actually covers the gap |

Writes: `responsibility_matrix`, ESP entries in
`assets.security_protection`, `inheritance_sources`, `open_questions` per
uncovered requirement.

When a provider runs the SIEM or SOC function, do not settle for the
generic tool answer here: drill the platform, tenancy, analyst access,
and retention in Phase 10 (audit-siem).

## Phase 10: audit-siem

**Entry criteria:** platforms (Phase 4) and ESPs (Phase 9) mapped.
**Exit criteria:** the log platform and its tenancy are known; the
log-source inventory is reconciled against the asset inventory or the
gap is logged; access, prevented access, and retention have answers.

Core questions:

1. What platform collects and correlates the logs (SIEM, log
   management, cloud-native), and whose tenant is it: yours, or a
   multi-tenant instance the MSSP operates? Where does it run? Log and
   alert data about the CUI environment is Security Protection Data;
   an MSSP platform holding it in their cloud raises the CSP
   conversation from Phase 9, and the platform is a Security
   Protection Asset either way.
2. Show the log-source inventory: which systems forward logs, and
   which event types per source (AU.L2-3.3.1)? "We have a SIEM" is
   not an answer; the documented list of what is collected is.
3. Reconcile that inventory against the asset inventory from the other
   phases: do the badge/PACS system (Phase 7), the OT segment
   (Phase 8), the MFPs, the break-glass accounts, and the backup
   platform actually forward logs? Every in-scope asset absent from
   the log-source list is a finding candidate.
4. Show the correlation and alerting rules (AU.L2-3.3.5) and the
   audit-failure alerting path (AU.L2-3.3.4). Who wrote the rules, who
   tunes them, and when did a rule last fire usefully?
5. Who reviews, and on what cadence (AU.L2-3.3.3): named reviewers,
   review artifacts from a specific recent week, not the policy's
   intention. This is the practice-based question a policy cannot
   answer.
6. Who can read audit information, and who can administer the logging
   tools? AU.L2-3.3.8 and 3.3.9 expect management limited to a subset
   of privileged users; general IT administrators who can edit or
   delete the audit trail defeat it. Name who is prevented, and how.
7. If an MSSP runs it: which named analysts have access, from where,
   under whose identities, with what isolation from other customers'
   tenants? If ITAR applies (Phase 1), the US-persons question follows
   their staffing.
8. Retention: what period is configured and documented (AU.L2-3.3.1
   expects a defined retention; DFARS 7012 sets no general duration,
   with 1 year a common standard per
   `references/domains/au-audit.md`), and can it serve the incident
   duties: 72-hour reporting under 7012(c) presumes logs to
   investigate with, and 7012(e) requires 90-day preservation of
   images and monitoring data from the report date.

Follow-up logic:

| If the answer is | Dig here |
|---|---|
| "The MSSP handles all of that" | The CRM rows for the AU requirements they perform, their named analysts for interview, and the tenancy/SPD-location questions above |
| "Everything goes to the SIEM" | The log-source export vs the asset inventory; the gap list is the real answer |
| "Admins can see the logs" | Which admins can modify or delete them; 3.3.8/3.3.9 want the audit trail protected from the people it watches |
| "Retention is whatever the default is" | The configured value, the documented decision, and the 7012(e) 90-day scenario walked end to end |

Writes: `assets.security_protection` (SIEM/log platform with tenancy
notes), `responsibility_matrix` (AU rows when MSSP-performed),
`discovery.qa_log`, `open_questions` per missing log source.

## Phase 11: data-flows

**Entry criteria:** most asset phases touched; this phase stitches them.
**Exit criteria:** every CUI ingress and egress on the diagram has a
"what happens at this line" answer; the flows the SSP narrative describes
match the diagram and the discovery record.

Core questions:

1. Walk CUI end to end for one real contract: arrival, storage, processing,
   output, delivery, destruction. Narrate it without the SSP open, then
   compare. Divergence between narration and SSP is the strongest finding
   signal an assessor gets.
2. For every line crossing the scope boundary on the diagram: what is it,
   what enforces it, where is the evidence? Undocumented ingress/egress is
   the DFD question assessors ask first.
3. The quiet flows: scan-to-email (Phase 7), backup streams (Phase 12),
   admin sessions, monitoring agents, print spools, VoIP and video (a DoD
   assessor has treated Teams as a collaborative computing device under
   SC.L2-3.13.12), ticketing systems (screenshots in tickets make the
   ticketing platform a CUI store), file-transfer portals, API integrations.
4. Break-glass accounts: they exist to bypass controls, which makes them
   in-scope privileged access; where are they stored and audited?
5. What CUI leaves: deliverables to the government, drawings to subs, media
   to customers. Every egress has an authorization answer (AC.L2-3.1.3,
   flow enforcement) and often an FCI/CUI marking answer.
6. Could a host on the corporate network reach a CUI asset if it tried?
   A theoretical path counts until a technical enforcement point removes
   it; a flat network makes everything one scope.

Writes: `topology.flows` additions, diagram-gap `open_questions`,
`decisions` for accepted-risk flows.

## Phase 12: backup-dr

**Entry criteria:** platforms and flows mapped. **Exit criteria:** every
backup target holding CUI is categorized; restore paths and DR sites are
in the inventory; the backup system's own protection story is written.

Core questions:

1. Where do backups of CUI systems land: appliance, tape, backup SaaS,
   secondary region? A target holding CUI backups is in scope even when the
   data is encrypted and immutable; who holds the keys matters to the
   conversation but the asset is still there.
2. The backup server or service holds credentials to everything it backs
   up. What protects it (the "forgotten backup system" is a staple
   finding)?
3. Tape and removable backup media: transport, storage, sanitization
   (MP family), and who signs custody.
4. DR: where does the environment come up, and does the DR site meet the
   same requirements? An untested DR region with a copy of the CUI store is
   an unassessed CUI asset.
5. Restore testing doubles as the forgotten-host hunt: what shows up in
   backup jobs that the inventory does not list?
6. SaaS-to-SaaS backup tools (M365 backup vendors): tenancy and FedRAMP
   posture, per the Phase 4 rules.
7. Name the backup platform exactly: on-premises appliance, backup SaaS,
   or CSP-native service. Each carries a different half of the scoping
   conversation (appliance: physical and management-plane questions;
   SaaS/CSP: the Phase 4 tenancy and authorization questions).
8. Is the encryption in the backup path FIPS-validated? SC.L2-3.13.11
   applies to CUI in the backup path like any other: the module doing
   the encrypting (appliance firmware crypto, agent TLS, the SaaS
   provider's module) needs a CMVP certificate for the deployed
   version, verified with `scripts/check_cmvp.py` and recorded in
   `cmvp_certificates`. "It's encrypted" without a validated module is
   the same gap the SSP's other encryption claims have.
9. Does the backup platform forward its own logs (job success/failure,
   admin actions, restore events) to the audit platform from Phase 10?

Writes: `assets` (backup targets), `topology.flows` (backup streams),
`cmvp_certificates` (backup path modules), `open_questions` for
unverified DR posture.

## After the twelfth phase

Run `python3 scripts/discovery_report.py <program-data>` and read the
result like an assessor: untouched phases are unexamined scope, open
questions are threads someone else will pull, unretired assumptions are
findings that have not happened yet. Then hand the file to the red-team
rail (`adversarial-challenge-catalog.md`), which exists to attack exactly
what this bank recorded.
