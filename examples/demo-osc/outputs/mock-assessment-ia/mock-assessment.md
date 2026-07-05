# Mock Assessment Prep Pack

**System:** APM GCC High CUI Enclave
**Generated:** 2026-07-05

## Discovery watchlist (chase these first)

- **Open OQ-0002** (Security engineer): Does the MSP NOC's NinjaOne alert console constitute a second, undocumented monitoring path holding Security Protection Data?
- **Open OQ-0001** (IT lead): What SMTP relay does the Floor-2 MFP scan-to-email path use, and does it transit a commercial mail system?
- **Open OQ-0003** (Sam Patel): Does the mail-room accumulation shelf (pre-shred staging) meet locked-media control for overnight storage?
- **Unverified QA-0002** (confidence: reported): Can the Floor-2 MFP scan to email, and if so, to which mail system?
- **Assumption AS-0001**: No CUI is scanned at the Floor-2 MFP because signage and policy prohibit it. Risk if wrong: An assessor treats policy-only separation as no separation; a CUI scan through a commercial relay recategorizes the MFP as a CUI asset and pulls its network segment into scope.


## IA (11 practices)

Mock assessment block for IA (11 practices in scope). Confirm scope narrative covers each practice before interviews.

### IA.L2-3.5.1: Identification
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Procedures addressing user identification and authentication
  - System security plan, system design documentation
  - System configuration settings and associated documentation
  - System audit logs and records
  - List of system accounts
  - Other relevant documents or records
- **Test:**
  - Organizational processes for uniquely identifying and authenticating users
  - Mechanisms supporting or implementing identification and authentication capability
- **Objective [a]** system users are identified
  - Interview: Interview Personnel with system operations responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] system users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] system users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] system users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with account management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] system users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] system users are identified? Walk through roles, frequency, and evidence.
- **Objective [b]** processes acting on behalf of users are identified
  - Interview: Interview Personnel with system operations responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] processes acting on behalf of users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] processes acting on behalf of users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] processes acting on behalf of users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with account management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] processes acting on behalf of users are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [b] processes acting on behalf of users are identified? Walk through roles, frequency, and evidence.
- **Objective [c]** devices accessing the system are identified
  - Interview: Interview Personnel with system operations responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] devices accessing the system are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] devices accessing the system are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [c] devices accessing the system are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with account management responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] devices accessing the system are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [c] devices accessing the system are identified? Walk through roles, frequency, and evidence.

### IA.L2-3.5.10: Cryptographically-Protected Passwords
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - System security plan
  - Procedures addressing authenticator management
  - Procedures addressing user identification and authentication
  - System design documentation
  - List of system authenticator types
  - System configuration settings and associated documentation
  - Change control records associated with managing system authenticators
  - System audit logs and records
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing authenticator management capability
- **Objective [a]** passwords are cryptographically protected in storage
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] passwords are cryptographically protected in storage? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] passwords are cryptographically protected in storage? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] passwords are cryptographically protected in storage? Walk through roles, frequency, and evidence.
- **Objective [b]** passwords are cryptographically protected in transit
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] passwords are cryptographically protected in transit? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] passwords are cryptographically protected in transit? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] passwords are cryptographically protected in transit? Walk through roles, frequency, and evidence.

### IA.L2-3.5.11: Obscure Feedback
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Procedures addressing authenticator feedback
  - System security plan
  - System design documentation
  - System configuration settings and associated documentation
  - System audit logs and records
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing the obscuring of feedback of authentication information during authentication
- **Objective [a]** authentication information is obscured during the authentication process
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] authentication information is obscured during the authentication process? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] authentication information is obscured during the authentication process? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] authentication information is obscured during the authentication process? Walk through roles, frequency, and evidence.

### IA.L2-3.5.2: Authentication
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - System security plan
  - Procedures addressing authenticator management
  - Procedures addressing user identification and authentication
  - System design documentation
  - List of system authenticator types
  - System configuration settings and associated documentation
  - Change control records associated with managing system authenticators
  - System audit logs and records
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing authenticator management capability
- **Objective [a]** the identity of each user is authenticated or verified as a prerequisite to system access
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] the identity of each user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] the identity of each user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] the identity of each user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
- **Objective [b]** the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
- **Objective [c]** the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [c] the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access? Walk through roles, frequency, and evidence.

### IA.L2-3.5.3: Multifactor Authentication
- Program conformity: **partially-met**
- **Examine:**
  - Identification and authentication policy
  - Procedures addressing user identification and authentication
  - System security plan
  - System design documentation
  - System configuration settings and associated documentation
  - System audit logs and records
  - List of system accounts
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing authenticator management capability
- **Objective [a]** privileged accounts are identified
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] privileged accounts are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] privileged accounts are identified? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] privileged accounts are identified? Walk through roles, frequency, and evidence.
- **Objective [b]** multifactor authentication is implemented for local access to privileged accounts
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] multifactor authentication is implemented for local access to privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] multifactor authentication is implemented for local access to privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] multifactor authentication is implemented for local access to privileged accounts? Walk through roles, frequency, and evidence.
- **Objective [c]** multifactor authentication is implemented for network access to privileged accounts
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] multifactor authentication is implemented for network access to privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] multifactor authentication is implemented for network access to privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [c] multifactor authentication is implemented for network access to privileged accounts? Walk through roles, frequency, and evidence.
- **Objective [d]** multifactor authentication is implemented for network access to non-privileged accounts
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [d] multifactor authentication is implemented for network access to non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [d] multifactor authentication is implemented for network access to non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [d] multifactor authentication is implemented for network access to non-privileged accounts? Walk through roles, frequency, and evidence.

