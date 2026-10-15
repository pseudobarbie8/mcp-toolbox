import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("files")
ROOT = Path(os.environ.get("FILES_ROOT", ".")).resolve()


def _safe(p: str) -> Path:
    path = (ROOT / p).resolve()
    if path != ROOT and ROOT not in path.parents:
        raise ValueError("path is outside the allowed folder")
    return path


@mcp.tool()
def search_files(query: str, folder: str = ".") -> list[str]:
    """Return paths of files whose names contain the query."""
    base = _safe(folder)
    hits = [p for p in base.rglob("*") if p.is_file() and query.lower() in p.name.lower()]
    return [str(p.relative_to(ROOT)) for p in hits[:50]]


@mcp.tool()
def read_file(path: str, max_chars: int = 5000) -> str:
    """Read the start of a text file."""
    return _safe(path).read_text(errors="replace")[:max_chars]


if __name__ == "__main__":
    mcp.run()
