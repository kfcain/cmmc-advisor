# CMMC Advisor MCP server

Local stdio MCP server for program-data read/write and GRC snapshot import.
**Does not** replace vendor MCP servers (Vanta, Drata, Secureframe, Paramify).

## Install

```bash
pip install -r scripts/mcp/requirements.txt
```

## Configure (Cursor / Claude Code / Codex)

Add alongside vendor GRC MCP servers. See `platforms/toolkit/mcp.json` for a combined template.

```json
{
  "mcpServers": {
    "cmmc-advisor": {
      "command": "python3",
      "args": ["scripts/mcp/cmmc_advisor_server.py"],
      "cwd": "/path/to/.cmmc-advisor",
      "env": {
        "CMMC_PROGRAM_DATA": "/path/to/your/compliance-repo/program-data.yaml"
      }
    }
  }
}
```

## Tools

| Tool | Purpose |
|------|---------|
| `list_grc_platforms` | Manifest of vendor MCP endpoints |
| `map_controls_to_cmmc` | 800-53 → CMMC requirement mapping |
| `import_grc_snapshot` | Merge normalized GRC JSON into program data |
| `read_program_summary` | Org, assessment, SPRS, integration metadata |
| `validate_poam` | 32 CFR 170.21 POA&M rules |
| `export_sprs` | SPRS scoresheet export |
| `get_grc_integration_workflow` | Step-by-step multi-MCP workflow per platform |

## Test

```bash
python3 scripts/import_grc_snapshot.py templates/grc-snapshot.sample.json templates/program-data.sample.yaml --dry-run
```
