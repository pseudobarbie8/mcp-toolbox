# mcp-toolbox

A few Model Context Protocol servers that give an LLM real tools.

```bash
pip install -r requirements.txt
python servers/files_server.py      # search local files
python servers/sqlite_server.py     # read-only SQL over a database
python servers/web_server.py        # fetch and clean a web page
```

Minimal server:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("files")

@mcp.tool()
def search_files(query: str, folder: str = ".") -> list[str]:
    """Return paths of files whose names contain the query."""
    ...

if __name__ == "__main__":
    mcp.run()
```

## Connecting a client

Add to your MCP client config:

```json
{"mcpServers": {"files": {"command": "python", "args": ["servers/files_server.py"]}}}
```

## Servers

| Server | Tools |
|---|---|
| files | `search_files`, `read_file` |
| sqlite | `list_tables`, `run_query` (SELECT only) |
| web | `fetch_page` |

`demo/` has a short script showing a client calling each one.

MIT
