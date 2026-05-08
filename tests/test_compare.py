import pytest
from unittest.mock import patch, MagicMock
from finance_mcp.tools.compare import compare_stocks
from finance_mcp.models import Quote, Fundamentals


@pytest.mark.asyncio
@patch("finance_mcp.tools.compare.get_fundamentals")
@patch("finance_mcp.tools.compare.get_quote")
async def test_compare_stocks(
    mock_get_quote: MagicMock, mock_get_fundamentals: MagicMock
) -> None:
    mock_get_quote.side_effect = lambda sym: Quote(
        symbol=sym.upper(), price=150.0, change_percent=1.5, volume=100
    )
    mock_get_fundamentals.side_effect = lambda sym: Fundamentals(
        symbol=sym.upper(),
        pe_ratio=20.0,
        market_cap=2000,
        dividend_yield=0.01,
        sector="Tech",
    )

    comp = await compare_stocks(["AAPL", "MSFT"])

    assert "AAPL" in comp.metrics
    assert "MSFT" in comp.metrics

    assert comp.metrics["AAPL"].price == 150.0
    assert comp.metrics["MSFT"].pe_ratio == 20.0


@pytest.mark.asyncio
async def test_compare_stocks_empty() -> None:
    with pytest.raises(ValueError, match="Must provide at least one symbol"):
        await compare_stocks([])
