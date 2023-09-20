from dataclasses import dataclass
from .connectors.currency_data_provider import CurrencyData


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:

    def convert_to_pln(
        self, currency_data: CurrencyData, price: float
    ) -> ConvertedPricePLN:
        return ConvertedPricePLN(
            price_in_source_currency=price,
            currency=currency_data.currency,
            currency_rate=currency_data.currency_rate,
            currency_rate_fetch_date=currency_data.currency_rate_fetch_date,
            price_in_pln=price * currency_data.currency_rate,
        )
