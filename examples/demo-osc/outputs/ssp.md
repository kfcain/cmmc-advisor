# System Security Plan (SSP)

**Organization:** Atlas Precision Manufacturing LLC  
**System:** APM GCC High CUI Enclave  
**Date:** 2026-07-05  
**Revision:** Rev 2

## Record of Acceptance/Approval

System Owner: Jordan Rivera, Director of Engineering

Printed Name: ______________________  Date: ____________  Signature: ______________________

## Purpose

Demo OSC for CMMC Advisor toolkit walkthrough

## Scope

Atlas Precision Manufacturing (APM) machines vehicle components for an Army prime. CUI (CTI and export-controlled drawings) is processed only in a Microsoft 365 GCC High tenant, twelve Intune-managed Windows laptops, Azure Government file services, and Microsoft Sentinel. Commercial M365, corporate HR/finance, and IGEL thin-client VDI terminals are out of scope with documented separation. Paper CUI (marked CTI hardcopy, traveler drawings, mail pouches) is in scope for the CUI floor mail room, locked job boxes, and cross-cut destruction path; digital CUI remains in GCC High.

## References

- Federal Information Security Modernization Act (FISMA) of 2014
- 32 CFR Part 2002, Controlled Unclassified Information
- 48 CFR 52.204-21, Basic Safeguarding of Covered Contractor Information Systems
- DFARS 252.204-7012, Safeguarding Covered Defense Information and Cyber Incident Reporting
- NIST SP 800-171 Revision 2 and NIST SP 800-171A
- 32 CFR Part 170, Cybersecurity Maturity Model Certification (CMMC) Program

## Roles & Responsibilities

**System Owner**: Jordan Rivera, Director of Engineering

**Affirming Official**: Casey Morgan, CEO
- Affirm continuing compliance in SPRS

**Issm**: Sam Patel, ISSM / IT Security Lead
- Maintain SSP, POA&M, and program-data.yaml
- Run quarterly evidence collection and SPRS updates

**Engineer Lead**: Alex Kim, Cloud Engineering Lead
- ControlBot profile and Terraform enclave IaC

## System Environment

Primary enclave: GCC High (Entra ID USGov, EXO/SPO/Teams), Azure Government (Sentinel, project file share). Edge: FortiGate 100F. RMM: NinjaOne for Government on CUI laptops only. Engineering uses Azure DevOps Government for IaC; ControlBot gates Terraform PRs.

## Asset Types

### CUI Assets

| Asset | Description | Vendor |
|-------|-------------|--------|
| M365 GCC High tenant (Exchange, SharePoint, Teams) | CUI storage, processing, and transmission | Microsoft |
| ENG laptops (12, Intune-managed, BitLocker) | CUI processing endpoints |  |
| CUI mail room (Building A Room 104) | Inbound/outbound hardcopy staging, cover-sheet log, locked shred console |  |
| Locked CUI job boxes (12, ENG floor) | Orange CUI asset stickers; keys on PE access list |  |

### Contractor Risk Managed Assets

| Asset | Description | Vendor |
|-------|-------------|--------|
| HP MFP Floor-2 |  |  |
| HSM cross-cut shredder (Model HSM-150) | Destroy sanitization for daily paper CUI; strip-cut prohibited by policy |  |

### Security Protection Assets

| Asset | Description | Vendor |
|-------|-------------|--------|
| Microsoft Sentinel (Azure Government) | SIEM ingesting enclave logs | Microsoft |
| FortiGate 100F enclave edge |  | Fortinet |
| NinjaOne for Government (ENG CUI laptops only) | FedRAMP Moderate RMM; segregated from MSP commercial tenants | NinjaOne |
| Certified destruction vendor (NAID AAA) | Quarterly bulk purge with certificate of destruction | SecureShred Regional |

### Specialized Assets

| Asset | Description | Vendor |
|-------|-------------|--------|
| CNC-07 controller | OT device on isolated VLAN, documented in SSP |  |

### Out-of-Scope Assets

| Asset | Description | Vendor |
|-------|-------------|--------|
| IGEL UD3 thin clients (8) | VDI terminals; CUI session only in Azure Virtual Desktop | IGEL |

## Networking Diagrams

- Figure 1, Network diagram: outputs/diagrams/network.svg (generate with scripts/generate_diagrams.py from the topology section)
- Figure 2, CUI flow diagram: outputs/diagrams/cui-flow.svg (generate with scripts/generate_diagrams.py from the topology section)

## Hardware and Software Information

*To be completed from the asset inventory.*

## Access Control [AC] Family

### AC.L2-3.1.1: Authorized Access Control

> Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** authorized users are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Authorized users are identified in Entra ID Government. The engineering security group ENG-CUI is the single authorization source for enclave access; membership requires a signed access request approved by the system owner.
- Evidence: ENG-CUI group membership export (evidence/ac/3.1.1/group-export-2026-06.csv)
- Evidence: Access request procedure (evidence/ac/3.1.1/access-request-procedure-v3.pdf)

**[b]** processes acting on behalf of authorized users are identified

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

**[c]** devices (and other systems) authorized to connect to the system are identified

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

**[d]** system access is limited to authorized users

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Conditional Access policy CA-01 blocks all access to the tenant except from compliant, Intune-enrolled devices by ENG-CUI members with phishing-resistant MFA.
- Evidence: CA-01 policy export (evidence/ac/3.1.1/ca-01-export.json)

**[e]** system access is limited to processes acting on behalf of authorized users

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

**[f]** system access is limited to authorized devices (including other systems)

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

### AC.L2-3.1.2: Transaction & Function Control

> Limit system access to the types of transactions and functions that authorized users are permitted to execute.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the types of transactions and functions that authorized users are permitted to execute are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Transaction & Function Control objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.2 [a] (evidence/demo/AC-L2-3-1-2-a.json)

**[b]** system access is limited to the defined types of transactions and functions for authorized users

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Transaction & Function Control objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.2 [b] (evidence/demo/AC-L2-3-1-2-b.json)

### AC.L2-3.1.3: Control CUI Flow

> Control the flow of CUI in accordance with approved authorizations.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** information flow control policies are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control CUI Flow objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.3 [a] (evidence/demo/AC-L2-3-1-3-a.json)
- Evidence: Bucket ACL or policy exposes object reads to the internet. (terraform/storage.tf:12)
- Evidence: Bucket policy allows public read access. (terraform/storage.tf:12)

**[b]** methods and enforcement mechanisms for controlling the flow of CUI are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control CUI Flow objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.3 [b] (evidence/demo/AC-L2-3-1-3-b.json)

**[c]** designated sources and destinations (e.g., networks, individuals, and devices) for CUI within the system and between interconnected systems are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control CUI Flow objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.3 [c] (evidence/demo/AC-L2-3-1-3-c.json)

**[d]** authorizations for controlling the flow of CUI are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control CUI Flow objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.3 [d] (evidence/demo/AC-L2-3-1-3-d.json)

**[e]** approved authorizations for controlling the flow of CUI are enforced

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control CUI Flow objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.3 [e] (evidence/demo/AC-L2-3-1-3-e.json)

### AC.L2-3.1.4: Separation of Duties

> Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the duties of individuals requiring separation are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Separation of Duties objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.4 [a] (evidence/demo/AC-L2-3-1-4-a.json)

**[b]** responsibilities for duties that require separation are assigned to separate individuals

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Separation of Duties objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.4 [b] (evidence/demo/AC-L2-3-1-4-b.json)

**[c]** access privileges that enable individuals to exercise the duties that require separation are granted to separate individuals

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Separation of Duties objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.4 [c] (evidence/demo/AC-L2-3-1-4-c.json)

### AC.L2-3.1.5: Least Privilege

> Employ the principle of least privilege, including for specific security functions and privileged accounts.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** privileged accounts are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Privilege objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.5 [a] (evidence/demo/AC-L2-3-1-5-a.json)

**[b]** access to privileged accounts is authorized in accordance with the principle of least privilege

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Privilege objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.5 [b] (evidence/demo/AC-L2-3-1-5-b.json)

**[c]** security functions are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Privilege objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.5 [c] (evidence/demo/AC-L2-3-1-5-c.json)

**[d]** access to security functions is authorized in accordance with the principle of least privilege

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Privilege objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.5 [d] (evidence/demo/AC-L2-3-1-5-d.json)

### AC.L2-3.1.6: Non-Privileged Account Use

