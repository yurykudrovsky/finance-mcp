import asyncio
from finance_mcp.models import Quote
from finance_mcp.cache import quote_cache

from finance_mcp.provider import DataProvider


def _fetch_quote(symbol: str) -> Quote:
    # Synchronous function to be run in a thread
    return DataProvider.get_quote(symbol)


async def get_quote(symbol: str) -> Quote:
    """Get current price, change %, and volume for a given stock symbol."""
    symbol = symbol.upper()
    cached = quote_cache.get(symbol)
    from typing import cast

    if cached is not None:
        return cast(Quote, cached)

    quote = await asyncio.to_thread(_fetch_quote, symbol)
    quote_cache.set(symbol, quote)
    return quote
