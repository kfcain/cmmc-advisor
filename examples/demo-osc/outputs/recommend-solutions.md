# CMMC gap-driven solution hints

SPRS points at stake on open gaps: **16**

Verify every FedRAMP listing at marketplace.fedramp.gov before procurement.
See `references/grc/solution-selection.md` for Rev5 Class C/D and 20x rules.

## AU: SIEM / log aggregation

- **Marketplace:** SIEM category in references/fedramp-marketplace-guide.md (Splunk, Sentinel, etc.)
- **On-prem / CIS fallback:** On-prem SIEM with CIS log retention baseline; cloud-native collectors in evidence manifest

## CM: Configuration management / MDM / baselines

- **Marketplace:** MDM/endpoint management FedRAMP packages when management plane touches CUI
- **On-prem / CIS fallback:** CIS Benchmarks + DISA STIGs per OS; Intune/GPO exports for evidence

## IA: MFA / authenticator management

- **Marketplace:** FedRAMP Moderate MFA/PAM (Duo FedRAMP package, etc.)
- **On-prem / CIS fallback:** Entra Conditional Access / on-prem MFA with CIS authenticator guidance

## AC: IAM / PAM / identity governance

- **Marketplace:** Search marketplace.fedramp.gov: IAM, PAM, identity governance; Moderate or Rev5 Class C
- **On-prem / CIS fallback:** CIS Microsoft/Azure benchmarks for IdP; on-prem: CIS Controls v8 IG1 for access
