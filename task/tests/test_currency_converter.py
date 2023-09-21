from .base import TestBaseCase
from task.currency_converter import PriceCurrencyConverterToPLN, ConvertedPricePLN
from task.connectors.currency_data_provider import CurrencyData
from task.connectors.local.local_currency_data_provider import LocalCurrencyDataProvider
from task.connectors.nbp.nbp_currency_data_provider import NBPCurrencyDataProvider
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
            currency="EUR",
            currency_rate=4.15,
            currency_rate_fetch_date="2023-01-01",
            price_in_pln=41.5,
        )
        result = converter.convert_to_pln("EUR", 10)
        self.assertEqual(result, expected)

    def test_convert_missing_currency(self):
        currency_data_provider = DummyCurrencyDataProvider()
        converter = PriceCurrencyConverterToPLN(currency_data_provider)
        result = converter.convert_to_pln("USD", 10)
        self.assertIsNone(result)

    def test_convert_invalid_currency(self):
        currency_data_provider = DummyCurrencyDataProvider()
        converter = PriceCurrencyConverterToPLN(currency_data_provider)
        result = converter.convert_to_pln(123, 10)
        self.assertIsNone(result)

    def test_convert_invalid_value(self):
        currency_data_provider = DummyCurrencyDataProvider()
        converter = PriceCurrencyConverterToPLN(currency_data_provider)
        result = converter.convert_to_pln("EUR", "10")
        self.assertIsNone(result)