> Use non-privileged accounts or roles when accessing nonsecurity functions.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** nonsecurity functions are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Non-Privileged Account Use objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.6 [a] (evidence/demo/AC-L2-3-1-6-a.json)

**[b]** users are required to use non-privileged accounts or roles when accessing nonsecurity functions

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Non-Privileged Account Use objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.6 [b] (evidence/demo/AC-L2-3-1-6-b.json)

### AC.L2-3.1.7: Privileged Functions

> Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** privileged functions are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Functions objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.7 [a] (evidence/demo/AC-L2-3-1-7-a.json)

**[b]** non-privileged users are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Functions objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.7 [b] (evidence/demo/AC-L2-3-1-7-b.json)

**[c]** non-privileged users are prevented from executing privileged functions

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Functions objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.7 [c] (evidence/demo/AC-L2-3-1-7-c.json)

**[d]** the execution of privileged functions is captured in audit logs

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Functions objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.7 [d] (evidence/demo/AC-L2-3-1-7-d.json)

### AC.L2-3.1.8: Unsuccessful Logon Attempts

> Limit unsuccessful logon attempts.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the means of limiting unsuccessful logon attempts is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Unsuccessful Logon Attempts objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.8 [a] (evidence/demo/AC-L2-3-1-8-a.json)

**[b]** the defined means of limiting unsuccessful logon attempts is implemented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Unsuccessful Logon Attempts objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.8 [b] (evidence/demo/AC-L2-3-1-8-b.json)

### AC.L2-3.1.9: Privacy & Security Notices

> Provide privacy and security notices consistent with applicable CUI rules.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** privacy and security notices required by CUI-specified rules are identified, consistent, and associated with the specific CUI category

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privacy & Security Notices objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.9 [a] (evidence/demo/AC-L2-3-1-9-a.json)

**[b]** privacy and security notices are displayed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privacy & Security Notices objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.9 [b] (evidence/demo/AC-L2-3-1-9-b.json)

### AC.L2-3.1.10: Session Lock

> Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the period of inactivity after which the system initiates a session lock is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Session Lock objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.10 [a] (evidence/demo/AC-L2-3-1-10-a.json)

**[b]** access to the system and viewing of data is prevented by initiating a session lock after the defined period of inactivity

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Session Lock objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.10 [b] (evidence/demo/AC-L2-3-1-10-b.json)

**[c]** previously visible information is concealed via a pattern-hiding display after the defined period of inactivity

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Session Lock objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.10 [c] (evidence/demo/AC-L2-3-1-10-c.json)

### AC.L2-3.1.11: Session Termination

> Terminate (automatically) a user session after a defined condition.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** conditions requiring a user session to terminate are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Session Termination objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.11 [a] (evidence/demo/AC-L2-3-1-11-a.json)

**[b]** a user session is automatically terminated after any of the defined conditions occur

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Session Termination objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.11 [b] (evidence/demo/AC-L2-3-1-11-b.json)

### AC.L2-3.1.12: Control Remote Access

> Monitor and control remote access sessions.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** remote access sessions are permitted

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Remote Access objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.12 [a] (evidence/demo/AC-L2-3-1-12-a.json)

**[b]** the types of permitted remote access are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Remote Access objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.12 [b] (evidence/demo/AC-L2-3-1-12-b.json)

**[c]** remote access sessions are controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Remote Access objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.12 [c] (evidence/demo/AC-L2-3-1-12-c.json)

**[d]** remote access sessions are monitored

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Remote Access objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.12 [d] (evidence/demo/AC-L2-3-1-12-d.json)

### AC.L2-3.1.13: Remote Access Confidentiality

> Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** cryptographic mechanisms to protect the confidentiality of remote access sessions are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Remote Access Confidentiality objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.13 [a] (evidence/demo/AC-L2-3-1-13-a.json)

**[b]** cryptographic mechanisms to protect the confidentiality of remote access sessions are implemented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Remote Access Confidentiality objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.13 [b] (evidence/demo/AC-L2-3-1-13-b.json)

### AC.L2-3.1.14: Remote Access Routing

> Route remote access via managed access control points.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** managed access control points are identified and implemented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Remote Access Routing objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.14 [a] (evidence/demo/AC-L2-3-1-14-a.json)

**[b]** remote access is routed through managed network access control points

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Remote Access Routing objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.14 [b] (evidence/demo/AC-L2-3-1-14-b.json)

### AC.L2-3.1.15: Privileged Remote Access

> Authorize remote execution of privileged commands and remote access to security-relevant information.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** privileged commands authorized for remote execution are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Remote Access objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.15 [a] (evidence/demo/AC-L2-3-1-15-a.json)

**[b]** security-relevant information authorized to be accessed remotely is identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Remote Access objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.15 [b] (evidence/demo/AC-L2-3-1-15-b.json)

**[c]** the execution of the identified privileged commands via remote access is authorized

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Remote Access objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.15 [c] (evidence/demo/AC-L2-3-1-15-c.json)

**[d]** access to the identified security-relevant information via remote access is authorized

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Privileged Remote Access objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.15 [d] (evidence/demo/AC-L2-3-1-15-d.json)

### AC.L2-3.1.16: Wireless Access Authorization

> Authorize wireless access prior to allowing such connections.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** wireless access points are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Wireless Access Authorization objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.16 [a] (evidence/demo/AC-L2-3-1-16-a.json)

**[b]** wireless access is authorized prior to allowing such connections

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Wireless Access Authorization objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.16 [b] (evidence/demo/AC-L2-3-1-16-b.json)

### AC.L2-3.1.17: Wireless Access Protection

> Protect wireless access using authentication and encryption.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** wireless access to the system is protected using authentication

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Wireless Access Protection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.17 [a] (evidence/demo/AC-L2-3-1-17-a.json)

**[b]** wireless access to the system is protected using encryption

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Wireless Access Protection objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.17 [b] (evidence/demo/AC-L2-3-1-17-b.json)

### AC.L2-3.1.18: Mobile Device Connection

> Control connection of mobile devices.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** mobile devices that process, store, or transmit CUI are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Mobile Device Connection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.18 [a] (evidence/demo/AC-L2-3-1-18-a.json)

**[b]** mobile device connections are authorized

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Mobile Device Connection objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.18 [b] (evidence/demo/AC-L2-3-1-18-b.json)

**[c]** mobile device connections are monitored and logged

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Mobile Device Connection objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.18 [c] (evidence/demo/AC-L2-3-1-18-c.json)

### AC.L2-3.1.19: Encrypt CUI on Mobile

> Encrypt CUI on mobile devices and mobile computing platforms.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** mobile devices and mobile computing platforms that process, store, or transmit CUI are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Encrypt CUI on Mobile objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.19 [a] (evidence/demo/AC-L2-3-1-19-a.json)

**[b]** encryption is employed to protect CUI on identified mobile devices and mobile computing platforms

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Encrypt CUI on Mobile objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.19 [b] (evidence/demo/AC-L2-3-1-19-b.json)

### AC.L2-3.1.20: External Connections

> Verify and control/limit connections to and use of external systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** connections to external systems are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [a] (evidence/demo/AC-L2-3-1-20-a.json)

**[b]** the use of external systems is identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [b] (evidence/demo/AC-L2-3-1-20-b.json)

**[c]** connections to external systems are verified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [c] (evidence/demo/AC-L2-3-1-20-c.json)

**[d]** the use of external systems is verified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [d] (evidence/demo/AC-L2-3-1-20-d.json)

**[e]** connections to external systems are controlled/limited

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [e] (evidence/demo/AC-L2-3-1-20-e.json)

**[f]** the use of external systems is controlled/limited

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: External Connections objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.20 [f] (evidence/demo/AC-L2-3-1-20-f.json)

### AC.L2-3.1.21: Portable Storage Use

> Limit use of portable storage devices on external systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the use of portable storage devices containing CUI on external systems is identified and documented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Portable Storage Use objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.21 [a] (evidence/demo/AC-L2-3-1-21-a.json)

**[b]** limits on the use of portable storage devices containing CUI on external systems are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Portable Storage Use objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.21 [b] (evidence/demo/AC-L2-3-1-21-b.json)

**[c]** the use of portable storage devices containing CUI on external systems is limited as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Portable Storage Use objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.21 [c] (evidence/demo/AC-L2-3-1-21-c.json)

### AC.L2-3.1.22: Control Public Information

> Control CUI posted or processed on publicly accessible systems.

