# Development Environment Baseline (SC.L2-3.13.2)

> Source: NIST SP 800-171 Rev 2 (3.13.2, 3.4.2, 3.14.1); NIST SSDF (SP 800-218);
> CMMC Assessment Guide examine/interview lists for SC.L2-3.13.2

SC.L2-3.13.2 requires **architectural designs, software development techniques,
and systems engineering principles** that promote security be identified **and
employed**. Assessors score six objectives (a through f); see
`references/assessment-objectives/sc.md`.

## When this baseline applies

- In-house software that processes CUI
- Custom integrations on CUI systems
- Infrastructure-as-code repos defining the enclave
- Dev/test environments that hold CUI-like data (sanitized or not)

Not a substitute for AC.L2-3.1.22 (public release); still gate exports separately.

## Identify (objectives a, b, c)

Document in SSP appendix or secure SDLC policy:

| Technique | Example in your environment |
|-----------|----------------------------|
| Architectural | Threat model for enclave; zero trust segmentation |
| Development | Branch protection, required review, dependency scanning |
| Systems engineering | Change advisory board; IaC peer review |

## Employ (objectives d, e, f)

Prove execution with records, not policy alone:

- Last quarter merged PRs with approval on CUI app repo
- SAST/Dependabot or equivalent findings triaged
- IaC pipeline plan/apply logs for firewall or identity changes
- Architecture decision record (ADR) for major CUI system changes

## Shared system resources (SC.L2-3.13.4)

Dev CI runners shared between teams: document session isolation, secret hygiene,
and artifact retention so CUI build artifacts do not leak to non-CUI jobs.

## Baseline checklist

| # | Item | Evidence |
|---|------|----------|
| 1 | SDLC policy version and owner | Policy PDF in document bucket |
| 2 | Repo list in scope for CUI code | Inventory in program data |
| 3 | Branch protection enforced | GitHub/GitLab export |
| 4 | Secret scanning enabled | Platform settings export |
| 5 | Test/staging separation from prod | Diagram + access list |
| 6 | Developer workstation baseline | Intune/GPO compliance (CM.L2-3.4.1) |

## Program data

```yaml
cui:
  - name: EDS firmware build pipeline
    baseline_profile: development-sdlc
    baseline_validation:
      validated: "2026-06-25"
      repo: github.com/example/eds-firmware
      branch_protection: true
```

## AI-assisted development

If developers use Copilot, Cursor, or Claude on CUI code, add controls from
`../ai-services/ai-dev-tools.md` (no CUI in public model training, tenant
boundaries, logging).
