from .base import TestBaseCase
from .dummy_data_provider import DummyCurrencyDataProvider


class TestCurrencyDataProvider(TestBaseCase):
    def setUp(self):
        super().setUp()
        self.currency_data_provider = DummyCurrencyDataProvider()
