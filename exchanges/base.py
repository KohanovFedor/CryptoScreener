from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd

class ExchangeAPI(ABC):
    name: str

    @abstractmethod
    def get_symbols(self) -> List[str]:
        """Возвращает список торговых пар (например, ['BTC_USDT', 'ETH_USDT'])"""
        pass

    @abstractmethod
    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 100) -> pd.DataFrame:
        """
        Возвращает свечи в формате DataFrame с колонками:
        time (timestamp в секундах!), open, high, low, close, volume
        """
        pass