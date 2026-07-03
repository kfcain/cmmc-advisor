# System and Communications Protection (SC) Assessment Objectives

> Source: NIST SP 800-171A (June 2018) assessment procedures;
> CMMC Assessment Guide Level 2 v2.13; DoD Assessment Methodology
> v1.2.1 (SPRS point values); 32 CFR 170.24

## How to Use This File

NIST SP 800-171A breaks each security requirement into assessment
objectives: determination statements an assessor must be able to answer
yes to. A requirement is MET only when **every** applicable objective is
satisfied; one failed objective fails the whole requirement
(32 CFR 170.24). The 110 Level 2 requirements decompose into 320
objectives, and assessments are conducted at the objective level.

For each requirement below: the SPRS value is the point deduction if the
requirement is NOT MET under the DoD Assessment Methodology (110 minus
deductions; minimum score is -203). The assessment methods are drawn from
the CMMC Assessment Guide Level 2: **examine** (review artifacts),
**interview** (talk to the people responsible), and **test** (exercise the
mechanism and compare actual to expected behavior). Examine lists below
show representative objects; the assessment guide carries the full lists.

Definitions that matter at the objective level (32 CFR 170.4 and the
Assessment Guide glossary): *periodically* means an organization-defined
interval not exceeding one year. An *operational plan of action*
(CA.L2-3.12.2) is a different artifact from an assessment POA&M. An
*Enduring Exception* (infeasible remediation, documented in the SSP) and a
*temporary deficiency* (known fix in progress, documented in the
operational plan of action) are the two sanctioned ways to carry a known
gap without failing honesty.

