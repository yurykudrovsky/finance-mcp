import asyncio
from finance_mcp.models import Comparison, Metrics
from finance_mcp.tools.quote import get_quote
from finance_mcp.tools.fundamentals import get_fundamentals


async def compare_stocks(symbols: list[str]) -> Comparison:
    """Compare multiple stock symbols and return side-by-side metrics."""
    if not symbols:
        raise ValueError("Must provide at least one symbol")

    metrics_dict = {}

    async def fetch_for_symbol(sym: str) -> tuple[str, Metrics]:
        try:
            quote, funds = await asyncio.gather(get_quote(sym), get_fundamentals(sym))
            return sym, Metrics(
                price=quote.price,
                pe_ratio=funds.pe_ratio,
                market_cap=funds.market_cap,
                change_percent=quote.change_percent,
            )
        except Exception:
            return sym, Metrics()

    results = await asyncio.gather(*[fetch_for_symbol(sym) for sym in symbols])

    for sym, metric in results:
        metrics_dict[sym.upper()] = metric

    return Comparison(symbols=[s.upper() for s in symbols], metrics=metrics_dict)
