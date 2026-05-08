import asyncio
from finance_mcp.server import run


def main() -> None:
    """Main entry point for the finance-mcp package."""
    asyncio.run(run())
