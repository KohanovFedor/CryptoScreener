import requests
import pandas as pd
from typing import List
from .base import ExchangeAPI

class MEXCExchange(ExchangeAPI):
    name = "MEXC"

    def __init__(self):
        self.base_url = "https://api.mexc.com/api/v3"

    def get_symbols(self) -> List[str]:
        """Получаем список активных USDT-пар"""
        try:
            response = requests.get(f"{self.base_url}/exchangeInfo")
            data = response.json()
            symbols = [
                s["symbol"] for s in data["symbols"]
                if s["quoteAsset"] == "USDT" and s["status"] == "1"
            ]
            # Ограничиваем для демо (иначе слишком много)
            return sorted(symbols)[:20]  # первые 20
        except Exception as e:
            print(f"Ошибка при загрузке символов MEXC: {e}")
            return ["BTC_USDT", "ETH_USDT", "SOL_USDT", "DOGE_USDT", "XRP_USDT"]

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
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base", "taker_buy_quote", "ignore"
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