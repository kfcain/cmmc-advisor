# Remote Access, SASE, VPN, and Jump Path Scoping

> Source: NIST SP 800-171 Rev 2 (AC 3.1.12 through 3.1.15, SC 3.13.6 through
> 3.13.8); CMMC Assessment Guide Level 2; DoD CIO CMMC FAQ v2.3 (F-Q3, F-Q4,
> B-Q8); AWS Prescriptive Guidance CMMC Level 2 on AWS (June 2026)

Practitioner map for **components that touch the boundary but are easy to
mis-scope**: VPN concentrators, SASE/ZTNA, mesh overlays (Tailscale, WireGuard),
bastion hosts, session brokers, DNS/proxy paths, and enterprise transit gear.

Pair with `../endpoints/remote-work.md` (implementation), `network-firewall-wlan.md`
(FIPS and firewall categories), and `../../scoping-and-cui.md` (asset categories).

---

## Scoping rule of thumb

Ask four questions for every component:

1. **Does it process CUI in plaintext?** (decrypt, inspect, store, print, cache)
2. **Does it provide a security function the SSP relies on?** (segmentation, default-deny, remote access gate, MFA enforcement)
3. **Does it provide FIPS-validated cryptography for CUI?** (SC.L2-3.13.11 applies **here**, not everywhere ciphertext transits)
4. **Is logical separation documented?** (F-Q3: encryption alone is not separation; firewalls, VLANs, VPNs, ZTNA gates count)

DoD FAQ **F-Q4**: enterprise networking **outside** a logically separated enclave
that only carries **properly encrypted** CUI may stay **out of scope** when those
devices do not perform security functions described in the SSP. See
`network-firewall-wlan.md` for pass-through FIPS nuance (interpretive guidance
aligned with DoD FAQ, also discussed in public practitioner literature).

---

## Component matrix

| Component | Typical scoping category | SC.L2-3.13.11 (FIPS) | Primary practices | Evidence |
|-----------|-------------------------|----------------------|-------------------|----------|
| **SASE / ZTNA** (Zscaler, Prisma, Entra Private Access, Netskope) | Security protection (edge policy) | At the **service** if it terminates TLS/VPN for CUI | AC 3.1.12–15, SC 3.13.1, 3.13.7, 3.13.8 | `zscaler-policy`, `prisma-access-rules`; FedRAMP CRM |
| **IPsec/SSL VPN concentrator** ( terminates tunnel, inspects traffic) | CUI asset or SPA | **Yes** on concentrator if it provides confidentiality for CUI | AC 3.1.12–15, SC 3.13.7–8 | VPN config, cipher suite, CMVP if claimed |
| **Site-to-site VPN** (tunnel mode, no payload decrypt) | Often SPA (boundary) or out-of-scope transit | Usually **no** on transit router if only encapsulates | SC 3.13.1, 3.13.6 | Tunnel config, no inspection proof |
| **Tailscale / WireGuard mesh** | Varies: CRM, SPA, or CUI | On node if it **terminates** plaintext CUI; mesh crypto module if FIPS claimed | AC 3.1.12–15 if CUI crosses tailnet | ACL policy export, subnet router diagram, MFA |
| **Bastion / jump host** (Azure Bastion, EC2 jump, hardened admin box) | CUI or security protection | On bastion OS if admin sessions to CUI systems | AC 3.1.1, 3.1.12–15, AU 3.3.x, CM 3.4.x | Session logging, no direct RDP from internet |
| **VDI / session broker** (AVD, Citrix, Horizon) | Security protection + cloud CUI boundary | Broker and session host per cloud CRM + endpoint FIPS | See `vdi-thin-client.md` | Broker policy, redirection blocks |
| **Reverse proxy / WAF with TLS inspect** | **CUI asset** (processes plaintext) | **Yes** on inspect path | SC 3.13.1, 3.13.10, 3.13.11 | Proxy config, cert chain |
| **Internal DNS / DHCP** on CUI VLAN | Contractor risk managed or SPA | No unless DNSSEC/FIPS claimed for CUI | SC 3.13.1 (if boundary dependency) | Split horizon, logging |
| **Enterprise core router** (encrypted transit only, not in SSP) | Out of scope if F-Q4 four conditions met | **No** | None if truly out of scope | SSP exclusion narrative + diagram |
| **Perimeter NGFW** (segmentation, no decrypt) | Security protection | **No** unless SSL inspect or VPN terminate | SC 3.13.1, 3.13.6 | Rule export, diagram reference |

Collectors and env profiles: `../security-operations/README.md`, `on-prem-inspectors.md`.

---

## SASE vs traditional VPN

**SASE/ZTNA** replaces full-tunnel VPN with identity-per-session access to
named applications. CMMC still expects:

