from abc import ABC, abstractmethod
from decimal import Decimal


from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyData:
    currency: str
    currency_rate: str
    currency_rate_fetch_date: str

    def __post_init__(self):
        object.__setattr__(self, "currency", self.currency.lower())

    def __str__(self):
        return f"{self.currency} {self.currency_rate} {self.currency_rate_fetch_date}"


class CurrencyDataProvider(ABC):
    def __init__(self):
        self._currencies_data: list[CurrencyData] = []
        self._valid_currencies = set()

    @abstractmethod
    def _parse_data(self, data) -> None:
        pass

    @abstractmethod
    def fetch_currencies_data(self) -> list[CurrencyData]:
        pass

    def currency_data(self, currency: str) -> CurrencyData:
        currency = currency.lower()
        if currency in self._valid_currencies:
            for currency_data in self._currencies_data:
                if currency_data.currency == currency:
                    return currency_data

        return None