**REQUIREMENT CONFORMITY:** NOT MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** individuals authorized to post or process information on publicly accessible systems are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Public Information objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.22 [a] (evidence/demo/AC-L2-3-1-22-a.json)

**[b]** procedures to ensure CUI is not posted or processed on publicly accessible systems are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Public Information objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.22 [b] (evidence/demo/AC-L2-3-1-22-b.json)

**[c]** a review process is in place prior to posting of any content to publicly accessible systems

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Public Information objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.22 [c] (evidence/demo/AC-L2-3-1-22-c.json)

**[d]** content on publicly accessible systems is reviewed to ensure that it does not include CUI

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Public Information objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.22 [d] (evidence/demo/AC-L2-3-1-22-d.json)

**[e]** mechanisms are in place to remove and address improper posting of CUI

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Control Public Information objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AC.L2-3.1.22 [e] (evidence/demo/AC-L2-3-1-22-e.json)


## Awareness & Training [AT] Family

### AT.L2-3.2.1: Role-Based Risk Awareness

> Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** security risks associated with organizational activities involving CUI are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Risk Awareness objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.1 [a] (evidence/demo/AT-L2-3-2-1-a.json)

**[b]** policies, standards, and procedures related to the security of the system are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Risk Awareness objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.1 [b] (evidence/demo/AT-L2-3-2-1-b.json)

**[c]** managers, systems administrators, and users of the system are made aware of the security risks associated with their activities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Risk Awareness objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.1 [c] (evidence/demo/AT-L2-3-2-1-c.json)

**[d]** managers, systems administrators, and users of the system are made aware of the applicable policies, standards, and procedures related to the security of the system

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Risk Awareness objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.1 [d] (evidence/demo/AT-L2-3-2-1-d.json)

### AT.L2-3.2.2: Role-Based Training

> Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** information security-related duties, roles, and responsibilities are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Training objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.2 [a] (evidence/demo/AT-L2-3-2-2-a.json)

**[b]** information security-related duties, roles, and responsibilities are assigned to designated personnel

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Training objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.2 [b] (evidence/demo/AT-L2-3-2-2-b.json)

**[c]** personnel are adequately trained to carry out their assigned information securityrelated duties, roles, and responsibilities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role-Based Training objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.2 [c] (evidence/demo/AT-L2-3-2-2-c.json)

### AT.L2-3.2.3: Insider Threat Awareness

> Provide security awareness training on recognizing and reporting potential indicators of insider threat.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** potential indicators associated with insider threats are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Insider Threat Awareness objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.3 [a] (evidence/demo/AT-L2-3-2-3-a.json)

**[b]** security awareness training on recognizing and reporting potential indicators of insider threat is provided to managers and employees

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Insider Threat Awareness objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AT.L2-3.2.3 [b] (evidence/demo/AT-L2-3-2-3-b.json)


## Audit & Accountability [AU] Family

### AU.L2-3.3.1: System Auditing

> Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** audit logs needed (i.e., event types to be logged) to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity are specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [a] (evidence/demo/AU-L2-3-3-1-a.json)

**[b]** the content of audit records needed to support monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [b] (evidence/demo/AU-L2-3-3-1-b.json)

**[c]** audit records are created (generated)

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [c] (evidence/demo/AU-L2-3-3-1-c.json)

**[d]** audit records, once created, contain the defined content

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [d] (evidence/demo/AU-L2-3-3-1-d.json)

**[e]** retention requirements for audit records are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [e] (evidence/demo/AU-L2-3-3-1-e.json)

**[f]** audit records are retained as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Auditing objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.1 [f] (evidence/demo/AU-L2-3-3-1-f.json)

### AU.L2-3.3.2: User Accountability

> Ensure that the actions of individual system users can be uniquely traced to those users so they can be held accountable for their actions.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the content of the audit records needed to support the ability to uniquely trace users to their actions is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: User Accountability objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.2 [a] (evidence/demo/AU-L2-3-3-2-a.json)

**[b]** audit records, once created, contain the defined content

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: User Accountability objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.2 [b] (evidence/demo/AU-L2-3-3-2-b.json)

### AU.L2-3.3.3: Event Review

> Review and update logged events.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a process for determining when to review logged events is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Event Review objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.3 [a] (evidence/demo/AU-L2-3-3-3-a.json)

**[b]** event types being logged are reviewed in accordance with the defined review process

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Event Review objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.3 [b] (evidence/demo/AU-L2-3-3-3-b.json)

**[c]** event types being logged are updated based on the review

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Event Review objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.3 [c] (evidence/demo/AU-L2-3-3-3-c.json)

### AU.L2-3.3.4: Audit Failure Alerting

> Alert in the event of an audit logging process failure.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** personnel or roles to be alerted in the event of an audit logging process failure are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Failure Alerting objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.4 [a] (evidence/demo/AU-L2-3-3-4-a.json)

**[b]** types of audit logging process failures for which alert will be generated are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Failure Alerting objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.4 [b] (evidence/demo/AU-L2-3-3-4-b.json)

**[c]** identified personnel or roles are alerted in the event of an audit logging process failure

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Failure Alerting objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.4 [c] (evidence/demo/AU-L2-3-3-4-c.json)

### AU.L2-3.3.5: Audit Correlation

> Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

**REQUIREMENT CONFORMITY:** NOT MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity are defined

- AO CONFORMITY: NOT MET
- Assessment Objective Conformity Statement: Audit record review processes are not yet correlated across sources. Sentinel collects enclave logs but correlation rules and the weekly review runbook are not implemented.

**[b]** defined audit record review, analysis, and reporting processes are correlated

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

**Remediation plan:** Sentinel workspace exists and ingests all enclave sources. Remaining work is detection content and the operating rhythm. Note: AU.L2-3.3.5 carries 5 SPRS points and is not POA&M-eligible under 32 CFR 170.21(a)(2)(ii); close this gap before assessment or accept the score deduction.

### AU.L2-3.3.6: Reduction & Reporting

> Provide audit record reduction and report generation to support on-demand analysis and reporting.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** an audit record reduction capability that supports on-demand analysis is provided

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Reduction & Reporting objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.6 [a] (evidence/demo/AU-L2-3-3-6-a.json)

**[b]** a report generation capability that supports on-demand reporting is provided

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Reduction & Reporting objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.6 [b] (evidence/demo/AU-L2-3-3-6-b.json)

### AU.L2-3.3.7: Authoritative Time Source

> Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** internal system clocks are used to generate time stamps for audit records

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authoritative Time Source objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.7 [a] (evidence/demo/AU-L2-3-3-7-a.json)

**[b]** an authoritative source with which to compare and synchronize internal system clocks is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authoritative Time Source objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.7 [b] (evidence/demo/AU-L2-3-3-7-b.json)

**[c]** internal system clocks used to generate time stamps for audit records are compared to and synchronized with the specified authoritative time source

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authoritative Time Source objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.7 [c] (evidence/demo/AU-L2-3-3-7-c.json)

### AU.L2-3.3.8: Audit Protection

> Protect audit information and audit logging tools from unauthorized access, modification, and deletion.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** audit information is protected from unauthorized access

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [a] (evidence/demo/AU-L2-3-3-8-a.json)

**[b]** audit information is protected from unauthorized modification

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [b] (evidence/demo/AU-L2-3-3-8-b.json)

**[c]** audit information is protected from unauthorized deletion

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [c] (evidence/demo/AU-L2-3-3-8-c.json)

**[d]** audit logging tools are protected from unauthorized access

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [d] (evidence/demo/AU-L2-3-3-8-d.json)

**[e]** audit logging tools are protected from unauthorized modification

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [e] (evidence/demo/AU-L2-3-3-8-e.json)

**[f]** audit logging tools are protected from unauthorized deletion

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Protection objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.8 [f] (evidence/demo/AU-L2-3-3-8-f.json)

### AU.L2-3.3.9: Audit Management

> Limit management of audit logging functionality to a subset of privileged users.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a subset of privileged users granted access to manage audit logging functionality is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Management objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.9 [a] (evidence/demo/AU-L2-3-3-9-a.json)

**[b]** management of audit logging functionality is limited to the defined subset of privileged users

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Audit Management objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — AU.L2-3.3.9 [b] (evidence/demo/AU-L2-3-3-9-b.json)


## Configuration Management [CM] Family

### CM.L2-3.4.1: System Baselining

> Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a baseline configuration is established

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [a] (evidence/demo/CM-L2-3-4-1-a.json)
- Evidence: Terraform declares aws_s3_bucket.cui_exports. (terraform/storage.tf:12)

