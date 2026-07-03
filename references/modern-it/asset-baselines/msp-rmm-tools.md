# MSP and RMM Tools (Endpoint Central, NinjaOne, ConnectWise, etc.)

> Source: DFARS 252.204-7012(b)(2)(ii)(D); 32 CFR 170.4, 170.17(c)(5)-(6);
> DoD CIO ESP scoping guidance; `references/grc/vendor-and-supply-chain.md`;
> FedRAMP Marketplace (verify current authorization before contract)

Remote Monitoring and Management (RMM) and MSP-operated endpoint platforms
(NinjaOne, ManageEngine Endpoint Central, ConnectWise Automate/Control,
Datto RMM, N-able, etc.) are a common **scope expansion** when agents land on
CUI endpoints or technicians remote into CUI systems through vendor cloud
consoles.

## The rule

**If the RMM/MSP platform touches CUI assets** (agent on CUI endpoint, remote
shell/file browse into CUI systems, backup of CUI volumes, patch inventory of
CUI devices, screenshots/session capture from CUI desktops):

| Platform role | Minimum authorization floor |
|---------------|----------------------------|
| **Cloud SaaS (CSP)** storing/processing/transmitting **CUI** or that can reach CUI | **FedRAMP Moderate** (Rev 5 agency path) **or** **FedRAMP 20x Class C (Moderate impact)** with current Marketplace listing |
| **Cloud SaaS** handling **SPD only** (telemetry, no CUI content path) | Assessed in **your** scope as security protection; FedRAMP not mandatory under ESP matrix but **strongly recommended** for same reasons as CUI-capable RMM |
| **On-premises** RMM server in **your** enclave | Not a CSP; server is **your** CUI/SPA asset; MSP **people and access** still assessed in your scope |

DFARS 7012 is explicit for **CSP + CUI**. Practitioner standard for defense
work: **do not deploy commercial multi-tenant RMM clouds on CUI endpoints**
unless that exact product SKU is FedRAMP Moderate (or 20x Class C Moderate)
authorized. "NIST aligned" marketing is not authorization.

FedRAMP 20x **Class C (Moderate)** is the modern certification class for many
new SaaS authorizations (example: **NinjaOne for Government**, Marketplace
package FR2430847803, FedRAMP Certified Rev 5). Treat **Class C Moderate** as
equivalent floor to legacy **FedRAMP Moderate** for due diligence unless your
contracting officer directs otherwise.

---

## Why RMM is high risk for CUI

RMM capabilities overlap CMMC families:

| RMM capability | CMMC touch | Data sensitivity |
|----------------|------------|------------------|
| Remote control / file transfer | AC 3.1.12–15, AU 3.3.x | **CUI** if technician opens CUI files |
| Inventory / config | CM 3.4.x, CA 3.12.x | **SPD**; may include paths, users, SW list |
| Patch deployment | CM 3.4.x, SI 3.14.x | **SPD**; supply chain if malicious package |
| Script execution | CM, SI, AC | **CUI** if scripts run in user context |
| Backup (if enabled) | MP, SC | **CUI** if volumes include CUI |
| Ticketing/docs in vendor cloud | AT, PS | **CUI** if tickets contain CUI text |

Assume the **vendor cloud can become a CUI store** unless architecture
proves otherwise (no file browse, no backup, no ticket CUI, read-only
telemetry only). That pushes you to FedRAMP Moderate / Class C for the SaaS.

---

## Vendor patterns (verify Marketplace before award)

| Product | Typical deployment | CMMC note |
|---------|-------------------|-----------|
| **NinjaOne for Government** | FedRAMP Moderate SaaS (US persons) | Use **government SKU**, not commercial NinjaOne tenant, for CUI endpoints |
| **ManageEngine Endpoint Central** | Cloud or **on-premises** ECMP | Commercial cloud is **not** a substitute for FedRAMP on CUI; on-prem shifts scope to **your** server + hardened MSP access |
| **ConnectWise / Datto / N-able** | MSP multi-tenant cloud | Check Marketplace per product; most commercial stacks are **not** authorized for CUI |
| **Microsoft Intune / Defender** | GCC High tenant | Preferred pattern: CUI endpoints in **customer GCC High**, MSP as delegated admin with **your** tenant accounts (CRM inheritance) |

