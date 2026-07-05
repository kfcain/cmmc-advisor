# DIB FedRAMP Security Tools (Rev 5 Class C / Class D)

> Source: FedRAMP Marketplace export (marketplace-fedramp-gov-data);
> FedRAMP Consolidated Rules 2026 preview (Class C Moderate, Class D High);
> references/grc/solution-selection.md; references/fedramp-marketplace-guide.md;
> CMMC Assessment Guide Level 2 (DoD CIO); NIST SP 800-171A assessment methods;
> vendor trust and government product pages cited in SOURCES.md

## Overview

Defense Industrial Base (DIB) contractors rarely run a single-vendor stack.
Typical CUI enclaves combine a **FedRAMP-authorized primary suite** (M365 GCC
High, Google Workspace Assured Controls Plus) with **point security tools** that
hold their own Marketplace packages. This file catalogs **commonly deployed DIB
security tools** with **Rev 5 Moderate (Class C equivalent)** or **Rev 5 High
(Class D equivalent)** authorization, maps them to CMMC practice families, and
routes evidence collection.

Read alongside:

- `references/grc/solution-selection.md` for Class C/D selection rules and 20x
- `references/fedramp-marketplace-guide.md` for Marketplace search patterns
- `references/data/fedramp-snapshot.json` (regenerate with
  `scripts/build_fedramp_snapshot.py`) for machine-readable package IDs
- `cloud-native-inspectors.md` and `on-prem-inspectors.md` for API collectors
- `references/grc/inherited-controls-mapping.md` when a tool is SaaS and you
  inherit CRM rows instead of re-implementing controls

**Verification discipline.** Package IDs and authorization status below reflect
the official Marketplace export timestamp in `fedramp-snapshot.json`. Re-run the
builder and confirm at marketplace.fedramp.gov before any SSP citation.

---

## Rev 5 Class C and Class D (practitioner shorthand)

| Marketplace signal | Impact | CMMC contractor use |
|--------------------|--------|---------------------|
| **Rev 5 Authorized, Moderate** | Moderate | **Class C floor** for CUI-touching SaaS under DFARS 7012 equivalence |
| **Rev 5 Authorized, High** | High | **Class D path** for high-impact CUI and many IL5-class workloads |
| **20x Class C Moderate** | Moderate | Accept when listing shows active 20x Moderate certification |
| **20x Class D High** | High | Emerging 20x High path; verify fedramp.gov before substituting for Rev5 High |
| **In Process / Ready / FRR** | varies | **Not cite-safe** in an SSP until status is Authorized |

FedRAMP authorization covers the **listed package boundary**, not every SKU or
feature in the vendor's commercial catalog. Map CRM Appendix J rows to CMMC
assessment objectives; do not assume "we bought the government SKU" satisfies a
practice without objective-level evidence.

---

## Capability catalog (DIB-common tools)

Each row lists a **representative FedRAMP package** commonly seen in DIB
programs. Alternate packages from the same vendor may exist; search the
Marketplace by vendor name before procurement.

### Endpoint detection and response (EDR / XDR)

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **SentinelOne Singularity Platform High** | FR1919071020A | High | Rev5 | SI (3.14.x), partial AU | Agent coverage export; threat detections; API or console |
| **CrowdStrike Falcon Platform for Government** | FR1807853629A | High | Rev5 | SI (3.14.x) | `crowdstrike-hosts` collector; GRC inspector bridge |
| **Microsoft Defender for Endpoint** | (inherits M365 GCC High) | High | Rev5 | SI (3.14.x) | `defender-endpoint` via Graph |
| **Palo Alto Networks Government Cloud Services** | FR1913470600 | Moderate | Rev5 | SI, SC | Cortex/XDR features vary by submodule; verify package scope |
| **Palo Alto GCS High** | FR2317253567 | High | Rev5 | SI, SC | High-tier workloads; confirm Cortex modules in boundary |

**Practitioner note:** Several vendors offer **Moderate and High** packages as
separate Marketplace entries. Pick the package that matches your CUI impact
decision; Moderate EDR on a High enclave is a common assessor finding.

### Vulnerability and exposure management

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Tenable Government Solutions** | FR1814276801 | Moderate | Rev5 | RA (3.11.x), SI (3.14.1) | Scan exports; asset inventory; credentialed scan proof |
| **Qualys Government Platform** | FR2231052341 | High | Rev5 | RA, SI | High-tier VM for sensitive enclaves |
| **Qualys Cloud Platform** | F1508207205 | Moderate | Rev5 | RA, SI | Moderate alternative |
| **Rapid7 InsightGovCloud** | FR2422240916 | Moderate | Rev5 | RA, SI | VM + appsec where in package scope |

