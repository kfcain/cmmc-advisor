# Microsoft Graph and GCC High Evidence Collectors

> Source: Microsoft Graph API (GCC High: graph.microsoft.us); Microsoft
> Defender for Endpoint API (api-gov.securitycenter.microsoft.us); Azure
> Resource Manager (management.usgovcloudapi.net); Entra ID P1/P2 sign-in
> logs; Intune; Microsoft Sentinel

## Endpoint overrides (GCC High)

| Service | Base URL |
|---------|----------|
| Microsoft Graph | `https://graph.microsoft.us/v1.0` |
| Entra token | `https://login.microsoftonline.us/{tenant}/oauth2/v2.0/token` |
| Defender for Endpoint | `https://api-gov.securitycenter.microsoft.us/api` |
| Azure ARM (Sentinel) | `https://management.usgovcloudapi.net` |

Token audience must match the API resource. A commercial Graph token against
`.us` endpoints returns 403 even with correct role assignments.

---

## Collectors in this repo

| Collector id | API | Permissions (app-only) |
|--------------|-----|------------------------|
| `entra-signins` | `GET /auditLogs/signIns` | `AuditLog.Read.All`, `Policy.Read.ConditionalAccess` |
| `entra-conditional-access` | `GET /identity/conditionalAccess/policies` | `Policy.Read.ConditionalAccess` |
| `intune-compliance` | `GET /deviceManagement/managedDevices` | `DeviceManagementManagedDevices.Read.All` |
| `defender-endpoint` | `GET /api/machines`, `GET /api/alerts` | `Machine.Read.All`, `Alert.Read.All` |
| `sentinel-health` | ARM incidents + Log Analytics query | `Microsoft.SecurityInsights/incidents/read`, workspace query |

See `references/data/evidence-collector-manifest.json` for objective mappings.

---

## Evidence artifacts → assessment objectives

### Sign-in logs (`entra-signins`)

Proves: **IA.L2-3.5.3** (MFA enforced), **AU.L2-3.3.2** (user attribution),
**AU.L2-3.3.1** (audit record creation).

Sample filter:

```
GET /auditLogs/signIns?$filter=createdDateTime ge 2026-06-01T00:00:00Z&$top=200
```

Export fields: `userPrincipalName`, `ipAddress`, `conditionalAccessStatus`,
`appliedConditionalAccessPolicies`, `authenticationRequirement`.

**Rate limit:** 5 requests per 10 seconds per app (Graph identity/audit).

**Retention gap:** Default Entra retention may not satisfy AU.L2-3.3.1 (e–f).
Pair API samples with Log Analytics archive policy evidence.

### Conditional Access (`entra-conditional-access`)

Proves: **IA.L2-3.5.3**, **AC.L2-3.1.2** (transaction/function control via app/session).

Export all enabled policies as JSON; include authentication strength requirements
when using phishing-resistant MFA.

### Intune (`intune-compliance`)

Proves: **AC.L2-3.1.18/19** (mobile), **CM.L2-3.4.1** (baseline), **SC.L2-3.13.11**
(FIPS mode on endpoints when enforced via compliance policy).

### Defender for Endpoint (`defender-endpoint`)

Proves: **SI.L2-3.14.2** (malicious code protection), **SI.L2-3.14.6** (monitoring).

Onboarding coverage query: machines where `healthStatus` is not `Inactive`.

### Sentinel (`sentinel-health`)

Proves: **AU.L2-3.3.5** (correlation), **SI.L2-3.14.6**, connector health for
**AU.L2-3.3.1** (a–b).

Export: enabled analytics rules, open incidents last 30 days, data connector
status table.

---

## Purview unified audit (manual collector note)

M365 unified audit log for SharePoint/Exchange CUI access is not yet a
registered collector id. Export via Purview compliance portal or Graph
`GET /security/auditLog/queries` where licensed. Map to **AU** and **MP**
families. Add a collector entry when Graph export stabilizes for GCC High.

---

## Running collectors

```bash
python3 scripts/collect_evidence.py program-data.yaml --dry-run \
  --collectors entra-signins,entra-conditional-access,intune-compliance,defender-endpoint,sentinel-health
```

Live collection requires app registration in Entra Government with admin
consent and secrets in a vault (not stored in program data).

---

## Related

- `../productivity/microsoft-365-gcc.md`: tenancy and practice narrative
- `../cloud-platforms/azure-government.md`: Sentinel and platform logging
- `references/grc/inherited-controls-mapping.md`: CRM inheritance from GCC High
