import asyncio
import yfinance as yf
from finance_mcp.models import History, OHLCV


def _fetch_history(symbol: str, period: str, interval: str) -> History:
    valid_periods = [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]
    if period not in valid_periods:
        raise ValueError(f"Invalid period '{period}'. Must be one of {valid_periods}")

    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)

    if df.empty:
        raise ValueError(
            f"No history data found for {symbol} (period={period}, interval={interval})"
        )

    data = []
    for date, row in df.iterrows():
        data.append(
            OHLCV(
                date=str(date),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
            )
        )

    return History(symbol=symbol.upper(), data=data)


async def get_history(symbol: str, period: str, interval: str) -> History:
    """Get historical OHLCV data for a given stock symbol."""
    return await asyncio.to_thread(_fetch_history, symbol, period, interval)
