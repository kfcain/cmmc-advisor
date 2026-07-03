# Specialized and OT Asset Baselines

> Source: 32 CFR 170.19(c); CMMC Level 2 scoping; Level 3 specialized asset
> requirements (`references/level-3-expert.md`)

## Level 2

Specialized assets (GFE, OT, IIoT, lab equipment) may interact with CUI but
cannot always run standard endpoint controls. Document:

1. Asset inventory with manufacturer, network attachment, and CUI interaction
   (process, store, transmit, or none)
2. Compensating controls: network isolation, monitoring, manual procedures
3. CRMA narrative if the asset is contractor risk managed
4. What you **cannot** do (no AV agent, no domain join) and why that is accepted

Sample in program data: `CNC-07 controller` on isolated VLAN.

## Baseline template per specialized asset

| Field | Content |
|-------|---------|
| Network zone | Dedicated VLAN, firewall deny-by-default to CUI subnet |
| Protocol | Modbus/OPC/etc.; encrypted tunnel if crossing zones |
| Patching | Vendor-approved maintenance window; MA.L2-3.7.6 narrative |
| Monitoring | SIEM flow logs, anomaly detection, physical access to panel |
| CUI path | Does drawing/CUI file ever rest on OT HMI? If yes, treat as CUI |
| Level 3 delta | SI.L3-3.14.3e specialized asset security if pursuing L3 |

## Evidence

- One-line diagram: OT cell, conduit, firewall rules
- Risk entry linking asset to RA.L2-3.11.1 scoring
- Maintenance log sample
- Photo of physical lock on PLC cabinet (supports PE chain)

## Common mistakes

- Declaring OT "out of scope" while engineering laptops bridge VLANs
- No CRMA entry for shared printer on OT maintenance laptop