- MFA (IA.L2-3.5.3)
- Monitored remote access (AC.L2-3.1.12)
- Cryptographic protection (AC.L2-3.1.13, SC.L2-3.13.8)
- Routing through managed control points (AC.L2-3.1.14)
- No bypass of control points for CUI traffic (SC.L2-3.13.7)

Per-app tunneling **can** satisfy split-tunnel intent if CUI applications cannot
reach the internet directly without the SASE path. Document the data flow; do not
assume brand name equals compliance.

FedRAMP-authorized SASE is strongly preferred when the SASE provider processes
metadata or content. See `../../fedramp-marketplace-guide.md` (SASE/ZTNA section).

---

## Tailscale and mesh VPNs

Tailscale (WireGuard-based) appears in small shops and dev teams. Scoping depends
on **what rides the tailnet**:

| Pattern | Scoping | Notes |
|---------|---------|-------|
| Admin-only tailnet to jump boxes, no CUI file share | Security protection or CRM | Document ACLs; MFA on Tailscale admin |
| Subnet router advertising CUI VLAN | **In scope** as extension of enclave | Tailscale router is SPA; endpoints on tailnet may be CRM/CUI |
| Developers copy CUI repos over tailnet | **CUI path** | Treat tailnet like VPN; FIPS on endpoints doing crypto |
| MagicDNS + exit node with split routes | Review SC.L2-3.13.7 | Exit node can bypass corporate controls |

No dedicated collector yet: export ACL policy JSON, login audit, and diagram the
tailnet like any VPN. If CUI never uses Tailscale, state that in SSP and block
at firewall.

---

## Bastion hosts and break-glass access

**Azure Bastion**, **AWS Systems Manager Session Manager**, or a hardened **jump
box** in the CUI VPC are common admin paths.

- **In scope** at least as security protection (controlled admin entry).
- **CUI asset** if administrators paste CUI into RDP sessions that cache on the
  bastion or local clipboard redirection is enabled.
- Practices: no direct RDP/SSH from internet to CUI VMs (use bastion), MFA,
  session recording where feasible, AU logging, CM baseline on bastion OS.

Azure Bastion pattern: `../cloud-platforms/azure-government.md`. AWS multi-account
CMMC architecture: `../cloud-platforms/aws-govcloud.md` (CMMC prescriptive guide).

---

## AWS CMMC prescriptive guide (June 2026)

AWS publishes **Preparation guide for CMMC Level 2 on AWS** (Prescriptive Guidance):
multi-account Organizations layout, CUI boundary reference architecture, automated
evidence pipelines, GovCloud and commercial Regions with **FIPS endpoints**. Use it
when the enclave is AWS-native; map native services to practices via
`../cloud-platforms/aws-govcloud.md` and the capability appendix there.

Artifact package: **AWS CMMC Customer Package** in AWS Artifact for planning
documentation (not a substitute for your SSP).

---

## FIPS: not every device needs validation

SC.L2-3.13.11 applies where cryptography **protects CUI confidentiality**, not
necessarily every router that forwards ciphertext. Security protection firewalls
that **do not decrypt** and **do not provide crypto for CUI** are assessed on
their **security function** (segmentation, ACLs), not FIPS-cc mode on the appliance.

**Still requires FIPS-validated crypto:**

- Endpoints encrypting CUI (BitLocker, TLS client to GCC High)
- VPN/SASE **terminating** CUI tunnels with org-owned crypto
- SSL inspection proxies
- Storage (cloud FedRAMP + customer-side modules)

**Do not conflate:** FedRAMP for **storage/processing** CUI in cloud (DFARS 7012)
with transit-only pass-through (FAQ B-Q8, E-Q2). See `network-firewall-wlan.md`.

Public practitioner analysis of pass-through scoping (citing DoD FAQ F-Q4, B-Q8):
DEFCERT, "Not Every Device Needs to Be FIPS Validated" (2026). Interpretive; verify
against current DoD CIO FAQ before assessment.

---

## SSP documentation checklist

For each remote-access or edge component, SSP should state:

1. Asset category (CUI, SPA, CRM, out-of-scope)
2. Whether it decrypts or inspects CUI
3. Where FIPS-validated crypto is applied in the flow
4. Which AC/SC practices it satisfies
5. Evidence owner (link to `responsibility_matrix` in program data)

Run `scripts/validate_asset_baselines.py` after updating asset inventory.

---

## Common mistakes

- Listing every firewall as needing FIPS-cc mode
- Tailscale for "convenience" with CUI subnet router and no SSP entry
- SASE purchased but CUI still reachable via unmanaged SaaS (AC 3.1.12 gap)
- Bastion with clipboard redirection enabled into admin RDP
- Claiming F-Q4 out-of-scope for **perimeter** gear that the SSP cites for segmentation
