import logging
from task.connectors.currency_data_provider import CurrencyData, CurrencyDataProvider
from .endpoints import get_table_rate


class NBPCurrencyDataProvider(CurrencyDataProvider):
    def _parse_data(self, data: list[dict]) -> None:
        try:
            data = data[0]
            date = data["effectiveDate"]
            for rate in data["rates"]:
                self.currencies_data.append(
                    CurrencyData(
                        currency=rate["code"],
                        currency_rate=rate["mid"],
                        currency_rate_fetch_date=date,
                    )
                )
        except KeyError as e:
            logging.error(f"Invalid data format: {e}")

    def fetch_currencies_data(self) -> list[CurrencyData]:
        raw_data = get_table_rate()
        if raw_data:
            self._parse_data(raw_data)

        return self.currencies_data
