import asyncio
import yfinance as yf
import pandas as pd
from finance_mcp.models import Indicators, IndicatorData


def _calculate_sma(df: pd.DataFrame, window: int) -> list[IndicatorData]:
    sma = df["Close"].rolling(window=window).mean()
    sma = sma.dropna()
    return [IndicatorData(date=str(idx), value=float(val)) for idx, val in sma.items()]


def _calculate_rsi(df: pd.DataFrame, periods: int = 14) -> list[IndicatorData]:
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.dropna()
    return [IndicatorData(date=str(idx), value=float(val)) for idx, val in rsi.items()]


def _calculate_macd(df: pd.DataFrame) -> list[IndicatorData]:
    exp1 = df["Close"].ewm(span=12, adjust=False).mean()
    exp2 = df["Close"].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    macd = macd.dropna()
    return [IndicatorData(date=str(idx), value=float(val)) for idx, val in macd.items()]


def _calc_indicators(symbol: str, indicator: str) -> Indicators:
    valid_indicators = ["SMA20", "SMA50", "SMA200", "RSI", "MACD"]
    indicator = indicator.upper()
    if indicator not in valid_indicators:
        raise ValueError(
            f"Invalid indicator '{indicator}'. Must be one of {valid_indicators}"
        )

    ticker = yf.Ticker(symbol)
    period = "1y"  # default period for indicators
    if indicator == "SMA200":
        period = "2y"
    df = ticker.history(period=period, interval="1d")

    if df.empty:
        raise ValueError(f"No history data found for {symbol} to calculate {indicator}")

    data = []
    if indicator == "SMA20":
        data = _calculate_sma(df, 20)
    elif indicator == "SMA50":
        data = _calculate_sma(df, 50)
    elif indicator == "SMA200":
        data = _calculate_sma(df, 200)
    elif indicator == "RSI":
        data = _calculate_rsi(df)
    elif indicator == "MACD":
        data = _calculate_macd(df)

    return Indicators(symbol=symbol.upper(), indicator=indicator, data=data)


async def calc_indicators(symbol: str, indicator: str) -> Indicators:
    """Calculate technical indicators like RSI, MACD, SMA(20/50/200)."""
    return await asyncio.to_thread(_calc_indicators, symbol, indicator)
