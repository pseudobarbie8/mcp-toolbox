"""Call each server's tools through the MCP protocol (no LLM involved).
Run from the repo root: python demo/make_db.py && python demo/client.py"""
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call(script, tool, args):
    params = StdioServerParameters(command=sys.executable, args=[script])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, args)
            print(f"{script} -> {tool}({args})")
            for item in result.content:
                print("  ", item.text[:300])


async def main():
    await call("servers/files_server.py", "search_files", {"query": "readme"})
    await call("servers/sqlite_server.py", "list_tables", {})
    await call("servers/sqlite_server.py", "run_query", {"sql": "SELECT * FROM cities WHERE country = 'Morocco'"})
    await call("servers/web_server.py", "fetch_page", {"url": "https://example.com"})


asyncio.run(main())
