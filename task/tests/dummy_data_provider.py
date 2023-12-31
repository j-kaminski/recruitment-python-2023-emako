from task.connectors.currency_data_provider import CurrencyData, CurrencyDataProvider


class DummyCurrencyDataProvider(CurrencyDataProvider):
    def __init__(self) -> None:
        super().__init__()
        self._valid_currencies = {"eur"}

    def _parse_data(self, _):
        pass

    def fetch_currencies_data(self):
        pass

    def update_currencies_data(self, currency_data: CurrencyData):
        self._currencies_data.append(currency_data)