Implementation guidance for these requirements lives in
`../domains/sc-system-comms.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## SC.L2-3.13.1: Boundary Protection

**SPRS value:** 5 points. **Level 1 counterpart:** SC.L1-b.1.x (FAR 52.204-21).

**Requirement:** Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.1[a] | the external system boundary is defined |
| 3.13.1[b] | key internal system boundaries are defined |
| 3.13.1[c] | communications are monitored at the external system boundary |
| 3.13.1[d] | communications are monitored at key internal boundaries |
| 3.13.1[e] | communications are controlled at the external system boundary |
| 3.13.1[f] | communications are controlled at key internal boundaries |
| 3.13.1[g] | communications are protected at the external system boundary |
| 3.13.1[h] | communications are protected at key internal boundaries |

**Examine:** System and communications protection policy; Procedures addressing boundary protection; System security plan; List of key internal boundaries of the system; System design documentation; Boundary protection hardware and software (plus 4 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers; Personnel with boundary protection responsibilities.

**Test:** Mechanisms implementing boundary protection capability.


## SC.L2-3.13.2: Security Engineering

**SPRS value:** 5 points.

**Requirement:** Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.2[a] | architectural designs that promote effective information security are identified |
| 3.13.2[b] | software development techniques that promote effective information security are identified |
| 3.13.2[c] | systems engineering principles that promote effective information security are identified |
| 3.13.2[d] | identified architectural designs that promote effective information security are employed |
| 3.13.2[e] | identified software development techniques that promote effective information security are employed |
| 3.13.2[f] | identified systems engineering principles that promote effective information security are employed |

**Examine:** Security planning policy; Procedures addressing system security plan development and implementation; Procedures addressing system security plan reviews and updates; Enterprise architecture documentation; System security plan; Records of system security plan reviews and updates (plus 7 more object types in the assessment guide).

**Interview:** Personnel with responsibility for determining information system security requirements; Personnel with information system design, development, implementation, and modification responsibilities; Personnel with security planning and system security plan implementation responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for system security plan development, review, update, and approval; Mechanisms supporting the system security plan; Processes for applying security engineering principles in system specification, design, development, implementation, and modification; Automated mechanisms supporting the application of security engineering principles in information system specification, design, development, implementation, and modification.


## SC.L2-3.13.3: Role Separation

**SPRS value:** 1 points.

**Requirement:** Separate user functionality from system management functionality.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.3[a] | user functionality is identified |
| 3.13.3[b] | system management functionality is identified |
| 3.13.3[c] | user functionality is separated from system management functionality |

**Examine:** System and communications protection policy; Procedures addressing application partitioning; System design documentation; System configuration settings and associated documentation; System security plan; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer.

**Test:** Separation of user functionality from system management functionality.


## SC.L2-3.13.4: Shared Resource Control

**SPRS value:** 1 points.

**Requirement:** Prevent unauthorized and unintended information transfer via shared system resources.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.4[a] | unauthorized and unintended information transfer via shared system resources is prevented |

**Examine:** System and communications protection policy; Procedures addressing application partitioning; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer.

**Test:** Separation of user functionality from system management functionality.


## SC.L2-3.13.5: Public-Access System Separation

**SPRS value:** 5 points. **Level 1 counterpart:** SC.L1-b.1.xi (FAR 52.204-21).

**Requirement:** Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.5[a] | publicly accessible system components are identified |
| 3.13.5[b] | subnetworks for publicly accessible system components are physically or logically separated from internal networks |

**Examine:** System and communications protection policy; Procedures addressing boundary protection; System security plan; List of key internal boundaries of the system; System design documentation; Boundary protection hardware and software (plus 4 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers; Personnel with boundary protection responsibilities.

**Test:** Mechanisms implementing boundary protection capability.


## SC.L2-3.13.6: Network Communication by Exception

**SPRS value:** 5 points.

**Requirement:** Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.6[a] | network communications traffic is denied by default |
| 3.13.6[b] | network communications traffic is allowed by exception |

**Examine:** System and communications protection policy; Procedures addressing boundary protection; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer; Personnel with boundary protection responsibilities.

**Test:** Mechanisms implementing traffic management at managed interfaces.


## SC.L2-3.13.7: Split Tunneling

**SPRS value:** 1 points.

**Requirement:** Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling).

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.7[a] | remote devices are prevented from simultaneously establishing non-remote connections with the system and communicating via some other connection to resources in external networks (i.e., split tunneling) |

**Examine:** System and communications protection policy; Procedures addressing boundary protection; System security plan; System design documentation; System hardware and software; System architecture (plus 3 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer; Personnel with boundary protection responsibilities.

**Test:** Mechanisms implementing boundary protection capability; Mechanisms supporting or restricting non-remote connections.


## SC.L2-3.13.8: Data in Transit

**SPRS value:** 3 points.

**Requirement:** Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.8[a] | cryptographic mechanisms intended to prevent unauthorized disclosure of CUI are identified |
| 3.13.8[b] | alternative physical safeguards intended to prevent unauthorized disclosure of CUI are identified |
| 3.13.8[c] | either cryptographic mechanisms or alternative physical safeguards are implemented to prevent unauthorized disclosure of CUI during transmission |

**Examine:** System and communications protection policy; Procedures addressing transmission confidentiality and integrity; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer.

**Test:** Cryptographic mechanisms or mechanisms supporting or implementing transmission confidentiality; Organizational processes for defining and implementing alternative physical safeguards.


## SC.L2-3.13.9: Connections Termination

**SPRS value:** 1 points.

**Requirement:** Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.9[a] | a period of inactivity to terminate network connections associated with communications sessions is defined |
| 3.13.9[b] | network connections associated with communications sessions are terminated at the end of the sessions |
| 3.13.9[c] | network connections associated with communications sessions are terminated after the defined period of inactivity |

**Examine:** System and communications protection policy; Procedures addressing network disconnect; System design documentation; System security plan; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer.

**Test:** Mechanisms supporting or implementing network disconnect capability.


## SC.L2-3.13.10: Key Management

**SPRS value:** 1 points.

**Requirement:** Establish and manage cryptographic keys for cryptography employed in organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.10[a] | cryptographic keys are established whenever cryptography is employed |
| 3.13.10[b] | cryptographic keys are managed whenever cryptography is employed |

**Examine:** System and communications protection policy; Procedures addressing cryptographic key establishment and management; System security plan; System design documentation; Cryptographic mechanisms; System configuration settings and associated documentation (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel with responsibilities for cryptographic key establishment and management.

**Test:** Mechanisms supporting or implementing cryptographic key establishment and management.


## SC.L2-3.13.11: CUI Encryption

**SPRS value:** 5 points (3-point deduction if partially implemented per the methodology).

**Requirement:** Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.11[a] | FIPS-validated cryptography is employed to protect the confidentiality of CUI |

**Examine:** System and communications protection policy; Procedures addressing cryptographic protection; System security plan; System design documentation; System configuration settings and associated documentation; Cryptographic module validation certificates (plus 3 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers; Personnel with responsibilities for cryptographic protection.

**Test:** Mechanisms supporting or implementing cryptographic protection.


## SC.L2-3.13.12: Collaborative Device Control

**SPRS value:** 1 points.

**Requirement:** Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.12[a] | collaborative computing devices are identified |
| 3.13.12[b] | collaborative computing devices provide indication to users of devices in use |
| 3.13.12[c] | remote activation of collaborative computing devices is prohibited |

**Examine:** System and communications protection policy; Procedures addressing collaborative computing; Access control policy and procedures; System security plan; System design documentation; System audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer; Personnel with responsibilities for managing collaborative computing devices.

**Test:** Mechanisms supporting or implementing management of remote activation of collaborative computing devices; Mechanisms providing an indication of use of collaborative computing devices.


## SC.L2-3.13.13: Mobile Code

**SPRS value:** 1 points.

**Requirement:** Control and monitor the use of mobile code.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.13[a] | use of mobile code is controlled |
| 3.13.13[b] | use of mobile code is monitored |

**Examine:** System and communications protection policy; Procedures addressing mobile code; Mobile code usage restrictions, mobile code implementation policy and procedures; System audit logs and records; System security plan; List of acceptable mobile code and mobile code technologies (plus 5 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel with responsibilities for managing mobile code.

**Test:** Organizational process for controlling, authorizing, monitoring, and restricting mobile code; Mechanisms supporting or implementing the management of mobile code; Mechanisms supporting or implementing the monitoring of mobile code.


## SC.L2-3.13.14: Voice over Internet Protocol

**SPRS value:** 1 points.

**Requirement:** Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.14[a] | use of Voice over Internet Protocol (VoIP) technologies is controlled |
| 3.13.14[b] | use of Voice over Internet Protocol (VoIP) technologies is monitored |

**Examine:** System and communications protection policy; Procedures addressing VoIP; VoIP usage restrictions; VoIP implementation guidance; System security plan; System design documentation (plus 4 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel with responsibilities for managing VoIP.

**Test:** Organizational process for authorizing, monitoring, and controlling VoIP; Mechanisms supporting or implementing authorizing, monitoring, and controlling VoIP.


## SC.L2-3.13.15: Communications Authenticity

**SPRS value:** 5 points.

**Requirement:** Protect the authenticity of communications sessions.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.15[a] | the authenticity of communications sessions is protected |

**Examine:** System and communications protection policy; Procedures addressing session authenticity; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities.

**Test:** Mechanisms supporting or implementing session authenticity.


## SC.L2-3.13.16: Data at Rest

**SPRS value:** 1 points.

**Requirement:** Protect the confidentiality of CUI at rest.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.13.16[a] | the confidentiality of CUI at rest is protected |

**Examine:** System and communications protection policy; Procedures addressing protection of information at rest; System security plan; System design documentation; List of information at rest requiring confidentiality protections; System configuration settings and associated documentation (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developer.

**Test:** Mechanisms supporting or implementing confidentiality protections for information at rest.

---

## Where SC Assessments Go Wrong

- Boundary protection (3.13.1) evidence limited to a firewall existing; objectives want monitored, controlled communications at external and key internal boundaries, which requires showing rules, monitoring, and architecture.
- FIPS-validated cryptography (3.13.11) claimed without CMVP certificate numbers mapped to the modules actually in use (anti-pattern 7); validate against the NIST CMVP registry, and note this is one of the two partial-credit SPRS items.
- Split tunneling (3.13.7) enabled on the VPN with no preventing configuration, contradicting the SSP narrative.
- Data at rest (3.13.16) covered on laptops but not on file servers, NAS devices, or SaaS exports where CUI actually sits.
- Key management (3.13.10) undocumented: nobody can explain where keys live, who can access them, or how they rotate.
