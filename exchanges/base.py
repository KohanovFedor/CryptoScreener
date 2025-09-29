from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd

class ExchangeAPI(ABC):
    name: str

    @abstractmethod
    def get_symbols_from_24hr(self, priceChangePercent: int = 3) -> List[str]:
        """Получаем список инструментов с процентом изменений больше 3"""
        pass

    @abstractmethod
    def get_symbols(self, firstSymbols: int = 0) -> Dict[str, int]:
        """
    Возвращает словарь: {символ: quotePrecision}
    Пример: {"BTC_USDT": 8, "ETH_USDT": 6, ...}
    """
        pass

    @abstractmethod
    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 100) -> pd.DataFrame:
        """
        Возвращает свечи в формате DataFrame с колонками:
        time (timestamp в секундах!), open, high, low, close, volume
        """
        pass