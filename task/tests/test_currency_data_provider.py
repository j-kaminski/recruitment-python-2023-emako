from .base import TestBaseCase
from .dummy_data_provider import DummyCurrencyDataProvider


class TestCurrencyDataProvider(TestBaseCase):
    def setUp(self):
        self.currency_data_provider = DummyCurrencyDataProvider()

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
