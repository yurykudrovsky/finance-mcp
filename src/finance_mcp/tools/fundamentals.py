import asyncio
import yfinance as yf
from finance_mcp.models import Fundamentals
from finance_mcp.cache import fundamentals_cache


def _fetch_fundamentals(symbol: str) -> Fundamentals:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    if not info or "symbol" not in info:
        raise ValueError(f"Invalid symbol or no data available for {symbol}")

    return Fundamentals(
        symbol=symbol.upper(),
        pe_ratio=info.get("trailingPE"),
        market_cap=info.get("marketCap"),
        dividend_yield=info.get("dividendYield"),
        sector=info.get("sector"),
    )


async def get_fundamentals(symbol: str) -> Fundamentals:
    """Get fundamental data for a given stock symbol."""
    symbol = symbol.upper()
    cached = fundamentals_cache.get(symbol)
    from typing import cast

    if cached is not None:
        return cast(Fundamentals, cached)

    funds = await asyncio.to_thread(_fetch_fundamentals, symbol)
    fundamentals_cache.set(symbol, funds)
    return funds
