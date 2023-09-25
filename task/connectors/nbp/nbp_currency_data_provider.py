from task.connectors.currency_data_provider import CurrencyData, CurrencyDataProvider
from task.logger import LOGGER

from .endpoints import get_table_rate


class NBPCurrencyDataProvider(CurrencyDataProvider):
    def _parse_data(self, data: list[dict]) -> None:
        try:
            data = data[0]
            date = data["effectiveDate"]
            for rate in data["rates"]:
                self._currencies_data.append(
                    CurrencyData(
                        currency=rate["code"],
                        currency_rate=rate["mid"],
                        currency_rate_fetch_date=date,
                    )
                )
                self._valid_currencies.add(rate["code"].lower())
        except KeyError as e:
            LOGGER.error(f"Invalid data format: {e} on payload {data}")

    def fetch_currencies_data(self) -> list[CurrencyData]:
        raw_data = get_table_rate()
        if raw_data:
            self._parse_data(raw_data)

        return self._currencies_data
