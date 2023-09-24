from unittest.mock import Mock, patch
from .base import TestBaseCase
from task.connectors.nbp.nbp_currency_data_provider import NBPCurrencyDataProvider
from task.connectors.currency_data_provider import CurrencyData


def mocked_get_table_a():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "table": "A",
            "no": "181/A/NBP/2023",
            "effectiveDate": "2023-09-19",
            "rates": [
                {"currency": "bat (Tajlandia)", "code": "THB", "mid": 0.1208},
                {"currency": "dolar amerykański", "code": "USD", "mid": 4.3472},
                {"currency": "dolar australijski", "code": "AUD", "mid": 2.8043},
            ],
        }
    ]
    return mock_response


def mocked_get_table_a_invalid_format():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "table": "A",
            "no": "181/A/NBP/2023",
        }
    ]
    return mock_response

def mocked_get_table_a_error_status_code():
    mock_response = Mock()
    mock_response.status_code = 400
    return mock_response


class TestNBP(TestBaseCase):
    @patch("requests.get", return_value=mocked_get_table_a())
    def test_load_nbp_parsed_currency_data(self, mock_get):
        nbp_currency_data_provider = NBPCurrencyDataProvider()
        data = nbp_currency_data_provider.fetch_currencies_data()
        mock_get.assert_called_once()
        expected_data = [
            CurrencyData(
                currency="THB",
                currency_rate=0.1208,
                currency_rate_fetch_date="2023-09-19",
            ),
            CurrencyData(
                currency="USD",
                currency_rate=4.3472,
                currency_rate_fetch_date="2023-09-19",
            ),
            CurrencyData(
                currency="AUD",
                currency_rate=2.8043,
                currency_rate_fetch_date="2023-09-19",
            ),
        ]
        self.assertEqual(data, expected_data)

    @patch("requests.get", return_value=mocked_get_table_a_invalid_format())
    def test_load_nbp_parsed_currency_data(self, mock_get):
        nbp_currency_data_provider = NBPCurrencyDataProvider()
        data = nbp_currency_data_provider.fetch_currencies_data()
        mock_get.assert_called_once()
        self.assertEqual(data, [])

    # TODD
    def test_load_nbp_currency_data_with_connection_error(self):
        pass
