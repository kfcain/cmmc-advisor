# VDI and Thin Client Baselines (IGEL Worked Example)

> Source: CMMC Assessment Guide Level 2; NIST SP 800-171 Rev 2 (3.1.12 through
> 3.1.15, 3.4.1, 3.13.4, PE.L2-3.10.6); vendor IGEL documentation
> (igel.com/community)

## Scope decision

A thin client is **out of scope** only when it is a true terminal: CUI never
persists on local storage, and session policy blocks exfiltration paths. If CUI
can land on the device (clipboard, print, USB, local drive mapping, offline
cache), treat the device as **contractor risk managed** or **CUI** and apply
full endpoint baselines from `../endpoints/windows-fleet.md` or the VDI vendor
hardening guide.

Capability patterns: `../endpoints/remote-work.md`.

## IGEL out-of-scope validation checklist

Use this checklist before claiming an IGEL (or similar) endpoint is out of scope.
Record results in program data under `baseline_validation` on the asset row.

| # | Control | Pass criteria | Evidence |
|---|---------|---------------|----------|
| 1 | Session broker | CUI sessions terminate only in FedRAMP-authorized VDI/DaaS | Broker config export, SSP boundary diagram |
| 2 | Clipboard | Copy/paste from session to local device disabled (both directions) | IGEL UMS policy export or Citrix/Horizon GPO equivalent |
| 3 | Printing | Printer redirection disabled; no local USB printers for CUI | Session policy export; user interview |
| 4 | USB / storage | USB mass storage and device redirection blocked | UMS device policy export |
| 5 | Local disk | No persistent user profile storing CUI; cache cleared on logout | UMS partition/cache policy |
| 6 | Drive mapping | No mapped drives to local or home shares for CUI sessions | Broker + thin client policy |
| 7 | Network | Thin client reaches only broker/gateway, not CUI VLAN directly | Firewall rules, network diagram |
| 8 | Encryption | If any local cache exists, encryption at rest enforced | BitLocker/FileVault on repurposed PCs acting as thin clients |
| 9 | PE alternate site | Home office safeguards documented if users work remotely | PE.L2-3.10.6 narrative, clean desk, visitor policy |
| 10 | Shared resources | SC.L2-3.13.4: no CUI residue in shared session resources | Broker session cleanup settings |

**Program data:** set `baseline_profile: vdi-thin-client-igel` and complete
`baseline_validation.checklist_id: igel-out-of-scope` with dated attestation.

## When IGEL stays in scope

- Repurposed PC running IGEL OS with local troubleshooting partitions enabled
- Clipboard or print allowed "for productivity"
- USB allowed for keyboards only but storage class not blocked
- Split tunnel VPN on the thin client to corporate LAN

## Primary CMMC practices

- AC.L2-3.1.12 through 3.1.15 (remote access)
- CM.L2-3.4.1 (configuration baseline on managed terminals)
- SC.L2-3.13.4 (shared resource control at broker)
- PE.L2-3.10.6 (alternate work site when terminal is at home)

## Common assessor tests

- Attempt copy from CUI session to local notepad
- Inspect print queue on local OS during session
- Review UMS policy version history and change ticket
