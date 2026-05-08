import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from finance_mcp.tools.history import get_history


@pytest.mark.asyncio
@patch("finance_mcp.tools.history.yf.Ticker")
async def test_get_history(mock_ticker):
    mock_instance = MagicMock()
    # Create mock dataframe
    df = pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [102.0, 103.0],
            "Low": [99.0, 100.0],
            "Close": [101.0, 102.0],
            "Volume": [1000, 2000],
        },
        index=pd.to_datetime(["2023-01-01", "2023-01-02"]),
    )

    mock_instance.history.return_value = df
    mock_ticker.return_value = mock_instance

    history = await get_history("AAPL", "5d", "1d")

    assert history.symbol == "AAPL"
    assert len(history.data) == 2
    assert history.data[0].close == 101.0
    assert history.data[1].volume == 2000


@pytest.mark.asyncio
async def test_get_history_invalid_period():
    with pytest.raises(ValueError, match="Invalid period"):
        await get_history("AAPL", "invalid_period", "1d")
