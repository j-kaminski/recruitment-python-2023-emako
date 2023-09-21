from abc import ABC, abstractmethod
from .models import CurrencyConversionPLN


class DatabaseConnector(ABC):
    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def save(self, entity: ...) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[CurrencyConversionPLN]:
        pass

    @abstractmethod
    def get_by_id(self) -> CurrencyConversionPLN: 
        pass
