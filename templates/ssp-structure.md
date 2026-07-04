# SSP Structure: AO-Level System Security Plan

> Source: structure mirrors a practitioner CMMC Level 2 SSP template
> built around NIST SP 800-171A assessment objectives; conformity
> vocabulary per 32 CFR 170.24; asset categories per 32 CFR 170.19(c)

This is the canonical section layout `scripts/generate_ssp.py` produces
and the checklist to review any AO-level SSP against. The distinguishing
feature: conformity is recorded per assessment objective, not just per
requirement, so the SSP answers exactly what a C3PAO determines.

## Front matter

1. **Cover**: organization logo, "System Security Plan (SSP)", system
   name, date, revision.
2. **Record of Acceptance/Approval**: system owner signature block
   (printed name, date, signature).
3. **Purpose**: why this SSP exists; the system it covers.
4. **Scope**: the CMMC Assessment Scope in prose; what is out of scope
   and why the separation holds.
5. **References**: FISMA, 32 CFR Part 2002, FAR 52.204-21, DFARS
   252.204-7012, NIST SP 800-171 Rev 2, NIST SP 800-171A, CMMC
   documentation, 32 CFR Part 170.
6. **Roles and Responsibilities**: named individuals with duties
   (system owner, CIO/ISSM-equivalent, Affirming Official, control
   owners; see `../references/grc/program-governance.md`).
7. **System Information**: responsible organization, system owner, and
   CIO tables (name, title, contact).
8. **System Environment**: narrative plus the CUI scoping components.
9. **Asset Types**: one table per 32 CFR 170.19(c) category: CUI
   Assets, Contractor Risk Managed Assets, Security Protection Assets,
   Specialized Assets, Out-of-Scope Assets.
10. **Networking Diagrams**: network diagram and CUI flow diagram
    (figures referenced from the data file). One combined diagram
    covering both the network topology and the CUI flows also
    satisfies this section.
11. **Hardware and Software Information**: inventory table.
12. **Organizational Responsibilities**: enforcement, exception to
    policy, non-compliance handling.
13. **Revision History** and **Acronyms**.

## Requirement families (the body)

One section per family (AC, AT, AU, CM, IA, IR, MA, MP, PS, PE, RA, CA,
SC, SI), containing one block per requirement:

- Requirement statement (verbatim NIST SP 800-171 Rev 2 text)
- **REQUIREMENT CONFORMITY**: met / not-met / partially-met /
  not-applicable / not-assessed
- **PRACTICE ID** and **PRACTICE NAME** (e.g. AC.L2-3.1.1, Authorized
  Access Control)
- **ASSESSMENT OBJECTIVE(S)**: for each 800-171A objective:
  - the determine-if text (e.g. `[a] authorized users are identified`)
  - **AO CONFORMITY**: met / not-met / not-applicable / inherited /
    shared / not-assessed
  - **Assessment Objective Conformity Statement**: the narrative. Good
    statements name the mechanism, the policy, and the evidence in this
    system ("Conditional Access policy CA-01 blocks..."), not generic
    intent. Inherited or shared objectives cite the provider CRM row and
    state the customer-side share.
  - Evidence references (artifact name and link)

## Closing sections

14. **Plans of Action and Milestones (POA&M)**: table with Priority,
    POA&M description, Due Date, Actions. Only POA&M-eligible gaps per
    32 CFR 170.21 (see `../references/poam-management.md`); 180-day
    closeout from the Conditional Status Date.
15. **NIST CMVP Certificates**: table with Certificate #, Vendor, Module
    Name, Standard, Status, Sunset Date, Associated Security Policy.
    This is the backing for every FIPS-validated cryptography claim
    (SC.L2-3.13.11); verify each certificate at the NIST CMVP registry
    before the assessment.

## Review checklist

- Every requirement block present (110 at Level 2), every objective row
  present (320), no objective left at "not assessed" in a final SSP.
- Boundary prose, asset tables, and diagrams tell the same story.
- Narratives are system-specific and name mechanisms; a reader could
  find the control from the text alone.
- Inherited and shared objectives trace to a CRM reference and a body
  of evidence location
  (see `../references/grc/inherited-controls-mapping.md`).
- POA&M entries only where 32 CFR 170.21 allows them; the SSP itself
  (CA.L2-3.12.4) is never POA&M-eligible.
- CMVP table rows current (not historical or sunset) for the modules
  actually deployed.