### IA.L2-3.5.4: Replay-Resistant Authentication
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Procedures addressing user identification and authentication
  - System security plan
  - System design documentation
  - System configuration settings and associated documentation
  - System audit logs and records
  - List of privileged system accounts
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing identification and authentication capability or replay resistant authentication mechanisms
- **Objective [a]** replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts
  - Interview: Interview Personnel with system operations responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with account management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts? Walk through roles, frequency, and evidence.

### IA.L2-3.5.5: Identifier Reuse
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - System security plan
  - Procedures addressing authenticator management
  - Procedures addressing user identification and authentication
  - System design documentation
  - List of system authenticator types
  - System configuration settings and associated documentation
  - Change control records associated with managing system authenticators
  - System audit logs and records
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing authenticator management capability
- **Objective [a]** a period within which identifiers cannot be reused is defined
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] a period within which identifiers cannot be reused is defined? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] a period within which identifiers cannot be reused is defined? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] a period within which identifiers cannot be reused is defined? Walk through roles, frequency, and evidence.
- **Objective [b]** reuse of identifiers is prevented within the defined period
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] reuse of identifiers is prevented within the defined period? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] reuse of identifiers is prevented within the defined period? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] reuse of identifiers is prevented within the defined period? Walk through roles, frequency, and evidence.

### IA.L2-3.5.6: Identifier Handling
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Procedures addressing identifier management
  - Procedures addressing account management
  - System security plan
  - System design documentation
  - System configuration settings and associated documentation
  - List of system accounts
  - List of identifiers generated from physical access control devices
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing identifier management
- **Objective [a]** a period of inactivity after which an identifier is disabled is defined
  - Interview: Interview Personnel with identifier management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] a period of inactivity after which an identifier is disabled is defined? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] a period of inactivity after which an identifier is disabled is defined? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] a period of inactivity after which an identifier is disabled is defined? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] a period of inactivity after which an identifier is disabled is defined? Walk through roles, frequency, and evidence.
- **Objective [b]** identifiers are disabled after the defined period of inactivity
  - Interview: Interview Personnel with identifier management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] identifiers are disabled after the defined period of inactivity? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] identifiers are disabled after the defined period of inactivity? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] identifiers are disabled after the defined period of inactivity? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [b] identifiers are disabled after the defined period of inactivity? Walk through roles, frequency, and evidence.

### IA.L2-3.5.7: Password Complexity
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Password policy
  - Procedures addressing authenticator management
  - System security plan
  - System configuration settings and associated documentation
  - System design documentation
  - Password configurations and associated documentation
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing authenticator management capability
- **Objective [a]** password complexity requirements are defined
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] password complexity requirements are defined? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] password complexity requirements are defined? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] password complexity requirements are defined? Walk through roles, frequency, and evidence.
- **Objective [b]** password change of character requirements are defined
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] password change of character requirements are defined? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] password change of character requirements are defined? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] password change of character requirements are defined? Walk through roles, frequency, and evidence.
- **Objective [c]** minimum password complexity requirements as defined are enforced when new passwords are created
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] minimum password complexity requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [c] minimum password complexity requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [c] minimum password complexity requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.
- **Objective [d]** minimum password change of character requirements as defined are enforced when new passwords are created
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [d] minimum password change of character requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [d] minimum password change of character requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [d] minimum password change of character requirements as defined are enforced when new passwords are created? Walk through roles, frequency, and evidence.

### IA.L2-3.5.8: Password Reuse
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Password policy
  - Procedures addressing authenticator management
  - System security plan
  - System design documentation
  - System configuration settings and associated documentation
  - Password configurations and associated documentation
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing password-based authenticator management capability
- **Objective [a]** the number of generations during which a password cannot be reused is specified
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] the number of generations during which a password cannot be reused is specified? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] the number of generations during which a password cannot be reused is specified? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] the number of generations during which a password cannot be reused is specified? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] the number of generations during which a password cannot be reused is specified? Walk through roles, frequency, and evidence.
- **Objective [b]** reuse of passwords is prohibited during the specified number of generations
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] reuse of passwords is prohibited during the specified number of generations? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [b] reuse of passwords is prohibited during the specified number of generations? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [b] reuse of passwords is prohibited during the specified number of generations? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [b] reuse of passwords is prohibited during the specified number of generations? Walk through roles, frequency, and evidence.

### IA.L2-3.5.9: Temporary Passwords
- Program conformity: **met**
- **Examine:**
  - Identification and authentication policy
  - Password policy
  - Procedures addressing authenticator management
  - System security plan
  - System configuration settings and associated documentation
  - System design documentation
  - Password configurations and associated documentation
  - Other relevant documents or records
- **Test:**
  - Mechanisms supporting or implementing password-based authenticator management capability
- **Objective [a]** an immediate change to a permanent password is required when a temporary password is used for system logon
  - Interview: Interview Personnel with authenticator management responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] an immediate change to a permanent password is required when a temporary password is used for system logon? Walk through roles, frequency, and evidence.
  - Interview: Interview Personnel with information security responsibilities: How does APM GCC High CUI Enclave satisfy objective [a] an immediate change to a permanent password is required when a temporary password is used for system logon? Walk through roles, frequency, and evidence.
  - Interview: Interview System or network administrators: How does APM GCC High CUI Enclave satisfy objective [a] an immediate change to a permanent password is required when a temporary password is used for system logon? Walk through roles, frequency, and evidence.
  - Interview: Interview System developers: How does APM GCC High CUI Enclave satisfy objective [a] an immediate change to a permanent password is required when a temporary password is used for system logon? Walk through roles, frequency, and evidence.

