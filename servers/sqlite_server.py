import os
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sqlite")
DB = os.environ.get("DB_PATH", "demo.db")


def _conn():
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)  # read-only connection


@mcp.tool()
def list_tables() -> list[str]:
    """List the tables in the database."""
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]


@mcp.tool()
def run_query(sql: str, limit: int = 100) -> list[dict]:
    """Run a single read-only SELECT query."""
    if not sql.strip().lower().startswith("select"):
        raise ValueError("only SELECT queries are allowed")
    with _conn() as c:
        cur = c.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchmany(limit)]


if __name__ == "__main__":
    mcp.run()
