import pytest
from unittest.mock import patch, MagicMock
from finance_mcp.tools.quote import get_quote
from finance_mcp.cache import quote_cache


@pytest.fixture(autouse=True)
def clear_cache():
    quote_cache._cache.clear()


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote(mock_ticker):
    # Setup mock
    mock_instance = MagicMock()
    mock_instance.fast_info = {
        "lastPrice": 150.0,
        "previousClose": 145.0,
        "lastVolume": 1000000,
    }
    mock_ticker.return_value = mock_instance

    quote = await get_quote("AAPL")

    assert quote.symbol == "AAPL"
    assert quote.price == 150.0
    assert quote.change_percent == round(((150.0 - 145.0) / 145.0) * 100, 2)
    assert quote.volume == 1000000

    # Test caching
    quote2 = await get_quote("AAPL")
    assert quote2.price == 150.0
    mock_ticker.assert_called_once()  # Should only be called once because of cache


@pytest.mark.asyncio
@patch("finance_mcp.provider.yf.Ticker")
async def test_get_quote_invalid_symbol(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.fast_info = {}  # Empty info implies invalid ticker
    mock_ticker.return_value = mock_instance

    with pytest.raises(ValueError, match="Both yfinance and Alpha Vantage failed"):
        await get_quote("INVALID")