**[b]** the baseline configuration includes hardware, software, firmware, and documentation

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [b] (evidence/demo/CM-L2-3-4-1-b.json)

**[c]** the baseline configuration is maintained (reviewed and updated) throughout the system development life cycle

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [c] (evidence/demo/CM-L2-3-4-1-c.json)

**[d]** a system inventory is established

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [d] (evidence/demo/CM-L2-3-4-1-d.json)

**[e]** the system inventory includes hardware, software, firmware, and documentation

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [e] (evidence/demo/CM-L2-3-4-1-e.json)

**[f]** the inventory is maintained (reviewed and updated) throughout the system development life cycle

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Baselining objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.1 [f] (evidence/demo/CM-L2-3-4-1-f.json)

### CM.L2-3.4.2: Security Configuration Enforcement

> Establish and enforce security configuration settings for information technology products employed in organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** security configuration settings for information technology products employed in the system are established and included in the baseline configuration

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Configuration Enforcement objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.2 [a] (evidence/demo/CM-L2-3-4-2-a.json)
- Evidence: Terraform declares aws_s3_bucket.cui_exports. (terraform/storage.tf:12)

**[b]** security configuration settings for information technology products employed in the system are enforced

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Configuration Enforcement objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.2 [b] (evidence/demo/CM-L2-3-4-2-b.json)

### CM.L2-3.4.3: System Change Management

> Track, review, approve or disapprove, and log changes to organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** changes to the system are tracked

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Change Management objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.3 [a] (evidence/demo/CM-L2-3-4-3-a.json)

**[b]** changes to the system are reviewed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Change Management objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.3 [b] (evidence/demo/CM-L2-3-4-3-b.json)

**[c]** changes to the system are approved or disapproved

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Change Management objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.3 [c] (evidence/demo/CM-L2-3-4-3-c.json)

**[d]** changes to the system are logged

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Change Management objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.3 [d] (evidence/demo/CM-L2-3-4-3-d.json)

### CM.L2-3.4.4: Security Impact Analysis

> Analyze the security impact of changes prior to implementation.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the security impact of changes to the system is analyzed prior to implementation

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Impact Analysis objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.4 [a] (evidence/demo/CM-L2-3-4-4-a.json)

### CM.L2-3.4.5: Access Restrictions for Change

> Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** physical access restrictions associated with changes to the system are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [a] (evidence/demo/CM-L2-3-4-5-a.json)

**[b]** physical access restrictions associated with changes to the system are documented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [b] (evidence/demo/CM-L2-3-4-5-b.json)

**[c]** physical access restrictions associated with changes to the system are approved

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [c] (evidence/demo/CM-L2-3-4-5-c.json)

**[d]** physical access restrictions associated with changes to the system are enforced

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [d] (evidence/demo/CM-L2-3-4-5-d.json)

**[e]** logical access restrictions associated with changes to the system are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [e] (evidence/demo/CM-L2-3-4-5-e.json)

**[f]** logical access restrictions associated with changes to the system are documented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [f] (evidence/demo/CM-L2-3-4-5-f.json)

**[g]** logical access restrictions associated with changes to the system are approved

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective g satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [g] (evidence/demo/CM-L2-3-4-5-g.json)

**[h]** logical access restrictions associated with changes to the system are enforced

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Access Restrictions for Change objective h satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.5 [h] (evidence/demo/CM-L2-3-4-5-h.json)

### CM.L2-3.4.6: Least Functionality

> Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** essential system capabilities are defined based on the principle of least functionality

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Functionality objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.6 [a] (evidence/demo/CM-L2-3-4-6-a.json)

**[b]** the system is configured to provide only the defined essential capabilities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Least Functionality objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.6 [b] (evidence/demo/CM-L2-3-4-6-b.json)

### CM.L2-3.4.7: Nonessential Functionality

> Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

**REQUIREMENT CONFORMITY:** NOT MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** essential programs are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [a] (evidence/demo/CM-L2-3-4-7-a.json)

**[b]** the use of nonessential programs is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [b] (evidence/demo/CM-L2-3-4-7-b.json)

**[c]** the use of nonessential programs is restricted, disabled, or prevented as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [c] (evidence/demo/CM-L2-3-4-7-c.json)

**[d]** essential functions are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [d] (evidence/demo/CM-L2-3-4-7-d.json)

**[e]** the use of nonessential functions is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [e] (evidence/demo/CM-L2-3-4-7-e.json)

**[f]** the use of nonessential functions is restricted, disabled, or prevented as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [f] (evidence/demo/CM-L2-3-4-7-f.json)

**[g]** essential ports are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective g satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [g] (evidence/demo/CM-L2-3-4-7-g.json)

**[h]** the use of nonessential ports is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective h satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [h] (evidence/demo/CM-L2-3-4-7-h.json)

**[i]** the use of nonessential ports is restricted, disabled, or prevented as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective i satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [i] (evidence/demo/CM-L2-3-4-7-i.json)

**[j]** essential protocols are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective j satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [j] (evidence/demo/CM-L2-3-4-7-j.json)

**[k]** the use of nonessential protocols is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective k satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [k] (evidence/demo/CM-L2-3-4-7-k.json)

**[l]** the use of nonessential protocols is restricted, disabled, or prevented as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective l satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [l] (evidence/demo/CM-L2-3-4-7-l.json)

**[m]** essential services are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective m satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [m] (evidence/demo/CM-L2-3-4-7-m.json)

**[n]** the use of nonessential services is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective n satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [n] (evidence/demo/CM-L2-3-4-7-n.json)

**[o]** the use of nonessential services is restricted, disabled, or prevented as defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonessential Functionality objective o satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.7 [o] (evidence/demo/CM-L2-3-4-7-o.json)

### CM.L2-3.4.8: Application Execution Policy

> Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a policy specifying whether whitelisting or blacklisting is to be implemented is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Application Execution Policy objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.8 [a] (evidence/demo/CM-L2-3-4-8-a.json)

**[b]** the software allowed to execute under whitelisting or denied use under blacklisting is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Application Execution Policy objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.8 [b] (evidence/demo/CM-L2-3-4-8-b.json)

**[c]** whitelisting to allow the execution of authorized software or blacklisting to prevent the use of unauthorized software is implemented as specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Application Execution Policy objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.8 [c] (evidence/demo/CM-L2-3-4-8-c.json)

### CM.L2-3.4.9: User-Installed Software

> Control and monitor user-installed software.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a policy for controlling the installation of software by users is established

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: User-Installed Software objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.9 [a] (evidence/demo/CM-L2-3-4-9-a.json)

**[b]** installation of software by users is controlled based on the established policy

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: User-Installed Software objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.9 [b] (evidence/demo/CM-L2-3-4-9-b.json)

**[c]** installation of software by users is monitored

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: User-Installed Software objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CM.L2-3.4.9 [c] (evidence/demo/CM-L2-3-4-9-c.json)


## Identification & Authentication [IA] Family

### IA.L2-3.5.1: Identification

> Identify system users, processes acting on behalf of users, and devices.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** system users are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identification objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.1 [a] (evidence/demo/IA-L2-3-5-1-a.json)

**[b]** processes acting on behalf of users are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identification objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.1 [b] (evidence/demo/IA-L2-3-5-1-b.json)

**[c]** devices accessing the system are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identification objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.1 [c] (evidence/demo/IA-L2-3-5-1-c.json)

### IA.L2-3.5.2: Authentication

> Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the identity of each user is authenticated or verified as a prerequisite to system access

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authentication objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.2 [a] (evidence/demo/IA-L2-3-5-2-a.json)

**[b]** the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authentication objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.2 [b] (evidence/demo/IA-L2-3-5-2-b.json)

**[c]** the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Authentication objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.2 [c] (evidence/demo/IA-L2-3-5-2-c.json)

### IA.L2-3.5.3: Multifactor Authentication

> Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

**REQUIREMENT CONFORMITY:** PARTIALLY MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** privileged accounts are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Multifactor Authentication objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.3 [a] (evidence/demo/IA-L2-3-5-3-a.json)

**[b]** multifactor authentication is implemented for local access to privileged accounts

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Multifactor Authentication objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.3 [b] (evidence/demo/IA-L2-3-5-3-b.json)

**[c]** multifactor authentication is implemented for network access to privileged accounts

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Multifactor Authentication objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.3 [c] (evidence/demo/IA-L2-3-5-3-c.json)

