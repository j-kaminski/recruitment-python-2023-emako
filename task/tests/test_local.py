from unittest.mock import Mock, patch

from task.connectors.currency_data_provider import CurrencyData
from task.connectors.local.local_currency_data_provider import LocalCurrencyDataProvider

from .base import TestBaseCase


def mocked_local_data():
    mock = Mock()
    mock.return_value = {
        "EUR": [
            {"date": "2023-09-01", "rate": 4.15},
            {"date": "2023-08-30", "rate": 4.10},
        ],
        "CZK": [
            {"date": "2023-09-01", "rate": 0.19},
            {"date": "2023-08-30", "rate": 0.18},
        ],
    }
    return mock


def mocked_local_data_invalid_format():
    mock = Mock()
    mock.return_value = {
        "EUR": [
            {"zz": "2023-09-01"},
        ]
    }


class TestLocal(TestBaseCase):
    @patch(
        "task.connectors.local.local_currency_data_provider.read_json_file",
        side_effect=mocked_local_data(),
    )
    def test_load_local_newest_currency_data(self, mock):
        local_currency_data_provider = LocalCurrencyDataProvider()
        data = local_currency_data_provider.fetch_currencies_data()
        mock.assert_called_once()
        expected_data = [
            CurrencyData(
                currency="eur",
                currency_rate=4.15,
                currency_rate_fetch_date="2023-09-01",
            ),
            CurrencyData(
                currency="CZK",
                currency_rate=0.19,
                currency_rate_fetch_date="2023-09-01",
            ),
        ]
        self.assertEqual(data, expected_data)

    @patch(
        "task.connectors.local.local_currency_data_provider.LOCAL_SOURCE_PATH", "xxxxx"
    )
    def test_load_local_currency_data_with_missing_file(self):
        local_currency_data_provider = LocalCurrencyDataProvider()
        data = local_currency_data_provider.fetch_currencies_data()
        expected_data = []
        self.assertEqual(data, expected_data)

    @patch(
        "task.connectors.local.local_currency_data_provider.read_json_file",
        side_effect=mocked_local_data_invalid_format(),
    )
    def test_load_local_currency_data_with_invalid_format(self, mock):
        local_currency_data_provider = LocalCurrencyDataProvider()
        data = local_currency_data_provider.fetch_currencies_data()
        mock.assert_called_once()
        expected_data = []
        self.assertEqual(data, expected_data)
