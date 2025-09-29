import requests
import pandas as pd
from typing import Dict, List
from .base import ExchangeAPI

class MEXCExchange(ExchangeAPI):
    name = "MEXC"

    def __init__(self):
        self.base_url = "https://api.mexc.com/api/v3"

    def get_symbols_from_24hr(self, priceChangePercent: int = 3) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/ticker/24hr")
            data = response.json()
            symbols = [
                s["symbol"] for s in data
                if abs(float(s["priceChangePercent"])) > priceChangePercent
            ]
            return symbols
        except Exception as e:
            print(f"Ошибка при загрузке символов MEXC: {e}")
            return ["BTC_USDT", "ETH_USDT", "SOL_USDT", "DOGE_USDT", "XRP_USDT"]

    def get_symbols(self, firstSymbols: int = 0) -> Dict[str, int]:
        try:
            response = requests.get(f"{self.base_url}/exchangeInfo")
            data = response.json()
            symbols_info = {}
            i = 0
            for s in data["symbols"]:
                if(i > firstSymbols):
                    break
                if (
                    s["quoteAsset"] == "USDT"
                    and s["isSpotTradingAllowed"] is True
                    and s["status"] == "1"
                ):
                    precision = s["quotePrecision"]
                    if precision is not None:
                        symbols_info[s["symbol"]] = int(precision)
                i = i + 1
            return symbols_info
        except Exception as e:
            print(f"Ошибка при загрузке символов MEXC: {e}")
            return {
                "BTC_USDT": 8,
            "ETH_USDT": 6,
            "SOL_USDT": 4,
            "DOGE_USDT": 6,
            "XRP_USDT": 6,
            }

    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 100) -> pd.DataFrame:
        """Получаем свечи"""
        try:
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }
            response = requests.get(f"{self.base_url}/klines", params=params)
            klines = response.json()

            # MEXC возвращает: [open_time, open, high, low, close, volume, ...]
            df = pd.DataFrame(klines, columns=[
                "time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume"
            ])

            # Преобразуем время в секунды (Lightweight Charts требует секунды!)
            df["time"] = (df["time"] // 1000).astype(int)
            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = pd.to_numeric(df[col])

            return df[["time", "open", "high", "low", "close", "volume"]]
        except Exception as e:
            print(f"Ошибка при загрузке свечей {symbol}: {e}")
            # Возвращаем пустой DF с правильной структурой
            return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])