**[d]** multifactor authentication is implemented for network access to non-privileged accounts

- AO CONFORMITY: NOT MET
- Assessment Objective Conformity Statement: Demo OSC: Multifactor Authentication objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.3 [d] (evidence/demo/IA-L2-3-5-3-d.json)

### IA.L2-3.5.4: Replay-Resistant Authentication

> Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Replay-Resistant Authentication objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.4 [a] (evidence/demo/IA-L2-3-5-4-a.json)

### IA.L2-3.5.5: Identifier Reuse

> Prevent reuse of identifiers for a defined period.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a period within which identifiers cannot be reused is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identifier Reuse objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.5 [a] (evidence/demo/IA-L2-3-5-5-a.json)

**[b]** reuse of identifiers is prevented within the defined period

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identifier Reuse objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.5 [b] (evidence/demo/IA-L2-3-5-5-b.json)

### IA.L2-3.5.6: Identifier Handling

> Disable identifiers after a defined period of inactivity.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a period of inactivity after which an identifier is disabled is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identifier Handling objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.6 [a] (evidence/demo/IA-L2-3-5-6-a.json)

**[b]** identifiers are disabled after the defined period of inactivity

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identifier Handling objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.6 [b] (evidence/demo/IA-L2-3-5-6-b.json)

### IA.L2-3.5.7: Password Complexity

> Enforce a minimum password complexity and change of characters when new passwords are created.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** password complexity requirements are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Complexity objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.7 [a] (evidence/demo/IA-L2-3-5-7-a.json)

**[b]** password change of character requirements are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Complexity objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.7 [b] (evidence/demo/IA-L2-3-5-7-b.json)

**[c]** minimum password complexity requirements as defined are enforced when new passwords are created

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Complexity objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.7 [c] (evidence/demo/IA-L2-3-5-7-c.json)

**[d]** minimum password change of character requirements as defined are enforced when new passwords are created

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Complexity objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.7 [d] (evidence/demo/IA-L2-3-5-7-d.json)

### IA.L2-3.5.8: Password Reuse

> Prohibit password reuse for a specified number of generations.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the number of generations during which a password cannot be reused is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Reuse objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.8 [a] (evidence/demo/IA-L2-3-5-8-a.json)

**[b]** reuse of passwords is prohibited during the specified number of generations

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Password Reuse objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.8 [b] (evidence/demo/IA-L2-3-5-8-b.json)

### IA.L2-3.5.9: Temporary Passwords

> Allow temporary password use for system logons with an immediate change to a permanent password.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** an immediate change to a permanent password is required when a temporary password is used for system logon

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Temporary Passwords objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.9 [a] (evidence/demo/IA-L2-3-5-9-a.json)

### IA.L2-3.5.10: Cryptographically-Protected Passwords

> Store and transmit only cryptographically-protected passwords.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** passwords are cryptographically protected in storage

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Cryptographically-Protected Passwords objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.10 [a] (evidence/demo/IA-L2-3-5-10-a.json)

**[b]** passwords are cryptographically protected in transit

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Cryptographically-Protected Passwords objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.10 [b] (evidence/demo/IA-L2-3-5-10-b.json)

### IA.L2-3.5.11: Obscure Feedback

> Obscure feedback of authentication information.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** authentication information is obscured during the authentication process

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Obscure Feedback objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IA.L2-3.5.11 [a] (evidence/demo/IA-L2-3-5-11-a.json)


## Incident Response [IR] Family

### IR.L2-3.6.1: Incident Handling

> Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** an operational incident-handling capability is established

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [a] (evidence/demo/IR-L2-3-6-1-a.json)

**[b]** the operational incident-handling capability includes preparation

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [b] (evidence/demo/IR-L2-3-6-1-b.json)

**[c]** the operational incident-handling capability includes detection

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [c] (evidence/demo/IR-L2-3-6-1-c.json)

**[d]** the operational incident-handling capability includes analysis

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [d] (evidence/demo/IR-L2-3-6-1-d.json)

**[e]** the operational incident-handling capability includes containment

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [e] (evidence/demo/IR-L2-3-6-1-e.json)

**[f]** the operational incident-handling capability includes recovery

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [f] (evidence/demo/IR-L2-3-6-1-f.json)

**[g]** the operational incident-handling capability includes user response activities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Handling objective g satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.1 [g] (evidence/demo/IR-L2-3-6-1-g.json)

### IR.L2-3.6.2: Incident Reporting

> Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** incidents are tracked

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [a] (evidence/demo/IR-L2-3-6-2-a.json)

**[b]** incidents are documented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [b] (evidence/demo/IR-L2-3-6-2-b.json)

**[c]** authorities to whom incidents are to be reported are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [c] (evidence/demo/IR-L2-3-6-2-c.json)

**[d]** organizational officials to whom incidents are to be reported are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [d] (evidence/demo/IR-L2-3-6-2-d.json)

**[e]** identified authorities are notified of incidents

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [e] (evidence/demo/IR-L2-3-6-2-e.json)

**[f]** identified organizational officials are notified of incidents

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Reporting objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.2 [f] (evidence/demo/IR-L2-3-6-2-f.json)

### IR.L2-3.6.3: Incident Response Testing

> Test the organizational incident response capability.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the incident response capability is tested

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Incident Response Testing objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — IR.L2-3.6.3 [a] (evidence/demo/IR-L2-3-6-3-a.json)


## Maintenance [MA] Family

### MA.L2-3.7.1: Perform Maintenance

> Perform maintenance on organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** system maintenance is performed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Perform Maintenance objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.1 [a] (evidence/demo/MA-L2-3-7-1-a.json)

### MA.L2-3.7.2: System Maintenance Control

> Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** tools used to conduct system maintenance are controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Maintenance Control objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.2 [a] (evidence/demo/MA-L2-3-7-2-a.json)

**[b]** techniques used to conduct system maintenance are controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Maintenance Control objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.2 [b] (evidence/demo/MA-L2-3-7-2-b.json)

**[c]** mechanisms used to conduct system maintenance are controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Maintenance Control objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.2 [c] (evidence/demo/MA-L2-3-7-2-c.json)

**[d]** personnel used to conduct system maintenance are controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Maintenance Control objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.2 [d] (evidence/demo/MA-L2-3-7-2-d.json)

### MA.L2-3.7.3: Equipment Sanitization

> Ensure equipment removed for off-site maintenance is sanitized of any CUI.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** equipment to be removed from organizational spaces for off-site maintenance is sanitized of any CUI

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Equipment Sanitization objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.3 [a] (evidence/demo/MA-L2-3-7-3-a.json)

### MA.L2-3.7.4: Media Inspection

> Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** media containing diagnostic and test programs are checked for malicious code before being used in organizational systems that process, store, or transmit CUI

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Media Inspection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.4 [a] (evidence/demo/MA-L2-3-7-4-a.json)

### MA.L2-3.7.5: Nonlocal Maintenance

> Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** multifactor authentication is used to establish nonlocal maintenance sessions via external network connections

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonlocal Maintenance objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.5 [a] (evidence/demo/MA-L2-3-7-5-a.json)

**[b]** nonlocal maintenance sessions established via external network connections are terminated when nonlocal maintenance is complete

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Nonlocal Maintenance objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.5 [b] (evidence/demo/MA-L2-3-7-5-b.json)

### MA.L2-3.7.6: Maintenance Personnel

> Supervise the maintenance activities of maintenance personnel without required access authorization.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** maintenance personnel without required access authorization are supervised during maintenance activities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Maintenance Personnel objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MA.L2-3.7.6 [a] (evidence/demo/MA-L2-3-7-6-a.json)


## Media Protection [MP] Family

### MP.L2-3.8.1: Media Protection

> Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.

**REQUIREMENT CONFORMITY:** PARTIALLY MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** paper media containing CUI is physically controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Paper CUI at rest in locked job boxes and locked file cabinets on the CUI floor; orange CUI stickers on each container.
- Evidence: CUI asset sticker inventory (evidence/mp/paper/cui-asset-sticker-inventory-2026-06.json)
- Evidence: PE access list for job-box keys (evidence/mp/paper/job-box-key-register-2026-06.csv)

**[b]** digital media containing CUI is physically controlled

- AO CONFORMITY: NOT MET
- Assessment Objective Conformity Statement: Mail-room pre-shred accumulation shelf is not locked overnight; POA&M tracks lockable console install.

