# NIST SP 800-171 Rev 2 to Rev 3 Crosswalk

> Source: NIST SP 800-171 Rev 3 dataset (NIST CPRT export, including
> withdrawal dispositions from NIST's Rev 2 to Rev 3 change analysis);
> NIST SP 800-171 Rev 2. Counts verified 2026-07-03: 110 Rev 2
> requirements = 77 carried forward + 33 withdrawn; Rev 3 totals 97
> requirements including 20 new ones.

## Overview

CMMC assesses against Rev 2 today; see `rev3-transition.md` for the
strategy and timeline. This file is the requirement-by-requirement map
for planning low-regret work and reading Rev 3 documentation without
getting lost. Rev 3 keeps the Rev 2 numbering scheme (03.xx.yy), so a
Rev 2 requirement either continues under its own number, or was
withdrawn with its content incorporated into or addressed by another
requirement. Rev 3 also introduces Organization-Defined Parameters
(ODPs); where DoD adopts Rev 3 for CMMC, expect DoD-assigned ODP values
the way 32 CFR 170.14 already assigns them for Level 3.

Headline numbers: 110 Rev 2 requirements become 97 in Rev 3. 77 carry
forward under the same number (many with substantive edits and new
ODPs), 33 are withdrawn into other requirements, and 20 are new,
including three new families: Planning (03.15), System and Services
Acquisition (03.16), and Supply Chain Risk Management (03.17).

## Disposition of Every Rev 2 Requirement

### Access Control (3.01)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| AC.L2-3.1.1: Authorized Access Control | Carried forward as 3.1.1 (Account Management) | 6 |
| AC.L2-3.1.2: Transaction & Function Control | Carried forward as 3.1.2 (Access Enforcement) | 0 |
| AC.L2-3.1.3: Control CUI Flow | Carried forward as 3.1.3 (Information Flow Enforcement) | 0 |
| AC.L2-3.1.4: Separation of Duties | Carried forward as 3.1.4 (Separation of Duties) | 0 |
| AC.L2-3.1.5: Least Privilege | Carried forward as 3.1.5 (Least Privilege) | 3 |
| AC.L2-3.1.6: Non-Privileged Account Use | Carried forward as 3.1.6 (Least Privilege – Privileged Accounts) | 1 |
| AC.L2-3.1.7: Privileged Functions | Carried forward as 3.1.7 (Least Privilege – Privileged Functions) | 0 |
| AC.L2-3.1.8: Unsuccessful Logon Attempts | Carried forward as 3.1.8 (Unsuccessful Logon Attempts) | 4 |
| AC.L2-3.1.9: Privacy & Security Notices | Carried forward as 3.1.9 (System Use Notification) | 0 |
| AC.L2-3.1.10: Session Lock | Carried forward as 3.1.10 (Device Lock) | 2 |
| AC.L2-3.1.11: Session Termination | Carried forward as 3.1.11 (Session Termination) | 1 |
| AC.L2-3.1.12: Control Remote Access | Carried forward as 3.1.12 (Remote Access) | 0 |
| AC.L2-3.1.13: Remote Access Confidentiality | Withdrawn: addressed by 3.13.8 (Transmission and Storage Confidentiality) |  |
| AC.L2-3.1.14: Remote Access Routing | Withdrawn: incorporated into 3.1.12 (Remote Access) |  |
| AC.L2-3.1.15: Privileged Remote Access | Withdrawn: incorporated into 3.1.12 (Remote Access) |  |
| AC.L2-3.1.16: Wireless Access Authorization | Carried forward as 3.1.16 (Wireless Access) | 0 |
| AC.L2-3.1.17: Wireless Access Protection | Withdrawn: incorporated into 3.1.16 (Wireless Access) |  |
| AC.L2-3.1.18: Mobile Device Connection | Carried forward as 3.1.18 (Access Control for Mobile Devices) | 0 |
| AC.L2-3.1.19: Encrypt CUI on Mobile | Withdrawn: incorporated into 3.1.18 (Access Control for Mobile Devices) |  |
| AC.L2-3.1.20: External Connections | Carried forward as 3.1.20 (Use of External Systems) | 1 |
| AC.L2-3.1.21: Portable Storage Use | Withdrawn: incorporated into 3.1.20 (Use of External Systems) |  |
| AC.L2-3.1.22: Control Public Information | Carried forward as 3.1.22 (Publicly Accessible Content) | 0 |

### Awareness and Training (3.02)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| AT.L2-3.2.1: Role-Based Risk Awareness | Carried forward as 3.2.1 (Literacy Training and Awareness) | 4 |
| AT.L2-3.2.2: Role-Based Training | Carried forward as 3.2.2 (Role-Based Training) | 4 |
| AT.L2-3.2.3: Insider Threat Awareness | Withdrawn: incorporated into 3.2.1 (Literacy Training and Awareness) |  |

### Audit and Accountability (3.03)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| AU.L2-3.3.1: System Auditing | Carried forward as 3.3.1 (Event Logging) | 2 |
| AU.L2-3.3.2: User Accountability | Carried forward as 3.3.2 (Audit Record Content) | 0 |
| AU.L2-3.3.3: Event Review | Carried forward as 3.3.3 (Audit Record Generation) | 0 |
| AU.L2-3.3.4: Audit Failure Alerting | Carried forward as 3.3.4 (Response to Audit Logging Process Failures) | 2 |
| AU.L2-3.3.5: Audit Correlation | Carried forward as 3.3.5 (Audit Record Review, Analysis, and Reporting) | 1 |
| AU.L2-3.3.6: Reduction & Reporting | Carried forward as 3.3.6 (Audit Record Reduction and Report Generation) | 0 |
| AU.L2-3.3.7: Authoritative Time Source | Carried forward as 3.3.7 (Time Stamps) | 1 |
| AU.L2-3.3.8: Audit Protection | Carried forward as 3.3.8 (Protection of Audit Information) | 0 |
| AU.L2-3.3.9: Audit Management | Withdrawn: incorporated into 3.3.8 (Protection of Audit Information) |  |

### Configuration Management (3.04)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| CM.L2-3.4.1: System Baselining | Carried forward as 3.4.1 (Baseline Configuration) | 1 |
| CM.L2-3.4.2: Security Configuration Enforcement | Carried forward as 3.4.2 (Configuration Settings) | 1 |
| CM.L2-3.4.3: System Change Management | Carried forward as 3.4.3 (Configuration Change Control) | 0 |
| CM.L2-3.4.4: Security Impact Analysis | Carried forward as 3.4.4 (Impact Analyses) | 0 |
| CM.L2-3.4.5: Access Restrictions for Change | Carried forward as 3.4.5 (Access Restrictions for Change) | 0 |
| CM.L2-3.4.6: Least Functionality | Carried forward as 3.4.6 (Least Functionality) | 6 |
| CM.L2-3.4.7: Nonessential Functionality | Withdrawn: incorporated into 3.4.6 (Least Functionality) |  |
| CM.L2-3.4.8: Application Execution Policy | Carried forward as 3.4.8 (Authorized Software – Allow by Exception) | 1 |
| CM.L2-3.4.9: User-Installed Software | Withdrawn: addressed by 3.1.5 (Least Privilege) |  |

### Identification and Authentication (3.05)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| IA.L2-3.5.1: Identification | Carried forward as 3.5.1 (User Identification and Authentication) | 1 |
| IA.L2-3.5.2: Authentication | Carried forward as 3.5.2 (Device Identification and Authentication) | 1 |
| IA.L2-3.5.3: Multifactor Authentication | Carried forward as 3.5.3 (Multi-Factor Authentication) | 0 |
| IA.L2-3.5.4: Replay-Resistant Authentication | Carried forward as 3.5.4 (Replay-Resistant Authentication) | 0 |
| IA.L2-3.5.5: Identifier Reuse | Carried forward as 3.5.5 (Identifier Management) | 2 |
| IA.L2-3.5.6: Identifier Handling | Withdrawn: Consistency with SP 800-53 |  |
| IA.L2-3.5.7: Password Complexity | Carried forward as 3.5.7 (Password Management) | 2 |
| IA.L2-3.5.8: Password Reuse | Withdrawn: Consistency with SP 800-53 |  |
| IA.L2-3.5.9: Temporary Passwords | Withdrawn: Consistency with SP 800-53 |  |
| IA.L2-3.5.10: Cryptographically-Protected Passwords | Withdrawn: incorporated into 3.5.7 (Password Management) |  |
| IA.L2-3.5.11: Obscure Feedback | Carried forward as 3.5.11 (Authentication Feedback) | 0 |

### Incident Response (3.06)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| IR.L2-3.6.1: Incident Handling | Carried forward as 3.6.1 (Incident Handling) | 0 |
| IR.L2-3.6.2: Incident Reporting | Carried forward as 3.6.2 (Incident Monitoring, Reporting, and Response Assistance) | 2 |
| IR.L2-3.6.3: Incident Response Testing | Carried forward as 3.6.3 (Incident Response Testing) | 1 |

### Maintenance (3.07)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| MA.L2-3.7.1: Perform Maintenance | Withdrawn: Recategorized as NCO |  |
| MA.L2-3.7.2: System Maintenance Control | Withdrawn: incorporated into 3.7.4 (Maintenance Tools) |  |
| MA.L2-3.7.3: Equipment Sanitization | Withdrawn: incorporated into 3.8.3 (Media Sanitization) |  |
| MA.L2-3.7.4: Media Inspection | Carried forward as 3.7.4 (Maintenance Tools) | 0 |
| MA.L2-3.7.5: Nonlocal Maintenance | Carried forward as 3.7.5 (Nonlocal Maintenance) | 0 |
| MA.L2-3.7.6: Maintenance Personnel | Carried forward as 3.7.6 (Maintenance Personnel) | 0 |

### Media Protection (3.08)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| MP.L2-3.8.1: Media Protection | Carried forward as 3.8.1 (Media Storage) | 0 |
| MP.L2-3.8.2: Media Access | Carried forward as 3.8.2 (Media Access) | 0 |
| MP.L2-3.8.3: Media Disposal | Carried forward as 3.8.3 (Media Sanitization) | 0 |
| MP.L2-3.8.4: Media Markings | Carried forward as 3.8.4 (Media Marking) | 0 |
| MP.L2-3.8.5: Media Accountability | Carried forward as 3.8.5 (Media Transport) | 0 |
| MP.L2-3.8.6: Portable Storage Encryption | Withdrawn: incorporated into 3.13.8 (Transmission and Storage Confidentiality) |  |
| MP.L2-3.8.7: Removeable Media | Carried forward as 3.8.7 (Media Use) | 1 |
| MP.L2-3.8.8: Shared Media | Withdrawn: incorporated into 3.8.7 (Media Use) |  |
| MP.L2-3.8.9: Protect Backups | Carried forward as 3.8.9 (System Backup – Cryptographic Protection) | 0 |

### Personnel Security (3.09)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| PS.L2-3.9.1: Screen Individuals | Carried forward as 3.9.1 (Personnel Screening) | 1 |
| PS.L2-3.9.2: Personnel Actions | Carried forward as 3.9.2 (Personnel Termination and Transfer) | 1 |

### Physical Protection (3.10)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| PE.L2-3.10.1: Limit Physical Access | Carried forward as 3.10.1 (Physical Access Authorizations) | 1 |
| PE.L2-3.10.2: Monitor Facility | Carried forward as 3.10.2 (Monitoring Physical Access) | 2 |
| PE.L2-3.10.3: Escort Visitors | Withdrawn: incorporated into 3.10.7 (Physical Access Control) |  |
| PE.L2-3.10.4: Physical Access Logs | Withdrawn: incorporated into 3.10.7 (Physical Access Control) |  |
| PE.L2-3.10.5: Manage Physical Access | Withdrawn: incorporated into 3.10.7 (Physical Access Control) |  |
| PE.L2-3.10.6: Alternative Work Sites | Carried forward as 3.10.6 (Alternate Work Site) | 1 |

### Risk Assessment (3.11)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| RA.L2-3.11.1: RIsk Assessments | Carried forward as 3.11.1 (Risk Assessment) | 1 |
| RA.L2-3.11.2: Vulnerability Scan | Carried forward as 3.11.2 (Vulnerability Monitoring and Scanning) | 4 |
| RA.L2-3.11.3: Vulnerability Remediation | Withdrawn: incorporated into 3.11.2 (Vulnerability Monitoring and Scanning) |  |

### Security Assessment and Monitoring (3.12)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| CA.L2-3.12.1: Security Control Assessment | Carried forward as 3.12.1 (Security Assessment) | 1 |
| CA.L2-3.12.2: operational Plan of Action | Carried forward as 3.12.2 (Plan of Action and Milestones) | 0 |
| CA.L2-3.12.3: Security Control Monitoring | Carried forward as 3.12.3 (Continuous Monitoring) | 0 |
| CA.L2-3.12.4: System Security Plan | Withdrawn: incorporated into 3.15.2 (System Security Plan) |  |

### System and Communications Protection (3.13)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| SC.L2-3.13.1: Boundary Protection | Carried forward as 3.13.1 (Boundary Protection) | 0 |
| SC.L2-3.13.2: Security Engineering | Withdrawn: Recategorized as NCO |  |
| SC.L2-3.13.3: Role Separation | Withdrawn: addressed by 3.1.1 (Account Management) |  |
| SC.L2-3.13.4: Shared Resource Control | Carried forward as 3.13.4 (Information in Shared System Resources) | 0 |
| SC.L2-3.13.5: Public-Access System Separation | Withdrawn: incorporated into 3.13.1 (Boundary Protection) |  |
| SC.L2-3.13.6: Network Communication by Exception | Carried forward as 3.13.6 (Network Communications – Deny by Default – Allow by Exception) | 0 |
| SC.L2-3.13.7: Split Tunneling | Withdrawn: addressed by 3.1.12 (Remote Access) |  |
| SC.L2-3.13.8: Data in Transit | Carried forward as 3.13.8 (Transmission and Storage Confidentiality) | 0 |
| SC.L2-3.13.9: Connections Termination | Carried forward as 3.13.9 (Network Disconnect) | 1 |
| SC.L2-3.13.10: Key Management | Carried forward as 3.13.10 (Cryptographic Key Establishment and Management) | 1 |
| SC.L2-3.13.11: CUI Encryption | Carried forward as 3.13.11 (Cryptographic Protection) | 1 |
| SC.L2-3.13.12: Collaborative Device Control | Carried forward as 3.13.12 (Collaborative Computing Devices and Applications) | 1 |
| SC.L2-3.13.13: Mobile Code | Carried forward as 3.13.13 (Mobile Code) | 0 |
| SC.L2-3.13.14: Voice over Internet Protocol | Withdrawn: Technology-specific |  |
| SC.L2-3.13.15: Communications Authenticity | Carried forward as 3.13.15 (Session Authenticity) | 0 |
| SC.L2-3.13.16: Data at Rest | Withdrawn: incorporated into 3.13.8 (Transmission and Storage Confidentiality) |  |

### System and Information Integrity (3.14)

| Rev 2 requirement | Rev 3 disposition | Rev 3 ODPs |
|-------------------|-------------------|------------|
| SI.L2-3.14.1: Flaw Remediation | Carried forward as 3.14.1 (Flaw Remediation) | 2 |
| SI.L2-3.14.2: Malicious Code Protection | Carried forward as 3.14.2 (Malicious Code Protection) | 1 |
| SI.L2-3.14.3: Security Alerts & Advisories | Carried forward as 3.14.3 (Security Alerts, Advisories, and Directives) | 0 |
| SI.L2-3.14.4: Update Malicious Code Protection | Withdrawn: incorporated into 3.14.2 (Malicious Code Protection) |  |
| SI.L2-3.14.5: System & File Scanning | Withdrawn: addressed by 3.14.2 (Malicious Code Protection) |  |
| SI.L2-3.14.6: Monitor Communications for Attacks | Carried forward as 3.14.6 (System Monitoring) | 0 |
| SI.L2-3.14.7: Identify Unauthorized Use | Withdrawn: incorporated into 3.14.6 (System Monitoring) |  |

## New in Rev 3 (No Rev 2 Counterpart)

| Rev 3 requirement | Title | Family | ODPs |
|-------------------|-------|--------|------|
| 3.4.10 | System Component Inventory | Configuration Management | 1 |
| 3.4.11 | Information Location | Configuration Management | 0 |
| 3.4.12 | System and Component Configuration for High-Risk Areas | Configuration Management | 2 |
| 3.5.12 | Authenticator Management | Identification and Authentication | 2 |
| 3.6.4 | Incident Response Training | Incident Response | 4 |
| 3.6.5 | Incident Response Plan | Incident Response | 0 |
| 3.10.7 | Physical Access Control | Physical Protection | 0 |
| 3.10.8 | Access Control for Transmission | Physical Protection | 0 |
| 3.11.4 | Risk Response | Risk Assessment | 0 |
| 3.12.5 | Information Exchange | Security Assessment and Monitoring | 2 |
| 3.14.8 | Information Management and Retention | System and Information Integrity | 0 |
| 3.15.1 | Policy and Procedures | Planning | 1 |
| 3.15.2 | System Security Plan | Planning | 1 |
| 3.15.3 | Rules of Behavior | Planning | 1 |
| 3.16.1 | Security Engineering Principles | System and Services Acquisition | 1 |
| 3.16.2 | Unsupported System Components | System and Services Acquisition | 0 |
| 3.16.3 | External System Services | System and Services Acquisition | 1 |
| 3.17.1 | Supply Chain Risk Management Plan | Supply Chain Risk Management | 1 |
| 3.17.2 | Acquisition Strategies, Tools, and Methods | Supply Chain Risk Management | 0 |
| 3.17.3 | Supply Chain Requirements and Processes | Supply Chain Risk Management | 1 |

The three new families formalize work Rev 2 handled implicitly or not
at all: Planning (system security plan and rules of behavior move here),
System and Services Acquisition (external system services, unsupported
components), and Supply Chain Risk Management (plan, acquisition
strategies, and controls; this is the Rev 3 cousin of the Level 3
supply chain requirements in `level-3-expert.md`).

## How to Use This for Planning

1. Keep implementing Rev 2; it is the assessed baseline (see
   `rev3-transition.md`).
2. When you touch a carried-forward requirement, skim its Rev 3 text
   and ODPs: choices that satisfy both revisions are free insurance.
3. The withdrawn list is consolidation, not deletion; capability you
   built for a withdrawn requirement lives on in its destination.
4. The 20 new requirements, especially the SCRM family, are the real
   transition delta. `grc/vendor-and-supply-chain.md` and
   `grc/risk-management.md` already position you for them.
