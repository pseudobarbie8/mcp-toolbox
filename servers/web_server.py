import re

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web")


@mcp.tool()
def fetch_page(url: str, max_chars: int = 5000) -> str:
    """Fetch a web page and return its text with tags stripped."""
    if not url.startswith(("http://", "https://")):
        raise ValueError("only http(s) URLs are allowed")
    html = httpx.get(url, timeout=15, follow_redirects=True).text
    html = re.sub(r"(?s)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()[:max_chars]


if __name__ == "__main__":
    mcp.run()