**[c]** paper media containing CUI is securely stored

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

**[d]** digital media containing CUI is securely stored

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

### MP.L2-3.8.2: Media Access

> Limit access to CUI on system media to authorized users.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** access to CUI on system media is limited to authorized users

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Media Access objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MP.L2-3.8.2 [a] (evidence/demo/MP-L2-3-8-2-a.json)

### MP.L2-3.8.3: Media Disposal

> Sanitize or destroy system media containing CUI before disposal or release for reuse.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** system media containing CUI is sanitized or destroyed before disposal

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Paper CUI destroyed via cross-cut shredding (HSM-150) with dual-person witness log, or NAID AAA vendor with certificate of destruction. No recycling bins for CUI.
- Evidence: Shred witness log (evidence/mp/paper/shred-witness-log-2026-06.csv)
- Evidence: NAID destruction certificate Q1 (evidence/mp/paper/naid-destruction-cert-2026-q1.pdf)
- Evidence: Paper CUI destruction procedure (policies/paper-cui-handling-v1.2.pdf)

**[b]** system media containing CUI is sanitized before it is released for reuse

- AO CONFORMITY: NOT ASSESSED
- Assessment Objective Conformity Statement: Assessment objective has not been assessed.

### MP.L2-3.8.4: Media Markings

> Mark media with necessary CUI markings and distribution limitations.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** media containing CUI is marked with applicable CUI markings

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: CTI banner and portion markings applied per 32 CFR 2002; CUI cover sheets on all external transmittals.
- Evidence: Redacted cover sheet sample (evidence/mp/paper/cui-cover-sheet-sample-redacted.pdf)
- Evidence: Marking standard excerpt (evidence/mp/paper/cui-marking-standard-excerpt.pdf)

**[b]** media containing CUI is marked with distribution limitations

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Distribution limitations (NOFORN where applicable) on cover sheets and document headers.
- Evidence: Training roster — paper CUI marking (evidence/mp/paper/marking-training-roster-2026-05.csv)

### MP.L2-3.8.5: Media Accountability

> Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** access to media containing CUI is controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Only mail-room clerks and ISSM may remove paper CUI from the CUI floor; authorization logged on cover sheet.
- Evidence: Mail/courier authorization procedure (procedures/cui-mail-courier-v1.pdf)

**[b]** accountability for media containing CUI is maintained during transport outside of controlled areas

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Chain-of-custody forms for FedEx and internal courier; signature on delivery.
- Evidence: FedEx chain of custody 2026-06-12 (evidence/mp/paper/chain-of-custody-fedex-2026-06-12.pdf)
- Evidence: Chain of custody blank template (procedures/shred-chain-of-custody-v1.pdf)

### MP.L2-3.8.6: Portable Storage Encryption

> Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the confidentiality of CUI stored on digital media is protected during transport using cryptographic mechanisms or alternative physical safeguards

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Portable Storage Encryption objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MP.L2-3.8.6 [a] (evidence/demo/MP-L2-3-8-6-a.json)

### MP.L2-3.8.7: Removeable Media

> Control the use of removable media on system components.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the use of removable media on system components is controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Removeable Media objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MP.L2-3.8.7 [a] (evidence/demo/MP-L2-3-8-7-a.json)

### MP.L2-3.8.8: Shared Media

> Prohibit the use of portable storage devices when such devices have no identifiable owner.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the use of portable storage devices is prohibited when such devices have no identifiable owner

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Shared Media objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MP.L2-3.8.8 [a] (evidence/demo/MP-L2-3-8-8-a.json)

### MP.L2-3.8.9: Protect Backups

> Protect the confidentiality of backup CUI at storage locations.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the confidentiality of backup CUI is protected at storage locations

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Protect Backups objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — MP.L2-3.8.9 [a] (evidence/demo/MP-L2-3-8-9-a.json)


## Personnel Security [PS] Family

### PS.L2-3.9.1: Screen Individuals

> Screen individuals prior to authorizing access to organizational systems containing CUI.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** individuals are screened prior to authorizing access to organizational systems containing CUI

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Screen Individuals objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — PS.L2-3.9.1 [a] (evidence/demo/PS-L2-3-9-1-a.json)

### PS.L2-3.9.2: Personnel Actions

> Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a policy and/or process for terminating system access and any credentials coincident with personnel actions is established

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Personnel Actions objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — PS.L2-3.9.2 [a] (evidence/demo/PS-L2-3-9-2-a.json)

**[b]** system access and credentials are terminated consistent with personnel actions such as termination or transfer

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Personnel Actions objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — PS.L2-3.9.2 [b] (evidence/demo/PS-L2-3-9-2-b.json)

**[c]** the system is protected during and after personnel transfer actions

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Personnel Actions objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — PS.L2-3.9.2 [c] (evidence/demo/PS-L2-3-9-2-c.json)


## Physical Protection [PE] Family

### PE.L2-3.10.1: Limit Physical Access

> Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** authorized individuals allowed physical access are identified

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[b]** physical access to organizational systems is limited to authorized individuals

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[c]** physical access to equipment is limited to authorized individuals

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[d]** physical access to operating environments is limited to authorized individuals

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

### PE.L2-3.10.2: Monitor Facility

> Protect and monitor the physical facility and support infrastructure for organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the physical facility where organizational systems reside is protected

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[b]** the support infrastructure for organizational systems is protected

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[c]** the physical facility where organizational systems reside is monitored

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[d]** the support infrastructure for organizational systems is monitored

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

### PE.L2-3.10.3: Escort Visitors

> Escort visitors and monitor visitor activity.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** visitors are escorted

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[b]** visitor activity is monitored

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

### PE.L2-3.10.4: Physical Access Logs

> Maintain audit logs of physical access.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** audit logs of physical access are maintained

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

### PE.L2-3.10.5: Manage Physical Access

> Control and manage physical access devices.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** physical access devices are identified

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[b]** physical access devices are controlled

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[c]** physical access devices are managed

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

### PE.L2-3.10.6: Alternative Work Sites

> Enforce safeguarding measures for CUI at alternate work sites.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** safeguarding measures for CUI are defined for alternate work sites

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/

**[b]** safeguarding measures for CUI are enforced for alternate work sites

- AO CONFORMITY: MET (INHERITED)
- Assessment Objective Conformity Statement: Physical protection for the GCC High boundary is inherited from Microsoft 365 GCC High per CRM Appendix J; no customer-operated datacenter for this enclave.
- Inheritance: Inherited from Microsoft Microsoft 365 GCC High; CRM ref: PE family rows (Appendix J); CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/


## Risk Assessment [RA] Family

### RA.L2-3.11.1: RIsk Assessments

> Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the frequency to assess risk to organizational operations, organizational assets, and individuals is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: RIsk Assessments objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.1 [a] (evidence/demo/RA-L2-3-11-1-a.json)

**[b]** risk to organizational operations, organizational assets, and individuals resulting from the operation of an organizational system that processes, stores, or transmits CUI is assessed with the defined frequency

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: RIsk Assessments objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.1 [b] (evidence/demo/RA-L2-3-11-1-b.json)

### RA.L2-3.11.2: Vulnerability Scan

> Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the frequency to scan for vulnerabilities in organizational systems and applications is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Scan objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.2 [a] (evidence/demo/RA-L2-3-11-2-a.json)

**[b]** vulnerability scans are performed on organizational systems with the defined frequency

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Scan objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.2 [b] (evidence/demo/RA-L2-3-11-2-b.json)

**[c]** vulnerability scans are performed on applications with the defined frequency

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Scan objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.2 [c] (evidence/demo/RA-L2-3-11-2-c.json)

**[d]** vulnerability scans are performed on organizational systems when new vulnerabilities are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Scan objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.2 [d] (evidence/demo/RA-L2-3-11-2-d.json)

**[e]** vulnerability scans are performed on applications when new vulnerabilities are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Scan objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.2 [e] (evidence/demo/RA-L2-3-11-2-e.json)

### RA.L2-3.11.3: Vulnerability Remediation

> Remediate vulnerabilities in accordance with risk assessments.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** vulnerabilities are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Remediation objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.3 [a] (evidence/demo/RA-L2-3-11-3-a.json)

**[b]** vulnerabilities are remediated in accordance with risk assessments

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Vulnerability Remediation objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — RA.L2-3.11.3 [b] (evidence/demo/RA-L2-3-11-3-b.json)


## Security Assessment [CA] Family

### CA.L2-3.12.1: Security Control Assessment

> Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the frequency of security control assessments is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Control Assessment objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.1 [a] (evidence/demo/CA-L2-3-12-1-a.json)

**[b]** security controls are assessed with the defined frequency to determine if the controls are effective in their application

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Control Assessment objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.1 [b] (evidence/demo/CA-L2-3-12-1-b.json)

### CA.L2-3.12.2: operational Plan of Action

> Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** deficiencies and vulnerabilities to be addressed by the plan of action are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: operational Plan of Action objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.2 [a] (evidence/demo/CA-L2-3-12-2-a.json)

**[b]** a plan of action is developed to correct identified deficiencies and reduce or eliminate identified vulnerabilities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: operational Plan of Action objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.2 [b] (evidence/demo/CA-L2-3-12-2-b.json)

**[c]** the plan of action is implemented to correct identified deficiencies and reduce or eliminate identified vulnerabilities

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: operational Plan of Action objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.2 [c] (evidence/demo/CA-L2-3-12-2-c.json)

### CA.L2-3.12.3: Security Control Monitoring

> Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** security controls are monitored on an ongoing basis to ensure the continued effectiveness of those controls

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Control Monitoring objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.3 [a] (evidence/demo/CA-L2-3-12-3-a.json)

### CA.L2-3.12.4: System Security Plan

> Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a system security plan is developed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: System Security Plan maintained at Rev 2; generated from program-data.yaml.
- Evidence: SSP Rev 2 (generated) (outputs/ssp.md)

**[b]** the system boundary is described and documented in the system security plan

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [b] (evidence/demo/CA-L2-3-12-4-b.json)

**[c]** the system environment of operation is described and documented in the system security plan

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [c] (evidence/demo/CA-L2-3-12-4-c.json)

**[d]** the security requirements identified and approved by the designated authority as non-applicable are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [d] (evidence/demo/CA-L2-3-12-4-d.json)

**[e]** the method of security requirement implementation is described and documented in the system security plan

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [e] (evidence/demo/CA-L2-3-12-4-e.json)

**[f]** the relationship with or connection to other systems is described and documented in the system security plan

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [f] (evidence/demo/CA-L2-3-12-4-f.json)

**[g]** the frequency to update the system security plan is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective g satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [g] (evidence/demo/CA-L2-3-12-4-g.json)

**[h]** system security plan is updated with the defined frequency

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System Security Plan objective h satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — CA.L2-3.12.4 [h] (evidence/demo/CA-L2-3-12-4-h.json)


## System and Communications Protection [SC] Family

### SC.L2-3.13.1: Boundary Protection

> Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the external system boundary is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [a] (evidence/demo/SC-L2-3-13-1-a.json)
- Evidence: Bucket ACL or policy exposes object reads to the internet. (terraform/storage.tf:12)
- Evidence: Bucket policy allows public read access. (terraform/storage.tf:12)

**[b]** key internal system boundaries are defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [b] (evidence/demo/SC-L2-3-13-1-b.json)

**[c]** communications are monitored at the external system boundary

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [c] (evidence/demo/SC-L2-3-13-1-c.json)

**[d]** communications are monitored at key internal boundaries

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [d] (evidence/demo/SC-L2-3-13-1-d.json)

**[e]** communications are controlled at the external system boundary

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [e] (evidence/demo/SC-L2-3-13-1-e.json)

**[f]** communications are controlled at key internal boundaries

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [f] (evidence/demo/SC-L2-3-13-1-f.json)

**[g]** communications are protected at the external system boundary

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective g satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [g] (evidence/demo/SC-L2-3-13-1-g.json)

**[h]** communications are protected at key internal boundaries

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Boundary Protection objective h satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.1 [h] (evidence/demo/SC-L2-3-13-1-h.json)

**Remediation plan:** Block public ACLs and restrict bucket policy to the enclave VPC endpoints. Source: ControlBot checkov Merge-blocking in IaC pipeline.

### SC.L2-3.13.2: Security Engineering

> Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** architectural designs that promote effective information security are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [a] (evidence/demo/SC-L2-3-13-2-a.json)

**[b]** software development techniques that promote effective information security are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [b] (evidence/demo/SC-L2-3-13-2-b.json)

**[c]** systems engineering principles that promote effective information security are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [c] (evidence/demo/SC-L2-3-13-2-c.json)

**[d]** identified architectural designs that promote effective information security are employed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [d] (evidence/demo/SC-L2-3-13-2-d.json)

**[e]** identified software development techniques that promote effective information security are employed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [e] (evidence/demo/SC-L2-3-13-2-e.json)

**[f]** identified systems engineering principles that promote effective information security are employed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Engineering objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.2 [f] (evidence/demo/SC-L2-3-13-2-f.json)

### SC.L2-3.13.3: Role Separation

> Separate user functionality from system management functionality.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** user functionality is identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role Separation objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.3 [a] (evidence/demo/SC-L2-3-13-3-a.json)

**[b]** system management functionality is identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role Separation objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.3 [b] (evidence/demo/SC-L2-3-13-3-b.json)

**[c]** user functionality is separated from system management functionality

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Role Separation objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.3 [c] (evidence/demo/SC-L2-3-13-3-c.json)

### SC.L2-3.13.4: Shared Resource Control

> Prevent unauthorized and unintended information transfer via shared system resources.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** unauthorized and unintended information transfer via shared system resources is prevented

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Shared Resource Control objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.4 [a] (evidence/demo/SC-L2-3-13-4-a.json)

### SC.L2-3.13.5: Public-Access System Separation

> Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** publicly accessible system components are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Public-Access System Separation objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.5 [a] (evidence/demo/SC-L2-3-13-5-a.json)
- Evidence: Bucket ACL or policy exposes object reads to the internet. (terraform/storage.tf:12)
- Evidence: Bucket policy allows public read access. (terraform/storage.tf:12)

**[b]** subnetworks for publicly accessible system components are physically or logically separated from internal networks

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Public-Access System Separation objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.5 [b] (evidence/demo/SC-L2-3-13-5-b.json)

### SC.L2-3.13.6: Network Communication by Exception

> Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** network communications traffic is denied by default

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Network Communication by Exception objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.6 [a] (evidence/demo/SC-L2-3-13-6-a.json)

**[b]** network communications traffic is allowed by exception

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Network Communication by Exception objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.6 [b] (evidence/demo/SC-L2-3-13-6-b.json)

### SC.L2-3.13.7: Split Tunneling

> Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling).

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** remote devices are prevented from simultaneously establishing non-remote connections with the system and communicating via some other connection to resources in external networks (i.e., split tunneling)

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Split Tunneling objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.7 [a] (evidence/demo/SC-L2-3-13-7-a.json)

### SC.L2-3.13.8: Data in Transit

> Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** cryptographic mechanisms intended to prevent unauthorized disclosure of CUI are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Data in Transit objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.8 [a] (evidence/demo/SC-L2-3-13-8-a.json)

**[b]** alternative physical safeguards intended to prevent unauthorized disclosure of CUI are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Data in Transit objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.8 [b] (evidence/demo/SC-L2-3-13-8-b.json)

**[c]** either cryptographic mechanisms or alternative physical safeguards are implemented to prevent unauthorized disclosure of CUI during transmission

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Data in Transit objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.8 [c] (evidence/demo/SC-L2-3-13-8-c.json)

### SC.L2-3.13.9: Connections Termination

> Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** a period of inactivity to terminate network connections associated with communications sessions is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Connections Termination objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.9 [a] (evidence/demo/SC-L2-3-13-9-a.json)

**[b]** network connections associated with communications sessions are terminated at the end of the sessions

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Connections Termination objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.9 [b] (evidence/demo/SC-L2-3-13-9-b.json)

**[c]** network connections associated with communications sessions are terminated after the defined period of inactivity

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Connections Termination objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.9 [c] (evidence/demo/SC-L2-3-13-9-c.json)

### SC.L2-3.13.10: Key Management

> Establish and manage cryptographic keys for cryptography employed in organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** cryptographic keys are established whenever cryptography is employed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Key Management objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.10 [a] (evidence/demo/SC-L2-3-13-10-a.json)

**[b]** cryptographic keys are managed whenever cryptography is employed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Key Management objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.10 [b] (evidence/demo/SC-L2-3-13-10-b.json)

### SC.L2-3.13.11: CUI Encryption

> Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** FIPS-validated cryptography is employed to protect the confidentiality of CUI

