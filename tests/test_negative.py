"""Negative / error-path tests for all tools and DataProvider."""

import asyncio
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pandas as pd
import pytest

from finance_mcp.cache import fundamentals_cache, quote_cache
from finance_mcp.tools.fundamentals import get_fundamentals
from finance_mcp.tools.history import get_history
from finance_mcp.tools.indicators import calc_indicators
from finance_mcp.tools.news import get_news, news_cache
from finance_mcp.tools.quote import get_quote


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_caches() -> None:
    quote_cache._cache.clear()
    fundamentals_cache._cache.clear()
    news_cache._cache.clear()


# ---------------------------------------------------------------------------
# get_quote — invalid / edge-case symbols
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_empty_symbol(mock_ticker: MagicMock) -> None:
    """Empty string — yfinance returns no data, fallback also fails."""
    mock_ticker.return_value.fast_info = {}
    with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
        await get_quote("")


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_special_chars_symbol(mock_ticker: MagicMock) -> None:
    """Special chars — yfinance returns no data, fallback also fails."""
    mock_ticker.return_value.fast_info = {}
    with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
        await get_quote("123!@#")


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_very_long_symbol(mock_ticker: MagicMock) -> None:
    """Very long symbol — treated same as an invalid ticker."""
    mock_ticker.return_value.fast_info = {}
    with pytest.raises(ValueError):
        await get_quote("A" * 200)


# ---------------------------------------------------------------------------
# get_quote — network / provider failures
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_yfinance_network_timeout(mock_ticker: MagicMock) -> None:
    """OSError from yfinance triggers AV fallback; AV also fails → ValueError."""
    mock_ticker.side_effect = OSError("Connection timed out")
    with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
        await get_quote("AAPL")


@pytest.mark.asyncio
@patch("finance_mcp.provider.httpx.Client")
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_alphavantage_fallback_success(
    mock_yf_ticker: MagicMock,
    mock_httpx_client_cls: MagicMock,
) -> None:
    """yfinance fails → Alpha Vantage fallback returns a valid quote."""
    mock_yf_ticker.return_value.fast_info = {}

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Global Quote": {
            "05. price": "150.00",
            "10. change percent": "1.5%",
            "06. volume": "1000000",
        }
    }
    mock_response.raise_for_status = MagicMock()
    mock_httpx_client_cls.return_value.__enter__.return_value.get.return_value = (
        mock_response
    )

    import os

    with patch.dict(os.environ, {"ALPHA_VANTAGE_API_KEY": "test-key"}):
        quote = await get_quote("AAPL")

    assert quote.symbol == "AAPL"
    assert quote.price == 150.0
    assert quote.change_percent == 1.5
    assert quote.volume == 1000000


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_alphavantage_missing_api_key(mock_ticker: MagicMock) -> None:
    """yfinance fails + no AV key → ValueError about missing key."""
    mock_ticker.return_value.fast_info = {}

    import os

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
            await get_quote("AAPL")


@pytest.mark.asyncio
@patch("finance_mcp.provider.httpx.Client")
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_alphavantage_rate_limit_429(
    mock_yf_ticker: MagicMock,
    mock_httpx_client_cls: MagicMock,
) -> None:
    """yfinance fails → AV returns 429 → ValueError propagated."""
    mock_yf_ticker.return_value.fast_info = {}

    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "429 Too Many Requests",
        request=MagicMock(),
        response=mock_response,
    )
    mock_httpx_client_cls.return_value.__enter__.return_value.get.return_value = (
        mock_response
    )

    import os

    with patch.dict(os.environ, {"ALPHA_VANTAGE_API_KEY": "test-key"}):
        with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
            await get_quote("AAPL")


# ---------------------------------------------------------------------------
# get_quote — TTL cache concurrency
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_concurrent_cache_hit(mock_ticker: MagicMock) -> None:
    """Two concurrent get_quote calls for the same symbol yield identical results.

    Due to the async+thread model, yfinance may be called once or twice before
    the cache is warm, but a subsequent serial call must always hit the cache.
    """
    mock_ticker.return_value.fast_info = {
        "lastPrice": 150.0,
        "previousClose": 145.0,
        "lastVolume": 1_000_000,
    }

    r1, r2 = await asyncio.gather(get_quote("AAPL"), get_quote("AAPL"))
    assert r1.price == r2.price == 150.0

    # Third call must use cache (ticker not called again)
    call_count_after_concurrent = mock_ticker.call_count
    await get_quote("AAPL")
    assert mock_ticker.call_count == call_count_after_concurrent


# ---------------------------------------------------------------------------
# get_history — edge cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.tools.history.yf.Ticker")
async def test_get_history_empty_dataframe(mock_ticker: MagicMock) -> None:
    """yfinance returns empty DataFrame for an unknown symbol."""
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    with pytest.raises(ValueError, match="No history data found"):
        await get_history("ZZZZ", "5d", "1d")


# ---------------------------------------------------------------------------
# get_fundamentals — malformed data
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.tools.fundamentals.yf.Ticker")
async def test_get_fundamentals_invalid_symbol(mock_ticker: MagicMock) -> None:
    """yfinance returns empty info dict → ValueError."""
    mock_ticker.return_value.info = {}
    with pytest.raises(ValueError, match="Invalid symbol or no data available"):
        await get_fundamentals("ZZZZ")


# ---------------------------------------------------------------------------
# calc_indicators — no data
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.tools.indicators.yf.Ticker")
async def test_calc_indicators_empty_history(mock_ticker: MagicMock) -> None:
    """yfinance returns empty DataFrame for indicator calc."""
    mock_ticker.return_value.history.return_value = pd.DataFrame()
    with pytest.raises(ValueError, match="No history data found"):
        await calc_indicators("ZZZZ", "RSI")


# ---------------------------------------------------------------------------
# get_news — malformed / missing fields
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_malformed_entries_skipped(mock_ticker: MagicMock) -> None:
    """Entries with no title are silently skipped; valid ones are returned."""
    raw: list[dict[str, Any]] = [
        # valid new-format entry
        {
            "content": {
                "title": "Valid headline",
                "canonicalUrl": {"url": "https://example.com/a"},
                "pubDate": "2024-01-15T10:00:00Z",
            }
        },
        # malformed: no title anywhere
        {"content": {}},
        # malformed: completely empty
        {},
    ]
    mock_ticker.return_value.news = raw

    result = await get_news("AAPL", limit=5)

    assert len(result.items) == 1
    assert result.items[0].title == "Valid headline"


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_none_news_attr(mock_ticker: MagicMock) -> None:
    """ticker.news returning None is handled gracefully."""
    mock_ticker.return_value.news = None

    result = await get_news("AAPL", limit=5)

    assert result.items == []
