# Configuration Management (CM) Assessment Objectives

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
`../domains/cm-configuration-mgmt.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## CM.L2-3.4.1: System Baselining

**SPRS value:** 5 points.

**Requirement:** Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.1[a] | a baseline configuration is established |
| 3.4.1[b] | the baseline configuration includes hardware, software, firmware, and documentation |
| 3.4.1[c] | the baseline configuration is maintained (reviewed and updated) throughout the system development life cycle |
| 3.4.1[d] | a system inventory is established |
| 3.4.1[e] | the system inventory includes hardware, software, firmware, and documentation |
| 3.4.1[f] | the inventory is maintained (reviewed and updated) throughout the system development life cycle |

**Examine:** Configuration management policy; Procedures addressing the baseline configuration of the system; Procedures addressing system inventory; System security plan; Configuration management plan; System inventory records (plus 9 more object types in the assessment guide).

**Interview:** Personnel with configuration management responsibilities; Personnel with responsibilities for establishing the system inventory; Personnel with responsibilities for updating the system inventory; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for managing baseline configurations; Mechanisms supporting configuration control of the baseline configuration; Organizational processes for developing and documenting an inventory of system components; Organizational processes for updating inventory of system components; Mechanisms supporting or implementing the system inventory; Mechanisms implementing updating of the system inventory.


## CM.L2-3.4.2: Security Configuration Enforcement

**SPRS value:** 5 points.

**Requirement:** Establish and enforce security configuration settings for information technology products employed in organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.2[a] | security configuration settings for information technology products employed in the system are established and included in the baseline configuration |
| 3.4.2[b] | security configuration settings for information technology products employed in the system are enforced |

**Examine:** Configuration management policy; Baseline configuration; Procedures addressing configuration settings for the system; Configuration management plan; System security plan; System design documentation (plus 6 more object types in the assessment guide).

**Interview:** Personnel with security configuration management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for managing configuration settings; Mechanisms that implement, monitor, and/or control system configuration settings; Mechanisms that identify and/or document deviations from established configuration settings; Processes for managing baseline configurations; Mechanisms supporting configuration control of baseline configurations.


## CM.L2-3.4.3: System Change Management

**SPRS value:** 1 points.

**Requirement:** Track, review, approve or disapprove, and log changes to organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.3[a] | changes to the system are tracked |
| 3.4.3[b] | changes to the system are reviewed |
| 3.4.3[c] | changes to the system are approved or disapproved |
| 3.4.3[d] | changes to the system are logged |

**Examine:** Configuration management policy; Procedures addressing system configuration change control; Configuration management plan; System architecture and configuration documentation; System security plan; Change control records (plus 4 more object types in the assessment guide).

**Interview:** Personnel with configuration change control responsibilities; Personnel with information security responsibilities; System or network administrators; Members of change control board or similar.

**Test:** Organizational processes for configuration change control; Mechanisms that implement configuration change control.


## CM.L2-3.4.4: Security Impact Analysis

**SPRS value:** 1 points.

**Requirement:** Analyze the security impact of changes prior to implementation.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.4[a] | the security impact of changes to the system is analyzed prior to implementation |

**Examine:** Configuration management policy; Procedures addressing security impact analysis for system changes; Configuration management plan; Security impact analysis documentation; System security plan; Analysis tools and associated outputs (plus 3 more object types in the assessment guide).

**Interview:** Personnel with responsibility for conducting security impact analysis; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for security impact analysis.


## CM.L2-3.4.5: Access Restrictions for Change

**SPRS value:** 5 points.

**Requirement:** Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.5[a] | physical access restrictions associated with changes to the system are defined |
| 3.4.5[b] | physical access restrictions associated with changes to the system are documented |
| 3.4.5[c] | physical access restrictions associated with changes to the system are approved |
| 3.4.5[d] | physical access restrictions associated with changes to the system are enforced |
| 3.4.5[e] | logical access restrictions associated with changes to the system are defined |
| 3.4.5[f] | logical access restrictions associated with changes to the system are documented |
| 3.4.5[g] | logical access restrictions associated with changes to the system are approved |
| 3.4.5[h] | logical access restrictions associated with changes to the system are enforced |

**Examine:** Configuration management policy; Procedures addressing access restrictions for changes to the system; System security plan; Configuration management plan; System design documentation; System architecture and configuration documentation (plus 7 more object types in the assessment guide).

**Interview:** Personnel with logical access control responsibilities; Personnel with physical access control responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for managing access restrictions associated with changes to the system; Mechanisms supporting, implementing, and enforcing access restrictions associated with changes to the system.


## CM.L2-3.4.6: Least Functionality

**SPRS value:** 5 points.

**Requirement:** Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.6[a] | essential system capabilities are defined based on the principle of least functionality |
| 3.4.6[b] | the system is configured to provide only the defined essential capabilities |

**Examine:** Configuration management policy; Configuration management plan; Procedures addressing least functionality in the system; System security plan; System design documentation; System configuration settings and associated documentation (plus 2 more object types in the assessment guide).

**Interview:** Personnel with security configuration management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes prohibiting or restricting functions, ports, protocols, or services; Mechanisms implementing restrictions or prohibition of functions, ports, protocols, or services.


## CM.L2-3.4.7: Nonessential Functionality

**SPRS value:** 5 points.

**Requirement:** Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.7[a] | essential programs are defined |
| 3.4.7[b] | the use of nonessential programs is defined |
| 3.4.7[c] | the use of nonessential programs is restricted, disabled, or prevented as defined |
| 3.4.7[d] | essential functions are defined |
| 3.4.7[e] | the use of nonessential functions is defined |
| 3.4.7[f] | the use of nonessential functions is restricted, disabled, or prevented as defined |
| 3.4.7[g] | essential ports are defined |
| 3.4.7[h] | the use of nonessential ports is defined |
| 3.4.7[i] | the use of nonessential ports is restricted, disabled, or prevented as defined |
| 3.4.7[j] | essential protocols are defined |
| 3.4.7[k] | the use of nonessential protocols is defined |
| 3.4.7[l] | the use of nonessential protocols is restricted, disabled, or prevented as defined |
| 3.4.7[m] | essential services are defined |
| 3.4.7[n] | the use of nonessential services is defined |
| 3.4.7[o] | the use of nonessential services is restricted, disabled, or prevented as defined |

**Examine:** Configuration management policy; Procedures addressing least functionality in the system; Configuration management plan; System security plan; System design documentation; Security configuration checklists (plus 6 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for reviewing programs, functions, ports, protocols, and services on the system; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Organizational processes for reviewing and disabling nonessential programs, functions, ports, protocols, or services; Mechanisms implementing review and handling of nonessential programs, functions, ports, protocols, or services; Organizational processes preventing program execution on the system; Organizational processes for software program usage and restrictions; Mechanisms supporting or implementing software program usage and restrictions; Mechanisms preventing program execution on the system.


## CM.L2-3.4.8: Application Execution Policy

**SPRS value:** 5 points.

**Requirement:** Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.8[a] | a policy specifying whether whitelisting or blacklisting is to be implemented is specified |
| 3.4.8[b] | the software allowed to execute under whitelisting or denied use under blacklisting is specified |
| 3.4.8[c] | whitelisting to allow the execution of authorized software or blacklisting to prevent the use of unauthorized software is implemented as specified |

**Examine:** Configuration management policy; Procedures addressing least functionality in the system; System security plan; Configuration management plan; System design documentation; System configuration settings and associated documentation (plus 7 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for identifying software authorized or not authorized to execute on the system; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational process for identifying, reviewing, and updating programs authorized or not authorized to execute on the system; Process for implementing blacklisting or whitelisting; Mechanisms supporting or implementing blacklisting or whitelisting.


## CM.L2-3.4.9: User-Installed Software

**SPRS value:** 1 points.

**Requirement:** Control and monitor user-installed software.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.4.9[a] | a policy for controlling the installation of software by users is established |
| 3.4.9[b] | installation of software by users is controlled based on the established policy |
| 3.4.9[c] | installation of software by users is monitored |

**Examine:** Configuration management policy; Procedures addressing user installed software; Configuration management plan; System security plan; System design documentation; System configuration settings and associated documentation (plus 5 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for governing user-installed software; Personnel operating, using, or maintaining the system; Personnel monitoring compliance with user-installed software policy; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes governing user-installed software on the system; Mechanisms enforcing rules or methods for governing the installation of software by users; Mechanisms monitoring policy compliance.

---

## Where CM Assessments Go Wrong

- Baselines that are aspirations, not records (3.4.1): no documented baseline per system type, so drift cannot even be defined.
- Change tickets exist for servers but not for firewall rules, cloud configuration, or mobile device profiles (3.4.3 objectives cover the system, not just Windows).
- Least functionality (3.4.6, 3.4.7) unaddressed on the exact machines that process CUI: unused services running, no essential-capability analysis on file.
- Allowlisting or denylisting policy (3.4.8) undefined, so user-installed software control (3.4.9) has no rule to enforce.
