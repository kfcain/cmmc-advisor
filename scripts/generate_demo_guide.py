#!/usr/bin/env python3
"""Generate DEMO-OSC-GUIDE.html for examples/demo-osc/."""

from __future__ import annotations

import html
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path, limit: int = 8000) -> str:
    if not path.is_file():
        return "(not generated)"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > limit:
        return text[:limit] + "\n… (truncated)"
    return text


def esc(value: object) -> str:
    return html.escape(str(value))


def artifact_row(name: str, rel: str, desc: str) -> str:
    return f"""
    <tr>
      <td><a href="{esc(rel)}">{esc(name)}</a></td>
      <td><code>{esc(rel)}</code></td>
      <td>{esc(desc)}</td>
    </tr>"""


def main() -> int:
    demo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "examples" / "demo-osc"
    program_path = demo_root / "program-data.yaml"
    out_dir = demo_root / "outputs"

    try:
        import yaml

        program = yaml.safe_load(program_path.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.exit(f"cannot load program data: {exc}")

    org = program.get("organization") or {}
    assessment = program.get("assessment") or {}
    poam = validate_poam = load_json(out_dir / "validate-poam.json") or {}
    sprs = load_json(out_dir / "sprs.json") or {}
    discovery = read_text(out_dir / "discovery-report.txt", 5000)

    req_count = len(program.get("requirements") or {})
    asset_buckets = program.get("assets") or {}
    asset_total = sum(len(v or []) for v in asset_buckets.values() if isinstance(v, list))
    qa_count = len((program.get("discovery") or {}).get("qa_log") or [])
    oq_count = len((program.get("discovery") or {}).get("open_questions") or [])

    artifacts = [
        ("Program dashboard", "outputs/dashboard.html", "Internal ISSM view: SPRS, POA&M, all 320 AOs"),
        ("System Security Plan", "outputs/ssp.md", "AO-level SSP markdown from program data"),
        ("Trust center", "outputs/trust-center.html", "Public deny-by-default page"),
        ("Executive brief", "outputs/executive-brief.html", "C-level gap and selection summary"),
        ("Network diagram", "outputs/diagrams/network.svg", "Topology from program-data zones/nodes"),
        ("CUI flow diagram", "outputs/diagrams/cui-flow.svg", "CUI/FCI/SPD flows only"),
        ("OSCAL SSP", "outputs/oscal-ssp.json", "FedRAMP/GRC tooling interchange"),
        ("SPRS scoresheet", "outputs/sprs.json", "Computed score with methodology notes"),
        ("Mock assessment (IA)", "outputs/mock-assessment-ia/mock-assessment.md", "Assessor interview/evidence pack"),
        ("Responsibility matrix", "outputs/responsibility-matrix/responsibility-matrix.md", "Internal RACI export"),
        ("Solution recommendations", "outputs/recommend-solutions.md", "Gap-driven Marketplace hints"),
        ("ControlBot profile", "outputs/controlbot-profile.yaml", "IaC inherited-control export"),
        ("Test report", "outputs/demo-test-report.txt", "All generator/validator command output"),
        ("Program data", "program-data.yaml", "Source of truth for the demo OSC"),
    ]

    routing_rows = [
        ("Level 2 scoping / CUI enclave", "references/scoping-and-cui.md", "Tenant boundary, asset categories"),
        ("GCC High tenancy", "references/modern-it/productivity/microsoft-365-gcc.md", "GCC vs GCC High decision"),
        ("Phased rollout", "references/modern-it/productivity/gcch-implementation-workbook.md", "Identity → devices → data → monitoring"),
        ("CRM inheritance", "references/grc/inherited-controls-mapping.md", "Shared SC-13 / PE rows from GCC High"),
        ("Graph evidence", "references/modern-it/security-operations/microsoft-graph-evidence.md", "Collector endpoints USGov"),
        ("POA&M rules", "references/poam-management.md", "180-day closeout, banned practices"),
        ("Companion stack", "references/grc/companion-stack.md", "ControlBot → program-data import"),
        ("Assessor discovery", "references/assessor-playbook/scope-discovery-question-bank.md", "12 discovery phases"),
    ]

    script_rows = [
        ("bootstrap_demo_osc.py", "Create/regenerate this entire demo package"),
        ("generate_dashboard.py", "Self-contained HTML program dashboard"),
        ("generate_ssp.py", "AO-level SSP markdown/DOCX"),
        ("generate_diagrams.py", "Network + CUI flow SVG/Mermaid"),
        ("generate_trust_center.py", "Public trust page (strict deny-by-default)"),
        ("collect_evidence.py", "Run collectors; --dry-run for pipeline test"),
        ("validate_poam.py", "32 CFR 170.21 eligibility and SPRS gates"),
        ("discovery_report.py", "Discovery memory coverage and ID integrity"),
        ("import_controlbot_seeds.py", "Terraform Checkov POA&M → program data"),
        ("eval_routing_smoke.py", "Deterministic eval scenario path checks"),
    ]

    eval_rows = [
        ("level-2-scoping-basic.yaml", "SDVOSB SaaS on GovCloud — level and boundary"),
        ("modern-it-gcch-workbook-routing.yaml", "Phased GCC High → AO mapping"),
        ("domain-ia-mfa-gcch.yaml", "Conditional Access / MFA objectives"),
        ("grc-inherited-controls-crm.yaml", "CRM rows → per-AO inheritance"),
        ("companion-stack-e2e-pipeline.yaml", "ControlBot import through dashboard"),
        ("assessor-grill-kickoff.yaml", "Discovery rail kickoff"),
        ("scoring-sprs-conditional.yaml", "SPRS -203 floor and conditional path"),
    ]

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CMMC Advisor Demo OSC — Atlas Precision Manufacturing</title>
  <style>
    :root {{
      --bg: #0f1419;
      --panel: #1a2332;
      --border: #2d3a4d;
      --text: #e6edf3;
      --muted: #8b9cb3;
      --accent: #58a6ff;
      --ok: #3fb950;
      --warn: #d29922;
      --bad: #f85149;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.55;
    }}
    header {{
      padding: 2rem 2rem 1rem;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(135deg, #1a2332 0%, #0f1419 100%);
    }}
    h1 {{ margin: 0 0 0.25rem; font-size: 1.75rem; }}
    .subtitle {{ color: var(--muted); max-width: 60rem; }}
    nav {{
      position: sticky;
      top: 0;
      background: var(--panel);
      border-bottom: 1px solid var(--border);
      padding: 0.5rem 2rem;
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      z-index: 10;
    }}
    nav a {{ color: var(--accent); text-decoration: none; font-size: 0.9rem; }}
    nav a:hover {{ text-decoration: underline; }}
    main {{ max-width: 72rem; margin: 0 auto; padding: 1.5rem 2rem 4rem; }}
    section {{ margin-bottom: 2.5rem; }}
    h2 {{
      font-size: 1.25rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.35rem;
      margin-top: 0;
    }}
    h3 {{ font-size: 1rem; color: var(--accent); margin-bottom: 0.5rem; }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr));
      gap: 0.75rem;
      margin: 1rem 0;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.85rem;
    }}
    .card .val {{ font-size: 1.5rem; font-weight: 600; }}
    .card .lbl {{ font-size: 0.8rem; color: var(--muted); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      margin: 0.75rem 0;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.5rem 0.65rem;
      text-align: left;
      vertical-align: top;
    }}
    th {{ background: var(--panel); color: var(--muted); font-weight: 600; }}
    code, pre {{
      font-family: ui-monospace, monospace;
      font-size: 0.82rem;
    }}
    pre {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1rem;
      overflow-x: auto;
      white-space: pre-wrap;
    }}
    a {{ color: var(--accent); }}
    .pill {{
      display: inline-block;
      padding: 0.15rem 0.5rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
    }}
    .pill-ok {{ background: #23863633; color: var(--ok); }}
    .pill-warn {{ background: #9e6a0333; color: var(--warn); }}
    .pill-bad {{ background: #da363333; color: var(--bad); }}
    iframe {{
      width: 100%;
      height: 420px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
    }}
    .cmd {{ color: var(--ok); }}
  </style>
</head>
<body>
  <header>
    <h1>Atlas Precision Manufacturing LLC</h1>
    <p class="subtitle">
      Demo Organization Seeking Certification (OSC) for exercising the full CMMC Advisor
      program toolkit. Fictional 45-person machine shop processing CUI in a GCC High enclave
      with Azure Government, Intune, Sentinel, and ControlBot-gated Terraform IaC.
      Generated {esc(date.today())}.
    </p>
  </header>
  <nav>
    <a href="#snapshot">Snapshot</a>
    <a href="#story">Org story</a>
    <a href="#program-data">Program data</a>
    <a href="#validation">Validation</a>
    <a href="#artifacts">Artifacts</a>
    <a href="#preview">Preview</a>
    <a href="#routing">SKILL routing</a>
    <a href="#scripts">Scripts</a>
    <a href="#evals">Evals</a>
    <a href="#commands">Commands</a>
  </nav>
  <main>
    <section id="snapshot">
      <h2>OSC snapshot</h2>
      <div class="cards">
        <div class="card"><div class="val">{esc(org.get('name', ''))}</div><div class="lbl">Organization</div></div>
        <div class="card"><div class="val">{esc(org.get('system_name', ''))}</div><div class="lbl">System</div></div>
        <div class="card"><div class="val">CMMC {esc(assessment.get('level', '?'))}</div><div class="lbl">Target level</div></div>
        <div class="card"><div class="val">{esc(assessment.get('path', ''))}</div><div class="lbl">Assessment path</div></div>
        <div class="card"><div class="val">{req_count}</div><div class="lbl">Requirements in program data</div></div>
        <div class="card"><div class="val">{asset_total}</div><div class="lbl">Inventoried assets</div></div>
        <div class="card"><div class="val">{sprs.get('computed_score', '—')}</div><div class="lbl">Computed SPRS</div></div>
        <div class="card"><div class="val">{qa_count} / {oq_count}</div><div class="lbl">QA log / open questions</div></div>
      </div>
    </section>

    <section id="story">
      <h2>Organization story (test persona)</h2>
      <p>{esc(org.get('scope_narrative', ''))}</p>
      <p>{esc(org.get('environment_narrative', ''))}</p>
      <h3>Key roles</h3>
      <table>
        <tr><th>Role</th><th>Name</th><th>Responsibility</th></tr>
        {"".join(
            f"<tr><td>{esc(slug)}</td><td>{esc((r or {}).get('name',''))}</td>"
            f"<td>{esc(', '.join((r or {}).get('responsibilities') or [(r or {}).get('title','')]))}</td></tr>"
            for slug, r in (org.get('roles') or {}).items()
        )}
      </table>
      <h3>Representative gaps (for toolkit testing)</h3>
      <ul>
        <li><strong>AU.L2-3.3.5</strong> — not met, 5 SPRS points, <em>not</em> POA&amp;M-eligible (must fix or accept score hit)</li>
        <li><strong>CM.L2-3.4.7 / AC.L2-3.1.22</strong> — open POA&amp;M items on 1-point requirements</li>
        <li><strong>IA.L2-3.5.3</strong> — partially met (SMS OTP on one legacy app)</li>
        <li><strong>SC.L2-3.13.11</strong> — shared with GCC High CRM + customer Intune FIPS policy</li>
        <li><strong>ControlBot import</strong> — Terraform Checkov seed on SC-7 mapped via crosswalk</li>
        <li><strong>Discovery open questions</strong> — MFP scan relay, MSP NinjaOne alert path</li>
      </ul>
    </section>

    <section id="program-data">
      <h2>Program data tour</h2>
      <p>Source file: <a href="program-data.yaml"><code>program-data.yaml</code></a>
      (validates against <code>templates/program-data.schema.json</code>).</p>
      <table>
        <tr><th>Section</th><th>Demo content</th></tr>
        <tr><td><code>organization</code></td><td>APM identity, scope/environment narratives, five roles</td></tr>
        <tr><td><code>assessment</code></td><td>Level 2, C3PAO path, Nov 2026 target</td></tr>
        <tr><td><code>assets</code></td><td>All five 32 CFR 170.19(c) buckets with baseline profiles</td></tr>
        <tr><td><code>topology</code></td><td>Zones, nodes, CUI/SPD flows for diagram generators</td></tr>
        <tr><td><code>inheritance_sources</code></td><td>GCC High CRM/BoE reference (<code>id: gcch</code>)</td></tr>
        <tr><td><code>discovery</code></td><td>8+ phases touched, QA log, assumptions, open questions, decisions</td></tr>
        <tr><td><code>requirements</code></td><td>All 110 requirements — met / partial / inherited / POA&amp;M / not-met mix</td></tr>
        <tr><td><code>trust_center</code></td><td>Published attestations without internal paths</td></tr>
        <tr><td><code>controlbot_import</code></td><td>Stamp after <code>import_controlbot_seeds.py</code> run</td></tr>
      </table>
    </section>

    <section id="validation">
      <h2>Validation report</h2>
      <p>POA&amp;M validator:
        <span class="pill {'pill-ok' if validate_poam.get('valid') else 'pill-bad'}">
          {'PASS' if validate_poam.get('valid') else 'FAIL'}
        </span>
        computed SPRS <strong>{esc(validate_poam.get('computed_sprs_score', '—'))}</strong>,
        POA&amp;M items <strong>{esc(validate_poam.get('poam_item_count', '—'))}</strong>
      </p>
      <pre>{esc(json.dumps(validate_poam, indent=2)[:6000] if validate_poam else 'Run bootstrap to generate')}</pre>
      <h3>Discovery report</h3>
      <pre>{esc(discovery)}</pre>
    </section>

    <section id="artifacts">
      <h2>Generated artifacts</h2>
      <table>
        <tr><th>Artifact</th><th>Path</th><th>Purpose</th></tr>
        {"".join(artifact_row(n, p, d) for n, p, d in artifacts)}
      </table>
    </section>

    <section id="preview">
      <h2>Live preview</h2>
      <p>Internal dashboard (open <a href="outputs/dashboard.html">outputs/dashboard.html</a> for full screen):</p>
      <iframe src="outputs/dashboard.html" title="Demo dashboard"></iframe>
      <p>Public trust center:</p>
      <iframe src="outputs/trust-center.html" title="Demo trust center"></iframe>
    </section>

    <section id="routing">
      <h2>SKILL.md routing for this OSC</h2>
      <table>
        <tr><th>Question type</th><th>Read first</th><th>Why</th></tr>
        {"".join(
            f"<tr><td>{esc(a)}</td><td><code>{esc(b)}</code></td><td>{esc(c)}</td></tr>"
            for a, b, c in routing_rows
        )}
      </table>
    </section>

    <section id="scripts">
      <h2>Toolkit scripts exercised</h2>
      <table>
        <tr><th>Script</th><th>Role in demo</th></tr>
        {"".join(f"<tr><td><code>{esc(a)}</code></td><td>{esc(b)}</td></tr>" for a, b in script_rows)}
      </table>
    </section>

    <section id="evals">
      <h2>Eval scenarios to run with this persona</h2>
      <p>Prompt the advisor as Atlas Precision Manufacturing and score against:</p>
      <table>
        <tr><th>Scenario</th><th>Exercises</th></tr>
        {"".join(f"<tr><td><code>evals/scenarios/{esc(a)}</code></td><td>{esc(b)}</td></tr>" for a, b in eval_rows)}
      </table>
      <pre class="cmd">python -m evals.runner.runner evals/scenarios/modern-it-gcch-workbook-routing.yaml</pre>
    </section>

    <section id="commands">
      <h2>Regenerate everything</h2>
      <pre class="cmd">python3 scripts/bootstrap_demo_osc.py</pre>
      <pre class="cmd">python3 scripts/discovery_report.py examples/demo-osc/program-data.yaml
python3 scripts/validate_poam.py examples/demo-osc/program-data.yaml
python3 scripts/collect_evidence.py examples/demo-osc/program-data.yaml --list
python3 scripts/eval_routing_smoke.py</pre>
    </section>
  </main>
</body>
</html>
"""

    dest = demo_root / "DEMO-OSC-GUIDE.html"
    dest.write_text(page, encoding="utf-8")
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