### Identity, MFA, and privileged access

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Cisco Duo Federal** | FR1823149273 | Moderate | Rev5 | IA (3.5.2–3.5.3), AC | `duo-auth-logs` collector |
| **RSA ID Plus for Government** | FR2102652499 | Moderate | Rev5 | IA, AC | MFA and identity governance; not a full GRC suite |
| **Okta IDaaS Government High Cloud** | FR2131856836 | High | Rev5 | IA, AC | High-tier IdP |
| **BeyondTrust Identity Security for Government** | FR2231070252 | Moderate | Rev5 | IA, AC, PAM | PAM/session evidence where licensed |
| **Palo Alto Idira Identity Security Government** | FR2001619337 | High | Rev5 | IA, AC | Identity security platform (verify module scope) |

**RSA Archer GRC:** RSA **ID Plus** holds a current Rev5 Moderate package.
**Archer**-branded GRC may be customer-hosted or sold outside a standalone
FedRAMP SaaS boundary. Search marketplace.fedramp.gov for "Archer" at
procurement time; do not cite Archer from memory.

### SIEM, logging, and observability

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Splunk Cloud Platform FedRAMP High** | FR2314156865 | High | Rev5 | AU (3.3.x), SI (3.14.6) | `splunk-ingest-health`; retention and correlation |
| **Splunk Cloud Platform FedRAMP Moderate** | F1607197917 | Moderate | Rev5 | AU, SI | Moderate-tier logging |
| **Datadog for Government** | FR2023864279 | Moderate | Rev5 | AU, SI, CA | Metrics/logs/traces; map monitors to objectives |
| **Cisco ThousandEyes for Government** | FR2523656707 | Moderate | Rev5 | SC (3.13.x), AU (partial) | Network path and SaaS experience monitoring; not a SIEM replacement |

Datadog **High** package (FR2023864279A) was **In Process** at last snapshot;
verify before citing High workloads.

### Data security, DLP, and collaboration governance

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Varonis DatAdvantage Cloud** | FR2421252644 | Moderate | Rev5 | AC, MP, SC | Data access governance; entitlement and activity proof |
| **Varonis Data Security Platform** | FR2421252636 | Moderate | Rev5 | AC, MP, SC | Broader DSP boundary; confirm feature scope |
| **Forcepoint ONE SSE (CASB/DLP/SWG/ZTNA)** | FR1932554201 | Moderate | Rev5 | SC, MP, AC | SSE bundle; collect policy exports + forwarded logs |
| **Proofpoint Email and Information Protection** | FR1720461312 | Moderate | Rev5 | SC, SI | Email DLP and TAP where in package |
| **AvePoint Online Services for US Government** | FR2025827270 | Moderate | Rev5 | MP, AC, CM | M365/SharePoint governance, backup, migration tooling |

Native **Microsoft Purview** DLP inherits GCC High authorization when deployed
in that tenancy; AvePoint and Varonis are typical **third-party overlays** when
Purview coverage is insufficient.

### Network security, SASE, and ZTNA

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Zscaler Internet Access Government High** | FR2227062482 | High | Rev5 | SC (3.13.1, 3.13.6–8), AC | `zscaler-policy` collector |
| **Zscaler Private Access Government** | FR1719759604 | High | Rev5 | SC, AC | ZTNA replacement for VPN |
| **Netskope NewEdge Government** | FR2105946715 | High | Rev5 | SC, AC | SASE/SSE |
| **Palo Alto Prisma Access / GCS** | FR1913470600 / FR2317253567 | Mod / High | Rev5 | SC, AC | `prisma-access-rules` where SCM API applies |
| **Cisco Meraki for Government** | FR2315535023 | Moderate | Rev5 | SC, CM | WLAN/SD-WAN; pair with on-prem collector if hybrid |
| **Cisco Catalyst SD-WAN for Government** | FR2012534927 | Moderate | Rev5 | SC | WAN edge policy exports |

On-premises **PAN-OS** NGFW is not FedRAMP-authorized as bare metal; use
`on-prem-inspectors.md` and CIS/STIG baselines. **Strata Cloud Manager** applies
to cloud-managed Palo Alto services in authorized packages.

### ERP, GovCon systems, and program data

| Product | Package ID | Level | Rev | Primary CMMC families | Evidence notes |
|---------|------------|-------|-----|----------------------|----------------|
| **Deltek Costpoint GovCon Cloud Moderate** | FR2405880485 | Moderate | Rev5 | AC, AU, CM (program-dependent) | Status was **FRR** at last export, not Authorized; verify before SSP |
| **ServiceNow GCC** | F1305072116 | High | Rev5 | CA, CM, IR | ITSM/GRC modules; see legacy-dib-tools.md |