Run `scripts/build_fedramp_snapshot.py` or search [FedRAMP Marketplace](https://fedramp.gov/marketplace/) before SSP citation. Date-stamp verification per `SOURCES.md`.

---

## Architecture options (enabler paths)

### 1. FedRAMP-authorized RMM SKU (preferred when MSP insists on RMM)

- Contract for **NinjaOne for Government** or other **Moderate / Class C** listing
- US-person support boundary; no commingling CUI agents with commercial MSP customers
- CRM in SSP; map inherited vs customer controls
- Disable or policy-block: backup of CUI drives, arbitrary file export, screen recording to vendor cloud unless assessed

### 2. Customer tenant management (preferred for GCC High shops)

- CUI endpoints in **Intune + Defender** (GCC High); MSP uses **delegated admin** or PIM roles **in your tenant**
- RMM limited to non-CUI or absent on CUI VLAN
- AC/IA/AU evidence from Entra/Defender collectors (`entra-signins`, `defender-endpoint`)

### 3. On-premises RMM in enclave

- ManageEngine ECMP or similar **inside** CUI boundary
- Patch server, RMM DB, and backup targets are **CUI assets**
- MSP VPN/jump access documented in `remote-access-scope.md`
- Still document MSP personnel (PS, AC) in ESP section of SSP

### 4. No compliant RMM available (gap honest)

- Identify gap; interim: manual patching cadence, Intune native policies, documented MSP SOP without remote file browse
- POA&M only if eligible; prefer close before CUI assessment
- Do not claim inherited FedRAMP from a non-authorized vendor

---

## MSP access model

| Model | Scope impact |
|-------|----------------|
| MSP tech uses **named account in your Entra/AD** | Your AC/IA/AU controls apply; better assessor story |
| MSP uses **shared vendor portal** into your agents | Vendor cloud + MSP IdP in scope; needs FedRAMP on that cloud |
| MSP **L1/L2 remote** without session recording | AU gaps; document or add SIEM forwarding |

Pin MSP duties in `responsibility_matrix` and `inheritance_sources` (if CRM exists).

---

## Evidence checklist

- FedRAMP Marketplace screenshot or snapshot JSON for **exact product SKU**
- Contract clause: DFARS 7012 flowdown, incident cooperation, US-person if required
- CRM or ESP service description in SSP
- Agent deployment list: which endpoints are CUI vs corporate
- Policy: no CUI file paths in RMM backup/tickets; remote session rules
- Sample audit log: MSP remote session into CUI enclave (redacted)

---

## Program data example

```yaml
security_protection:
  - name: NinjaOne for Government (CUI endpoints only)
    vendor: NinjaOne
    baseline_profile: msp-rmm-platform
    baseline_validation:
      validated: "2026-07-01"
      fedramp_package_id: FR2430847803
      authorization: FedRAMP Moderate Rev5 Class C
      cui_agents: 12
      commercial_tenant_segregated: true
```

---

## Common mistakes

- Commercial NinjaOne/Datto on CUI laptops because "the MSP uses it everywhere"
- ManageEngine cloud marketed as "NIST 800-171 compliant" without FedRAMP
- RMM backup jobs including CUI profile or mapped drives
- Same MSP portal credentials across CUI and non-CUI customers
- Treating RMM as out of scope because "the MSP is certified" (ESP is assessed **in your** scope unless they hold their own CMMC)

See also: `../../grc/vendor-and-supply-chain.md`, `remote-access-scope.md`,
`../endpoints/README.md` (FedRAMP overlap for endpoint management).
