from typing import Any

import pytest
from unittest.mock import patch, MagicMock
from finance_mcp.tools.news import get_news, news_cache


@pytest.fixture(autouse=True)
def clear_cache() -> None:
    news_cache._cache.clear()


def _make_ticker(raw_news: list[dict[str, Any]]) -> MagicMock:
    mock_ticker: MagicMock = MagicMock()
    mock_ticker.news = raw_news
    return mock_ticker


NEW_FORMAT_NEWS: list[dict[str, Any]] = [
    {
        "content": {
            "title": "AAPL hits record high",
            "canonicalUrl": {"url": "https://example.com/aapl-record"},
            "pubDate": "2024-01-15T10:30:00Z",
        }
    },
    {
        "content": {
            "title": "Apple Vision Pro review",
            "canonicalUrl": {"url": "https://example.com/vision-pro"},
            "pubDate": "2024-01-14T08:00:00Z",
        }
    },
]

LEGACY_FORMAT_NEWS: list[dict[str, Any]] = [
    {
        "title": "Old format headline",
        "link": "https://example.com/old",
        "providerPublishTime": 1705312200,
    }
]


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_new_format(mock_ticker_cls: MagicMock) -> None:
    mock_ticker_cls.return_value = _make_ticker(NEW_FORMAT_NEWS)

    result = await get_news("AAPL", limit=5)

    assert result.symbol == "AAPL"
    assert len(result.items) == 2
    assert result.items[0].title == "AAPL hits record high"
    assert result.items[0].url == "https://example.com/aapl-record"
    assert result.items[0].published_at == "2024-01-15T10:30:00Z"


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_legacy_format(mock_ticker_cls: MagicMock) -> None:
    mock_ticker_cls.return_value = _make_ticker(LEGACY_FORMAT_NEWS)

    result = await get_news("MSFT", limit=5)

    assert result.symbol == "MSFT"
    assert len(result.items) == 1
    assert result.items[0].title == "Old format headline"
    assert result.items[0].url == "https://example.com/old"
    assert "2024-01-15" in result.items[0].published_at


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_limit(mock_ticker_cls: MagicMock) -> None:
    mock_ticker_cls.return_value = _make_ticker(NEW_FORMAT_NEWS)

    result = await get_news("AAPL", limit=1)

    assert len(result.items) == 1


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_empty(mock_ticker_cls: MagicMock) -> None:
    mock_ticker_cls.return_value = _make_ticker([])

    result = await get_news("FAKE", limit=5)

    assert result.symbol == "FAKE"
    assert result.items == []


@pytest.mark.asyncio
@patch("finance_mcp.tools.news.yf.Ticker")
async def test_get_news_caching(mock_ticker_cls: MagicMock) -> None:
    mock_ticker_cls.return_value = _make_ticker(NEW_FORMAT_NEWS)

    result1 = await get_news("AAPL", limit=5)
    result2 = await get_news("AAPL", limit=5)

    assert result1.items[0].title == result2.items[0].title
    mock_ticker_cls.assert_called_once()  # second call hits cache
