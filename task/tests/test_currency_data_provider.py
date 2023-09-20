from task.connectors.currency_data_provider import CurrencyDataProvider
from .base import TestBaseCase


class DummyCurrencyDataProvider(CurrencyDataProvider):
    def _parse_data(self, _):
        pass

    def fetch_currencies_data(self):
        pass


class TestCurrencyDataProvider(TestBaseCase):
    def setUp(self):
        self.currency_data_provider = DummyCurrencyDataProvider()
        self.currency_data_provider.valid_currencies.add("EUR")

    def test_valid_currency(self):
        currency = "EUR"
        value = 4.15
        self.assertTrue(self.currency_data_provider.validate_currency(currency, value))

    def test_missing_currency(self):
        currency = "USD"
        value = 4.15
        self.assertFalse(self.currency_data_provider.validate_currency(currency, value))

    def test_invalid_type_currency(self):
        currency = 123
        value = 4.15
        self.assertFalse(self.currency_data_provider.validate_currency(currency, value))

    def test_invalid_type_value(self):
        currency = "EUR"
        value = "4.15"
        self.assertFalse(self.currency_data_provider.validate_currency(currency, value))

    def test_invalid_type_value(self):
        currency = "EUR"
        value = -4.15
        self.assertFalse(self.currency_data_provider.validate_currency(currency, value))
