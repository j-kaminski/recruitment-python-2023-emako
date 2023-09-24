from dataclasses import dataclass
from task.logger import LOGGER
from .connectors.currency_data_provider import CurrencyDataProvider


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:
    def __init__(self, currency_data_provider: CurrencyDataProvider):
        self._currency_data_provider = currency_data_provider

    def convert_to_pln(self, currency: str, price: float) -> ConvertedPricePLN:
        currency_data = self._currency_data_provider.currency_data(currency)

        if currency_data is None:
            return None

        price_in_pln = price * currency_data.currency_rate
        LOGGER.info(
            f"Converted price from {currency.upper()} to PLN: {price} {currency} -> {price_in_pln} PLN"
        )

        return ConvertedPricePLN(
            price_in_source_currency=price,
            currency=currency,
            currency_rate=currency_data.currency_rate,
            currency_rate_fetch_date=currency_data.currency_rate_fetch_date,
            price_in_pln=price_in_pln,
        )
