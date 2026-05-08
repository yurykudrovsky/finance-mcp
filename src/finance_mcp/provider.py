import os
import httpx
import yfinance as yf
from finance_mcp.models import Quote
from dotenv import load_dotenv

load_dotenv()

# Expected runtime failures from yfinance (uses requests internally):
#   ValueError/KeyError  – bad symbol or missing data fields
#   AttributeError       – yfinance object attribute missing
#   OSError              – covers requests.exceptions.ConnectionError /
#                          Timeout which both ultimately subclass OSError
_YFINANCE_ERRORS = (ValueError, KeyError, AttributeError, OSError)

# Expected runtime failures from the httpx-based Alpha Vantage call:
_AV_ERRORS = (ValueError, KeyError, httpx.RequestError, httpx.HTTPStatusError)


class DataProvider:
    @staticmethod
    def get_quote(symbol: str) -> Quote:
        """Fetch quote using yfinance, fallback to Alpha Vantage."""
        try:
            return DataProvider._get_quote_yfinance(symbol)
        except _YFINANCE_ERRORS as e_yf:
            print(
                f"yfinance failed for {symbol}: {e_yf}. Falling back to Alpha Vantage..."
            )
            try:
                return DataProvider._get_quote_alphavantage(symbol)
            except _AV_ERRORS as e_av:
                raise ValueError(
                    f"Both yfinance and Alpha Vantage failed for {symbol}. AV Error: {e_av}"
                ) from e_av

    @staticmethod
    def _get_quote_yfinance(symbol: str) -> Quote:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info

        if "lastPrice" not in info:
            raise ValueError(f"Invalid symbol or no data available for {symbol}")

        price = float(info["lastPrice"])
        prev_close = float(info.get("previousClose", price))
        change_percent = (
            ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
        )
        volume = int(info.get("lastVolume", 0))

        return Quote(
            symbol=symbol.upper(),
            price=price,
            change_percent=round(change_percent, 2),
            volume=volume,
        )

    @staticmethod
    def _get_quote_alphavantage(symbol: str) -> Quote:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not set in environment.")

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        with httpx.Client() as client:
            response = client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

        quote_data = data.get("Global Quote", {})
        if not quote_data:
            raise ValueError(f"Alpha Vantage returned empty data for {symbol}")

        price = float(quote_data.get("05. price", 0.0))
        change_percent_str = quote_data.get("10. change percent", "0%").strip("%")
        change_percent = float(change_percent_str)
        volume = int(quote_data.get("06. volume", 0))

        return Quote(
            symbol=symbol.upper(),
            price=price,
            change_percent=round(change_percent, 2),
            volume=volume,
        )
