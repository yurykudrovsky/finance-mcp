import pytest
from unittest.mock import patch, MagicMock
from finance_mcp.tools.fundamentals import get_fundamentals
from finance_mcp.cache import fundamentals_cache


@pytest.fixture(autouse=True)
def clear_cache():
    fundamentals_cache._cache.clear()


@pytest.mark.asyncio
@patch("finance_mcp.tools.fundamentals.yf.Ticker")
async def test_get_fundamentals(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.info = {
        "symbol": "AAPL",
        "trailingPE": 25.5,
        "marketCap": 2500000000000,
        "dividendYield": 0.005,
        "sector": "Technology",
    }
    mock_ticker.return_value = mock_instance

    funds = await get_fundamentals("AAPL")

    assert funds.symbol == "AAPL"
    assert funds.pe_ratio == 25.5
    assert funds.market_cap == 2500000000000
    assert funds.dividend_yield == 0.005
    assert funds.sector == "Technology"
