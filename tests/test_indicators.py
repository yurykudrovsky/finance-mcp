import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from finance_mcp.tools.indicators import calc_indicators


@pytest.mark.asyncio
@patch("finance_mcp.tools.indicators.yf.Ticker")
async def test_calc_indicators(mock_ticker):
    mock_instance = MagicMock()
    # Create mock dataframe with enough data for SMA20
    dates = pd.date_range(start="2023-01-01", periods=30)
    df = pd.DataFrame(
        {
            "Close": range(100, 130),
        },
        index=dates,
    )

    mock_instance.history.return_value = df
    mock_ticker.return_value = mock_instance

    ind = await calc_indicators("AAPL", "SMA20")

    assert ind.symbol == "AAPL"
    assert ind.indicator == "SMA20"
    # 30 periods - 19 periods of NaN = 11 values
    assert len(ind.data) == 11


@pytest.mark.asyncio
async def test_calc_indicators_invalid():
    with pytest.raises(ValueError, match="Invalid indicator"):
        await calc_indicators("AAPL", "INVALID")