Deltek stores **contract and financial CUI** in many shops. Treat Costpoint like
any other CUI SaaS: Authorized package required, CRM mapped, scope boundary in
SSP.

### CMMC program platforms

| Product | Package ID | Level | Rev | Status at last export | Notes |
|---------|------------|-------|-----|----------------------|-------|
| **ATX Defense CMMC Space** | FR2618738935 | Moderate | Rev5 | **In Process** | CMMC workflow/collaboration platform; not cite-safe until Authorized |

CMMC Space and similar platforms **accelerate program management**; they do not
substitute for C3PAO assessment or replace evidence in program data.

---

## MSSP and MDR providers (Cyderes and similar)

**Cyderes** (and peer MSSPs/MDRs) typically **do not** appear as standalone
FedRAMP packages. They operate as **External Service Providers (ESPs)** using:

- Customer-owned FedRAMP-authorized tools (SentinelOne, Splunk, Tenable, etc.)
- Their own SOC tooling, which must stay **inside your authorization boundary**
  or be documented as inherited/shared per `references/grc/vendor-and-supply-chain.md`

For CMMC:

1. Record the MSSP in `program-data.yaml` vendor/ESP section with flowdown
   clauses (DFARS 252.204-7012, 7019, 7020 as applicable).
2. Map **which controls** the MSSP implements vs the OSC.
3. Collect evidence from **underlying platforms** (EDR console, SIEM queries),
   not MSSP marketing PDFs alone.
4. Do not claim FedRAMP inheritance from the MSSP brand; inherit from the
   **authorized SaaS package** named in the contract.

---

## CMMC practice mapping workflow

1. **Inventory** authorized tools touching CUI (this file + program data
   `inheritance_sources` / asset baselines).
2. **Map package to 800-53** using the vendor CRM and
   `references/data/800-53-crosswalk.json`.
3. **Trace to assessment objectives** per practice (for example, Duo logs to
   IA.L2-3.5.2 [a]–[d]; Tenable scans to RA.L2-3.11.2; Varonis to AC.L2-3.1.3
   and MP.L2-3.8.x where file activity is monitored).
4. **Mark conformity** only with objective-level evidence; use `partial` when the
   tool covers part of a practice (common for SIEM vs full AU family).
5. **Regenerate** dashboard and SSP after tool changes.

Gap-driven hints: `python3 scripts/recommend_solutions.py program-data.yaml --format md`

---

## Stack patterns seen in DIB enclaves

**Pattern A: Microsoft-centric with third-party overlays**

GCC High (identity, mail, Purview) + Duo or Entra MFA + SentinelOne or Defender
+ Sentinel or Splunk + Tenable + Zscaler or Entra Private Access.

**Pattern B: Multi-cloud with observability**

AWS GovCloud or Azure Government workloads + Datadog for Government + Palo Alto
SASE + CrowdStrike Falcon Gov + Qualys Gov.

**Pattern C: Data-centric manufacturing**

GCC High + Varonis or AvePoint for SharePoint/file governance + on-prem PAN-OS
(collector) + ThousandEyes for supplier portal path monitoring + Deltek
Costpoint (when Authorized) for contract data.

Each pattern still requires **scope diagrams** from `generate_diagrams.py` and
**CRM rows** for every inherited SaaS control.

---

## Related collectors and automation

| Tool family | Collector / bridge | File |
|-------------|-------------------|------|
| Duo | `duo-auth-logs` | cloud-native-inspectors.md |
| CrowdStrike | `crowdstrike-hosts` | cloud-native-inspectors.md |
| Zscaler | `zscaler-policy` | cloud-native-inspectors.md |
| Palo Alto SCM | `prisma-access-rules` | cloud-native-inspectors.md |
| Splunk | `splunk-ingest-health` | cloud-native-inspectors.md |
| PAN-OS on-prem | `palo-alto-ngfw-onprem` | on-prem-inspectors.md |
| Defender / Entra | Graph collectors | microsoft-graph-evidence.md |

Collectors ship **dry-run stubs** in this repo; live API pulls require customer
credentials. Tenable, Varonis, Datadog, ThousandEyes, and AvePoint evidence is
typically **scheduled exports** or GRC inspector integrations until dedicated
collectors are added.

---

## Cross-domain anchors

- **FedRAMP selection method:** `references/grc/solution-selection.md`
- **Category short-lists:** `references/fedramp-marketplace-guide.md`
- **ESP / subcontractor flowdown:** `references/grc/vendor-and-supply-chain.md`
- **Evidence automation:** `references/grc/evidence-automation.md`
- **Endpoint hub:** `references/modern-it/endpoints/README.md`

Content aligned to Marketplace export embedded in `fedramp-snapshot.json`
generated_at timestamp. Re-verify vendor status at procurement and SSP refresh.
