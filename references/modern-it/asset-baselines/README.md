# Asset Baselines by Type

> Source: 32 CFR 170.19(c) asset categories; NIST SP 800-171 Rev 2; CMMC
> Assessment Guide Level 2; NIST CMVP; vendor public hardening guides

Practitioner hub for **baseline expectations, scoping treatment, and evidence**
by asset class. Pair with `references/scoping-and-cui.md` for category
definitions and `templates/program-data.schema.json` for inventory fields.

## Why this layer exists

CMMC scoping names five asset categories (CUI, security protection, contractor
risk managed, specialized, out-of-scope). Endpoint and cloud guidance lives under
`references/modern-it/endpoints/` and `cloud-platforms/`. Many assessments still
fail on **printers, physical access hardware, on-prem firewalls, WLAN, thin
clients, and OT** because those assets sit in CRM or security-protection scope
without a written baseline or evidence plan.

This directory gives one reference file per class plus a machine-readable catalog
at `references/data/asset-baseline-manifest.json`.

## Baseline profile catalog

| Profile id | Asset class | Reference |
|------------|-------------|-----------|
| `vdi-thin-client-igel` | VDI terminals, IGEL/Citrix/Horizon thin clients | `vdi-thin-client.md` |
| `printer-mfp` | Printers, MFPs, print servers | `printers-mfp.md` |
| `network-firewall-onprem` | On-prem NGFW, segmentation, FIPS-cc mode | `network-firewall-wlan.md` |
| `wlan-controller` | WLAN controllers, APs, 802.1X | `network-firewall-wlan.md` |
| `physical-access-pacs` | Badges, readers, keys, visitor logs | `physical-access.md` |
| `specialized-ot` | OT, GFE, IoT, test equipment | `specialized-ot.md` |
| `development-sdlc` | Dev/test pipelines touching CUI (3.13.2) | `development-sdlc.md` |
| `remote-access-scope` | SASE, VPN, Tailscale, bastion, jump paths | `remote-access-scope.md` |
| `msp-rmm-platform` | MSP/RMM on CUI endpoints (NinjaOne, Endpoint Central, etc.) | `msp-rmm-tools.md` |
| `cis-appliance-onprem` | Firewalls, switches, WLAN, PACS without FedRAMP | `cis-appliance-baselines.md` |

Assign `baseline_profile` on each asset row in program data. Run:

```bash
python3 scripts/validate_asset_baselines.py templates/program-data.sample.yaml
python3 scripts/generate_responsibility_matrix.py templates/program-data.sample.yaml
```

On-prem API collectors (firewall, WLAN, PACS) register in
`references/data/evidence-collector-manifest.json` and are documented in
`references/modern-it/security-operations/on-prem-inspectors.md`.

## Internal RACI vs FedRAMP CRM

**Customer Responsibility Matrix (CRM):** vendor inheritance for FedRAMP CSPs.
See `references/grc/inherited-controls-mapping.md` and `grc/vendor-and-supply-chain.md`.

**Internal responsibility matrix:** who on *your* team (and MSP) owns each
practice family or requirement. Stored in program data as `responsibility_matrix`;
exported with `scripts/generate_responsibility_matrix.py`. See
`references/grc/responsibility-matrix.md`.

## Cross-links

- Endpoints (Windows/macOS/mobile): `../endpoints/README.md`
- VDI session containment (capability-level): `../endpoints/remote-work.md`
- Network domain practices: `../../domains/sc-system-comms.md`
- Physical protection: `../../domains/pe-physical-protection.md`
- Evidence automation: `../../grc/evidence-automation.md`
