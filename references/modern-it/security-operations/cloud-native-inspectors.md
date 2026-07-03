# Cloud-Native and Third-Party Inspector Evidence

> Source: AWS Config, CloudTrail, Security Hub, GuardDuty API references;
> Google Cloud SCC and Assured Workloads; CrowdStrike Falcon API; Zscaler
> OneAPI; Palo Alto Strata Cloud Manager; Cisco Duo Admin API; Splunk REST

## AWS GovCloud

| Collector id | Service | IAM actions | Primary objectives |
|--------------|---------|-------------|-------------------|
| `aws-config-compliance` | Config | `GetComplianceSummaryByConfigRule`, `SelectResourceConfig` | CM.L2-3.4.1, SC.L2-3.13.8, SC.L2-3.13.11 |
| `aws-cloudtrail` | CloudTrail | `LookupEvents` | AU.L2-3.3.1, AU.L2-3.3.2 |
| `aws-security-hub` | Security Hub | `GetFindings`, `DescribeStandardsControls` | SI.L2-3.14.1, CA.L2-3.12.3 |

**GovCloud endpoints:** region-specific (`*.us-gov-west-1.amazonaws.com`). Use
org Config aggregator for multi-account scope.

**Rate limits:** CloudTrail LookupEvents 2 req/sec; Security Hub GetFindings
3 req/sec burst 6.

Narrative: `../cloud-platforms/aws-govcloud.md`

---

## GCP Assured Workloads

| Collector id | Service | Role | Primary objectives |
|--------------|---------|------|-------------------|
| `gcp-scc-findings` | Security Command Center | `roles/securitycenter.findingsViewer` | SI.L2-3.14.6, SI.L2-3.14.1 |

Filter findings to the Assured Workloads folder. Pair with Cloud Audit Logs
sink configuration for AU retention evidence.

Narrative: `../cloud-platforms/gcp-assured.md`

---

## EDR / XDR (third-party)

| Collector id | Platform | API | Primary objectives |
|--------------|----------|-----|-------------------|
| `crowdstrike-hosts` | CrowdStrike Falcon | `/devices/queries/devices/v1` | SI.L2-3.14.2, SI.L2-3.14.6 |
| `defender-endpoint` | Microsoft (see microsoft-graph-evidence.md) | MDE API | SI.L2-3.14.x |

**CrowdStrike:** OAuth2 token TTL ~30 min; cache tokens. Region-specific base
URL (`api.us-2.crowdstrike.com`, etc.).

GRC Engineering Club: `crowdstrike-inspector` plugin merges via `merge_findings.py`.

---

## SASE / ZTNA

| Collector id | Platform | API | Primary objectives |
|--------------|----------|-----|-------------------|
| `zscaler-policy` | Zscaler ZIA | OneAPI `GET /firewallFilteringRules` | SC.L2-3.13.1, AC.L2-3.1.3 |
| `prisma-access-rules` | Palo Alto SCM | Strata OAuth2 security rules | SC.L2-3.13.1, SC.L2-3.13.6 |

**Gap:** Session-level audit proof (AU.L2-3.3.1 c–f) requires log forwarding
to SIEM, not policy API alone. Collectors export **policy posture**; add
Sentinel/Splunk collector for session logs.

Narrative: `../endpoints/remote-work.md`

---

## MFA (Duo alongside Entra)

| Collector id | Platform | API | Primary objectives |
|--------------|----------|-----|-------------------|
| `duo-auth-logs` | Cisco Duo | `GET /admin/v2/logs/authentication` | IA.L2-3.5.2, IA.L2-3.5.3 |

HMAC-SHA1 signed requests; clock sync required. Paginate with `mintime`/`maxtime`.

When Duo is Entra External Authentication Method, prefer Entra sign-in logs for
unified evidence (`entra-signins` collector).

---

## SIEM (Splunk)

| Collector id | Platform | API | Primary objectives |
|--------------|----------|-----|-------------------|
| `splunk-ingest-health` | Splunk Enterprise | `/services/search/jobs/export` | AU.L2-3.3.1, AU.L2-3.3.5 |

Search example: index=_internal source=*metrics.log group=per_sourcetype_thruput
for ingest health.

For Sentinel-native shops, use `sentinel-health` instead.

Marketplace short-list: `references/fedramp-marketplace-guide.md` (SIEM category).

---

## GRC inspector mapping

Install GRC Engineering Club connectors for live pulls:

| Connector | Maps through |
|-----------|--------------|
| `aws-inspector` | 800-53 → `800-53-crosswalk.json` → CMMC reqs |
| `azure-inspector` | same |
| `gcp-inspector` | same |
| `crowdstrike-inspector` | same |
| `splunk-inspector` | same |

```bash
python3 scripts/merge_findings.py ~/.cache/claude-grc/findings/aws-inspector/latest.json program-data.yaml
```

---

## Dry-run all cloud collectors

```bash
python3 scripts/collect_evidence.py program-data.yaml --dry-run \
  --collectors aws-config-compliance,aws-cloudtrail,gcp-scc-findings,crowdstrike-hosts,zscaler-policy,duo-auth-logs
```
