from task.connectors.currency_data_provider import CurrencyData
from task.currency_converter import ConvertedPricePLN, PriceCurrencyConverterToPLN

from .base import TestBaseCase
from .dummy_data_provider import DummyCurrencyDataProvider


class TestCurrencyConverter(TestBaseCase):
    def test_convert_to_pln(self):
        currency_data_provider = DummyCurrencyDataProvider()
        euro_currency_data = CurrencyData(
            currency="EUR",
            currency_rate=4.15,
            currency_rate_fetch_date="2023-01-01",
        )
        currency_data_provider.update_currencies_data(euro_currency_data)
        converter = PriceCurrencyConverterToPLN(currency_data_provider)

        expected = ConvertedPricePLN(
            price_in_source_currency=10,
            currency="eur",
            currency_rate=4.15,
            currency_rate_fetch_date="2023-01-01",
            price_in_pln=41.5,
        )
        result = converter.convert_to_pln("eur", 10)
        self.assertEqual(result, expected)

    def test_convert_missing_currency(self):
        currency_data_provider = DummyCurrencyDataProvider()
        converter = PriceCurrencyConverterToPLN(currency_data_provider)
        result = converter.convert_to_pln("usd", 10)
        self.assertIsNone(result)
