#!/usr/bin/env python3
"""Generate network and CUI flow diagrams from the program data topology.

Reads the `topology` section of a program data file
(templates/program-data.schema.json) and emits the two diagrams the SSP
and scoping guides require, in two formats each:

- Mermaid sources (network.mmd, cui-flow.mmd) for GitHub rendering and
  editing in diagram tools
- Self-contained SVGs (network.svg, cui-flow.svg) from a deterministic
  layered layout: zones as containers, the CMMC Assessment Scope as a
  dashed boundary, nodes labeled with their 32 CFR 170.19(c) asset
  category, CUI flows emphasized

Usage (from repo root):
    python3 scripts/generate_diagrams.py path/to/program-data.yaml -o diagrams/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# fixed light styling so the SVGs print and paste into documents cleanly
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#c9c8c0"
SURFACE = "#fcfcfb"
ZONE_BG = "#f4f3ef"
CUI_EDGE = "#0b0b0b"
OTHER_EDGE = "#898781"
CATEGORY = {
    "cui": ("CUI asset", "#0ca30c"),
    "security-protection": ("Security Protection", "#2f6fb2"),
    "contractor-risk-managed": ("Contractor Risk Managed", "#b28419"),
    "specialized": ("Specialized", "#ec835a"),
    "out-of-scope": ("Out of scope", "#898781"),
}
ROLE_SHAPE = {"entity": "rect", "process": "round", "store": "store"}

NODE_W, NODE_H, GAP_Y, ZONE_PAD, ZONE_GAP = 190, 58, 26, 26, 60
TITLE_H = 34


def esc(s) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def layout(topology: dict, only_nodes: set | None = None):
    """Column per zone, nodes stacked; returns geometry dicts."""
    zones = topology.get("zones", [])
    nodes = [n for n in topology.get("nodes", [])
             if only_nodes is None or n["id"] in only_nodes]
    by_zone = {}
    for n in nodes:
        by_zone.setdefault(n.get("zone"), []).append(n)
    # keep cmmc-scope zones adjacent so one dashed boundary can wrap them
    zones = sorted(zones, key=lambda z: 0 if z.get("boundary") == "cmmc-scope" else 1)
    zones = [z for z in zones if by_zone.get(z["id"])]

    zgeo, ngeo = {}, {}
    x = 20
    max_h = 0
    for z in zones:
        zn = by_zone.get(z["id"], [])
        h = TITLE_H + ZONE_PAD + len(zn) * (NODE_H + GAP_Y) - GAP_Y + ZONE_PAD
        w = NODE_W + 2 * ZONE_PAD
        zgeo[z["id"]] = {"x": x, "y": 20, "w": w, "h": h, "zone": z}
        y = 20 + TITLE_H + ZONE_PAD
        for n in zn:
            ngeo[n["id"]] = {"x": x + ZONE_PAD, "y": y, "node": n, "zone": z["id"]}
            y += NODE_H + GAP_Y
        x += w + ZONE_GAP
        max_h = max(max_h, h)
    width = x - ZONE_GAP + 20
    height = max_h + 80
    return zones, zgeo, ngeo, width, height


def node_svg(g: dict) -> str:
    n, x, y = g["node"], g["x"], g["y"]
    cat_label, cat_color = CATEGORY.get(n.get("category", "cui"), CATEGORY["cui"])
    role = ROLE_SHAPE.get(n.get("role", "process"), "round")
    rx = 10 if role == "round" else 0
    parts = []
    if role == "store":  # classic DFD store: top and bottom rules only
        parts.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" fill="{SURFACE}"/>')
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x + NODE_W}" y2="{y}" stroke="{INK}" stroke-width="1.4"/>')
        parts.append(f'<line x1="{x}" y1="{y + NODE_H}" x2="{x + NODE_W}" y2="{y + NODE_H}" stroke="{INK}" stroke-width="1.4"/>')
    else:
        parts.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="{rx}" '
                     f'fill="{SURFACE}" stroke="{GRID}" stroke-width="1"/>')
    parts.append(f'<rect x="{x}" y="{y}" width="4" height="{NODE_H}" fill="{cat_color}"/>')
    parts.append(f'<text x="{x + 14}" y="{y + 24}" font-size="13" font-weight="600" fill="{INK}">{esc(n.get("label", n["id"]))}</text>')
    parts.append(f'<text x="{x + 14}" y="{y + 43}" font-size="11" fill="{INK2}">{esc(cat_label)}</text>')
    return "".join(parts)


def edge_svg(fg: dict, tg: dict, flow: dict, emphasize_cui: bool) -> str:
    fx, fy = fg["x"], fg["y"] + NODE_H / 2
    tx, ty = tg["x"], tg["y"] + NODE_H / 2
    if fg["x"] < tg["x"]:
        x1, x2 = fx + NODE_W, tx
    elif fg["x"] > tg["x"]:
        x1, x2 = fx, tx + NODE_W
    else:  # same column: bow out to the right
        x1 = x2 = fx + NODE_W
    data = flow.get("data", "other")
    is_cui = data in ("cui", "fci")
    color = CUI_EDGE if (is_cui and emphasize_cui) else OTHER_EDGE
    width = 2.4 if (is_cui and emphasize_cui) else 1.4
    mid_x, mid_y = (x1 + x2) / 2, (fy + ty) / 2
    if x1 == x2:  # loop bow
        bow = x1 + 46
        path = f'M {x1} {fy} C {bow} {fy}, {bow} {ty}, {x2} {ty}'
        mid_x, mid_y = bow, (fy + ty) / 2
    else:
        path = f'M {x1} {fy} C {mid_x} {fy}, {mid_x} {ty}, {x2} {ty}'
    marker = "arrow-cui" if (is_cui and emphasize_cui) else "arrow"
    label = flow.get("label") or data.upper()
    tag = data.upper() if data != "other" else ""
    text = f"{tag} {label}".strip() if label != data.upper() else label
    lw = max(38, 7 * len(text) + 10)
    path_svg = f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"/>'
    label_parts = [f'<rect x="{mid_x - lw / 2}" y="{mid_y - 10}" width="{lw}" height="16" fill="{SURFACE}" opacity="0.92" stroke="{GRID}" stroke-width="0.5"/>']
    label_parts.append(f'<text x="{mid_x}" y="{mid_y + 2}" font-size="10.5" text-anchor="middle" fill="{INK2}">{esc(text)}</text>')
    if flow.get("bidirectional"):
        label_parts.append(f'<text x="{mid_x}" y="{mid_y + 14}" font-size="9" text-anchor="middle" fill="{MUTED}">(bidirectional)</text>')
    return path_svg, "".join(label_parts)


def build_svg(program: dict, mode: str) -> str:
    """mode: 'network' (all nodes and flows) or 'cui-flow' (DFD of CUI/FCI/SPD flows)."""
    topo = program.get("topology") or {}
    flows = topo.get("flows", [])
    if mode == "cui-flow":
        flows = [f for f in flows if f.get("data") in ("cui", "fci", "spd")]
        keep = {f.get("from") for f in flows} | {f.get("to") for f in flows}
        keep.discard(None)
    else:
        keep = None
    zones, zgeo, ngeo, width, height = layout(topo, keep)
    if not ngeo:
        sys.exit(f"topology has no nodes for the {mode} diagram")

    title = ("CUI Flow Diagram" if mode == "cui-flow" else "Network Diagram")
    org = (program.get("organization") or {}).get("system_name", "")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="-apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
        '<defs>'
        f'<marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
        f'<path d="M0,0 L9,4.5 L0,9 z" fill="{OTHER_EDGE}"/></marker>'
        f'<marker id="arrow-cui" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{CUI_EDGE}"/></marker>'
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="{SURFACE}"/>',
    ]
    # CMMC scope boundary around scope zones
    scope = [g for g in zgeo.values() if g["zone"].get("boundary") == "cmmc-scope"]
    if scope:
        x0 = min(g["x"] for g in scope) - 10
        y0 = min(g["y"] for g in scope) - 10
        x1 = max(g["x"] + g["w"] for g in scope) + 10
        y1 = max(g["y"] + g["h"] for g in scope) + 10
        parts.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="12" fill="none" '
                     f'stroke="{INK}" stroke-width="1.6" stroke-dasharray="8 5"/>')
        parts.append(f'<text x="{x0 + 10}" y="{y1 + 18}" font-size="11.5" font-weight="600" fill="{INK}">CMMC Assessment Scope</text>')
    for g in zgeo.values():
        z = g["zone"]
        fed = ' · FedRAMP' if z.get("boundary") == "fedramp" else ""
        parts.append(f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="8" '
                     f'fill="{ZONE_BG}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(f'<text x="{g["x"] + 12}" y="{g["y"] + 22}" font-size="12" font-weight="650" '
                     f'fill="{INK}">{esc(z.get("label", z["id"]))}<tspan fill="{MUTED}" font-weight="400">{esc(fed)}</tspan></text>')
    edge_paths, edge_labels = [], []
    for f in flows:
        fg, tg = ngeo.get(f.get("from")), ngeo.get(f.get("to"))
        if fg and tg:
            path_svg, label_svg = edge_svg(fg, tg, f, emphasize_cui=True)
            edge_paths.append(path_svg)
            edge_labels.append(label_svg)
    parts.extend(edge_paths)
    for g in ngeo.values():
        parts.append(node_svg(g))
    parts.extend(edge_labels)
    foot = f'{esc(org)} · {title} · generated from program data; keep synchronized with the SSP'
    parts.append(f'<text x="20" y="{height - 12}" font-size="10.5" fill="{MUTED}">{foot}</text>')
    parts.append("</svg>")
    return "".join(parts)


def build_mermaid(program: dict, mode: str) -> str:
    topo = program.get("topology") or {}
    flows = topo.get("flows", [])
    if mode == "cui-flow":
        flows = [f for f in flows if f.get("data") in ("cui", "fci", "spd")]
        keep = {f.get("from") for f in flows} | {f.get("to") for f in flows}
        keep.discard(None)
    else:
        keep = None
    lines = ["flowchart LR"]
    for z in topo.get("zones", []):
        zn = [n for n in topo.get("nodes", []) if n.get("zone") == z["id"]
              and (keep is None or n["id"] in keep)]
        if not zn:
            continue
        scope_tag = " [CMMC scope]" if z.get("boundary") == "cmmc-scope" else ""
        lines.append(f'  subgraph {z["id"]}["{z.get("label", z["id"])}{scope_tag}"]')
        for n in zn:
            cat = CATEGORY.get(n.get("category", "cui"), CATEGORY["cui"])[0]
            label = f'{n.get("label", n["id"])}<br/><i>{cat}</i>'
            if n.get("role") == "store":
                lines.append(f'    {n["id"]}[("{label}")]')
            elif n.get("role") == "entity":
                lines.append(f'    {n["id"]}["{label}"]')
            else:
                lines.append(f'    {n["id"]}("{label}")')
        lines.append("  end")
    for f in flows:
        label = f.get("label") or ""
        tag = f.get("data", "other").upper()
        text = f"{tag}: {label}" if label else tag
        cui = f.get("data") in ("cui", "fci")
        if f.get("bidirectional"):
            link = "<==>" if cui else "<-->"
        else:
            link = "==>" if cui else "-->"
        src, dst = f.get("from"), f.get("to")
        if not src or not dst:
            continue
        lines.append(f'  {src} {link}|"{text}"| {dst}')
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SSP diagrams from program data topology")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out-dir", type=Path, default=Path("diagrams"))
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data must parse to a mapping (YAML or JSON object)")
    if not program.get("topology"):
        sys.exit("no topology section in the program data file; see templates/program-data.schema.json")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for mode, stem in (("network", "network"), ("cui-flow", "cui-flow")):
        svg = build_svg(program, mode)
        (args.out_dir / f"{stem}.svg").write_text(svg, encoding="utf-8")
        mmd = build_mermaid(program, mode)
        (args.out_dir / f"{stem}.mmd").write_text(mmd, encoding="utf-8")
        print(f"wrote {args.out_dir / stem}.svg and .mmd")
    print("Embed the SVGs in the SSP (Figures: network diagram, CUI flow diagram) "
          "and keep them synchronized with the asset inventory and boundary prose.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