- AO CONFORMITY: MET (SHARED)
- Assessment Objective Conformity Statement: FIPS-validated cryptography is employed for CUI at rest and in transit. Service-side cryptography is inherited from the GCC High boundary per the Microsoft CRM; customer-side, BitLocker runs in FIPS mode (CMVP certificate 4536) enforced by Intune policy EDS-FIPS-01.
- Inheritance: Shared from Microsoft Microsoft 365 GCC High; CRM ref: SC-13 rows 3-7; CRM doc: Microsoft 365 GCC High CIS/CRM Appendix J, 2026-03 edition; BoE: vendor-boe/microsoft/2026-03/; Customer share: Customer enforces FIPS mode on endpoints and manages Intune policy
- Evidence: Intune EDS-FIPS-01 policy export (evidence/sc/3.13.11/intune-fips-policy.json)

### SC.L2-3.13.12: Collaborative Device Control

> Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** collaborative computing devices are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Collaborative Device Control objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.12 [a] (evidence/demo/SC-L2-3-13-12-a.json)

**[b]** collaborative computing devices provide indication to users of devices in use

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Collaborative Device Control objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.12 [b] (evidence/demo/SC-L2-3-13-12-b.json)

**[c]** remote activation of collaborative computing devices is prohibited

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Collaborative Device Control objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.12 [c] (evidence/demo/SC-L2-3-13-12-c.json)

### SC.L2-3.13.13: Mobile Code

> Control and monitor the use of mobile code.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** use of mobile code is controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Mobile Code objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.13 [a] (evidence/demo/SC-L2-3-13-13-a.json)

**[b]** use of mobile code is monitored

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Mobile Code objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.13 [b] (evidence/demo/SC-L2-3-13-13-b.json)

### SC.L2-3.13.14: Voice over Internet Protocol

> Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** use of Voice over Internet Protocol (VoIP) technologies is controlled

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Voice over Internet Protocol objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.14 [a] (evidence/demo/SC-L2-3-13-14-a.json)

**[b]** use of Voice over Internet Protocol (VoIP) technologies is monitored

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Voice over Internet Protocol objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.14 [b] (evidence/demo/SC-L2-3-13-14-b.json)

### SC.L2-3.13.15: Communications Authenticity

> Protect the authenticity of communications sessions.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the authenticity of communications sessions is protected

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Communications Authenticity objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.15 [a] (evidence/demo/SC-L2-3-13-15-a.json)

### SC.L2-3.13.16: Data at Rest

> Protect the confidentiality of CUI at rest.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the confidentiality of CUI at rest is protected

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Data at Rest objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SC.L2-3.13.16 [a] (evidence/demo/SC-L2-3-13-16-a.json)


## System and Information Integrity [SI] Family

### SI.L2-3.14.1: Flaw Remediation

> Identify, report, and correct system flaws in a timely manner.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the time within which to identify system flaws is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [a] (evidence/demo/SI-L2-3-14-1-a.json)

**[b]** system flaws are identified within the specified time frame

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [b] (evidence/demo/SI-L2-3-14-1-b.json)

**[c]** the time within which to report system flaws is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [c] (evidence/demo/SI-L2-3-14-1-c.json)

**[d]** system flaws are reported within the specified time frame

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective d satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [d] (evidence/demo/SI-L2-3-14-1-d.json)

**[e]** the time within which to correct system flaws is specified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective e satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [e] (evidence/demo/SI-L2-3-14-1-e.json)

**[f]** system flaws are corrected within the specified time frame

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Flaw Remediation objective f satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.1 [f] (evidence/demo/SI-L2-3-14-1-f.json)

### SI.L2-3.14.2: Malicious Code Protection

> Provide protection from malicious code at designated locations within organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** designated locations for malicious code protection are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Malicious Code Protection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.2 [a] (evidence/demo/SI-L2-3-14-2-a.json)

**[b]** protection from malicious code at designated locations is provided

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Malicious Code Protection objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.2 [b] (evidence/demo/SI-L2-3-14-2-b.json)

### SI.L2-3.14.3: Security Alerts & Advisories

> Monitor system security alerts and advisories and take action in response.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** response actions to system security alerts and advisories are identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Alerts & Advisories objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.3 [a] (evidence/demo/SI-L2-3-14-3-a.json)

**[b]** system security alerts and advisories are monitored

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Alerts & Advisories objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.3 [b] (evidence/demo/SI-L2-3-14-3-b.json)

**[c]** actions in response to system security alerts and advisories are taken

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Security Alerts & Advisories objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.3 [c] (evidence/demo/SI-L2-3-14-3-c.json)

### SI.L2-3.14.4: Update Malicious Code Protection

> Update malicious code protection mechanisms when new releases are available.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** malicious code protection mechanisms are updated when new releases are available

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Update Malicious Code Protection objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.4 [a] (evidence/demo/SI-L2-3-14-4-a.json)

### SI.L2-3.14.5: System & File Scanning

> Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the frequency for malicious code scans is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System & File Scanning objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.5 [a] (evidence/demo/SI-L2-3-14-5-a.json)

**[b]** malicious code scans are performed with the defined frequency

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System & File Scanning objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.5 [b] (evidence/demo/SI-L2-3-14-5-b.json)

**[c]** real-time malicious code scans of files from external sources as files are downloaded, opened, or executed are performed

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: System & File Scanning objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.5 [c] (evidence/demo/SI-L2-3-14-5-c.json)

### SI.L2-3.14.6: Monitor Communications for Attacks

> Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** the system is monitored to detect attacks and indicators of potential attacks

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Monitor Communications for Attacks objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.6 [a] (evidence/demo/SI-L2-3-14-6-a.json)

**[b]** inbound communications traffic is monitored to detect attacks and indicators of potential attacks

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Monitor Communications for Attacks objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.6 [b] (evidence/demo/SI-L2-3-14-6-b.json)

**[c]** outbound communications traffic is monitored to detect attacks and indicators of potential attacks

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Monitor Communications for Attacks objective c satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.6 [c] (evidence/demo/SI-L2-3-14-6-c.json)

### SI.L2-3.14.7: Identify Unauthorized Use

> Identify unauthorized use of organizational systems.

**REQUIREMENT CONFORMITY:** MET

**ASSESSMENT OBJECTIVE(S):**

**[a]** authorized use of the system is defined

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identify Unauthorized Use objective a satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.7 [a] (evidence/demo/SI-L2-3-14-7-a.json)

**[b]** unauthorized use of the system is identified

- AO CONFORMITY: MET
- Assessment Objective Conformity Statement: Demo OSC: Identify Unauthorized Use objective b satisfied via documented enclave controls (Atlas Precision Manufacturing).
- Evidence: Demo evidence — SI.L2-3.14.7 [b] (evidence/demo/SI-L2-3-14-7-b.json)


## Plans of Action & Milestones [POA&M]

| Priority | POA&M | Due Date | Actions |
|----------|-------|----------|---------|
| Medium | AC.L2-3.1.22: Close gap on AC.L2-3.1.22 before C3PAO assessment | 2026-09-30 | Document control; Collect assessor evidence; Update conformity |
| High | AU.L2-3.3.5: Implement Sentinel analytics rules and weekly correlated review for enclave audit records | 2026-09-15 | Deploy Microsoft Sentinel analytics rules for the enclave workspace; Stand up weekly audit review runbook with sign-off log; Backfill 90 days of review evidence before assessment |
| Medium | CM.L2-3.4.7: Close gap on CM.L2-3.4.7 before C3PAO assessment | 2026-09-30 | Document control; Collect assessor evidence; Update conformity |
| Medium | MP.L2-3.8.1: Install locked shred console for overnight mail-room accumulation | 2026-08-15 | Procure lockable console; Update mail-room procedure; Photo evidence for assessor |
| High | SC.L2-3.13.1: S3 bucket ACL allows public access [controlbot:checkov-ckv-aws-019-terraform-aws-s3-bucket-public-acl] | 2026-08-03 | Block public ACLs and restrict bucket policy to the enclave VPC endpoints. |

## NIST CMVP Certificates

| Certificate # | Vendor | Module Name | Standard | Status | Sunset Date | Associated Security Policy |
|---------------|--------|-------------|----------|--------|-------------|----------------------------|
| 4536 | Microsoft | Windows Cryptographic Primitives Library | FIPS 140-3 | Active | 2030-03-01 | https://csrc.nist.gov/projects/cryptographic-module-validation-program |

Verify each certificate at the NIST CMVP registry before the assessment.
