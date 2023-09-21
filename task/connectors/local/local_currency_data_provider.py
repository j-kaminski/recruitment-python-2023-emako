import logging
from typing import Optional
from task.connectors.currency_data_provider import CurrencyDataProvider, CurrencyData
from task.connectors.common import read_json_file
from task.config import LOCAL_SOURCE_PATH


class LocalCurrencyDataProvider(CurrencyDataProvider):
    def _find_currency_data(self, currency: str) -> Optional[CurrencyData]:
        if currency not in self._valid_currencies:
            return None

        return next(
            filter(
                lambda currency_data: currency_data.currency == currency,
                self._currencies_data,
            )
        )

    def _is_newest_currency_rate(self, currency: str, currency_date: str) -> bool:
        currency_data = self._find_currency_data(currency)
        if currency_data is None:
            return False

        if currency_data.currency_rate_fetch_date > currency_date:
            return False

        return True

    def _parse_data(self, data: dict) -> None:
        for currency, currency_rates in data.items():
            try:
                for currency_rate in currency_rates:
                    if (
                        currency in self._valid_currencies
                        and not self._is_newest_currency_rate(
                            currency, currency_rate["date"]
                        )
                    ):
                        continue

                    self._currencies_data.append(
                        CurrencyData(
                            currency=currency,
                            currency_rate=currency_rate["rate"],
                            currency_rate_fetch_date=currency_rate["date"],
                        )
                    )
                    self._valid_currencies.add(currency)
            except KeyError as e:
                logging.error(f"Invalid data format: {e}")

    def fetch_currencies_data(self) -> list[CurrencyData]:
        raw_data = read_json_file(LOCAL_SOURCE_PATH)
        if raw_data:
            self._parse_data(raw_data)

        return self._currencies_data
