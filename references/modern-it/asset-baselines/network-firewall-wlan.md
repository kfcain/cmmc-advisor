# Network Firewall, Segmentation, and WLAN Baselines

> Source: NIST SP 800-171 Rev 2 (AC 3.1.3, 3.1.16/17; SC 3.13.1, 3.13.2,
> 3.13.6, 3.13.11); NIST CMVP; vendor documentation (Palo Alto, Fortinet,
> Cisco); CMMC Assessment Guide

## On-premises firewall / NGFW

Security protection assets. Document in SSP with enclave boundary diagram.

### Segmentation baseline

- CUI enclave on dedicated VLAN(s) or VRF; deny-by-default ACLs between
  enclave and corporate LAN
- Management plane on separate interface or restricted source IPs
- East-west rules between CUI subnets documented (SC.L2-3.13.1)
- MAC filtering: optional compensating control on small flat networks; document
  if used instead of 802.1X on a segment (not a substitute for WLAN encryption)

### FIPS 140 / FIPS-cc validated cryptography

SC.L2-3.13.11 requires **FIPS-validated modules** where cryptography protects
CUI. For firewalls:

1. Identify the **CMVP certificate** for the appliance model and OS version
   (vendor security data sheet or CMVP search).
2. Distinguish **FIPS-cc mode** (validated crypto module active) from generic
   "AES enabled" in IPsec/SSL-VPN settings.
3. Export `show system info` / `get system status` / equivalent showing FIPS mode
   when the vendor supports an explicit toggle (FortiGate FIPS-CC, Palo Alto FIPS
   mode where applicable).
4. Record certificate number in `cmvp_certificates` table when the appliance
   module is in scope for CUI VPN or TLS inspection.

Windows endpoint FIPS: `../endpoints/windows-fleet.md`. Cloud edge: Zscaler/Prisma
collectors in evidence manifest.

### Evidence automation

Collectors (stub/live org wiring):

- `fortinet-firewall`: policy and FIPS status export via FortiGate REST API
- `palo-alto-ngfw-onprem`: security rules and system info via PAN-OS XML/API

See `../security-operations/on-prem-inspectors.md`.

## WLAN baseline

Practices: AC.L2-3.1.16 (authorization), AC.L2-3.1.17 (authentication +
encryption).

| Control | Baseline |
|---------|----------|
| Inventory | Authorized APs and SSIDs listed; rogue AP detection or survey cadence |
| CUI SSID | WPA3-Enterprise or WPA2-Enterprise (802.1X); no PSK on CUI WLAN |
| Separation | Guest SSID isolated from CUI VLAN (firewall rules, not SSID name alone) |
| Management | Controller admin MFA; firmware patch record |
| Crypto | AES for data; deprecated protocols disabled (WEP, WPA-TKIP) |

Collector: `wlan-controller` (Aruba/Cisco/Mist-style REST stub).

## Logical + physical segmentation evidence

- Network diagram with VLAN IDs and firewall rule **names** (not just "firewall")
- Export of top deny rules proving guest and corp cannot reach CUI subnet
- WLAN controller SSID-to-VLAN mapping export
- Change tickets for last rule change affecting CUI boundary

## Program data example

```yaml
security_protection:
  - name: FortiGate 100F enclave edge
    vendor: Fortinet
    baseline_profile: network-firewall-onprem
    baseline_validation:
      validated: "2026-06-20"
      fips_cc_mode: true
      cmvp_certificate: "XXXX"
  - name: Aruba 7205 CUI WLAN
    baseline_profile: wlan-controller
    baseline_validation:
      validated: "2026-06-20"
      ssid_cui: EDS-CUI-8021X
      wpa: WPA3-Enterprise
```

## Common mistakes

- Flat network diagram with a single "firewall" icon and no rule narrative
- FIPS-cc claimed without CMVP citation for the deployed firmware train
- Guest Wi-Fi bridged to same VLAN as printers on CUI floor
