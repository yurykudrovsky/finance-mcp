import asyncio
from datetime import datetime, timezone
import yfinance as yf
from finance_mcp.models import NewsItem, NewsResult
from finance_mcp.cache import TTLCache

news_cache = TTLCache(ttl=900.0)  # 15 minutes


def _fetch_news(symbol: str, limit: int) -> NewsResult:
    ticker = yf.Ticker(symbol)
    raw = ticker.news or []
    items = []
    for entry in raw[:limit]:
        content = entry.get("content", {})
        title = content.get("title") or entry.get("title", "")
        url = (
            content.get("canonicalUrl", {}).get("url")
            or content.get("clickThroughUrl", {}).get("url")
            or entry.get("link", "")
        )
        pub_ts = content.get("pubDate") or entry.get("providerPublishTime")
        if isinstance(pub_ts, (int, float)):
            published_at = (
                datetime.fromtimestamp(pub_ts, tz=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
        elif isinstance(pub_ts, str):
            published_at = pub_ts
        else:
            published_at = ""
        if title:
            items.append(NewsItem(title=title, url=url, published_at=published_at))
    return NewsResult(symbol=symbol, items=items)


async def get_news(symbol: str, limit: int = 5) -> NewsResult:
    """Return recent news headlines for a stock symbol."""
    symbol = symbol.upper()
    cache_key = f"{symbol}:{limit}"
    cached = news_cache.get(cache_key)
    if cached is not None:
        from typing import cast

        return cast(NewsResult, cached)

    result = await asyncio.to_thread(_fetch_news, symbol, limit)
    news_cache.set(cache_key, result)
    return result
