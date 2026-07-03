# Toolkit MCP configuration

Combined MCP template for a **compliance program repository** that submodules
cmmc-advisor at `.cmmc-advisor/`.

## Files

| File | Purpose |
|------|---------|
| `mcp.json` | Vendor GRC MCPs + local cmmc-advisor MCP |
| `../cursor/` | Cursor skill/rule install |
| `../../scripts/mcp/` | cmmc-advisor MCP server |

## Setup

1. Copy `mcp.json` into your MCP client config (or merge `mcpServers` block).
2. Set `CMMC_PROGRAM_DATA` to your `program-data.yaml` path.
3. Complete OAuth for Vanta/Drata in the client.
4. Set Secureframe API env vars if used.
5. Configure Paramify workspace URL + API key separately (see Paramify plugin docs).

Workflow: `references/grc/grc-platform-mcp-bridge.md`
