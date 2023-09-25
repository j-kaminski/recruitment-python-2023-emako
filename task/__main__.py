import sys

from .connectors.currency_data_provider import CurrencyDataProvider
from .connectors.database.base import DatabaseConnector
from .connectors.database.json import JsonFileDatabaseConnector
from .connectors.database.models import CurrencyConversionPLN
from .connectors.database.sqlite_connector import SQLiteDatabaseConnector
from .connectors.local.local_currency_data_provider import LocalCurrencyDataProvider
from .connectors.nbp.nbp_currency_data_provider import NBPCurrencyDataProvider
from .currency_converter import PriceCurrencyConverterToPLN
from .logger import LOGGER


def format_input_str(input_str: str) -> str:
    if not isinstance(input_str, str):
        raise ValueError("Invalid input type")
    return input_str.lower().strip()


def handle_env_param():
    if len(sys.argv) > 1:
        env = format_input_str(sys.argv[1])
        if env not in ["dev", "prod"]:
            raise ValueError("Invalid env parameter (dev, prod))")
    else:
        raise ValueError("Missing env parameter (dev, prod))")
    return env


def handle_source_input():
    source = format_input_str(input("Please enter source (local or nbp): "))

    if source not in ["local", "nbp"]:
        raise ValueError("Invalid source parameter (local, nbp))")

    return source


def handle_currency_input():
    currency, currency_value = input(
        "Please enter currency and value (e.g. eur 10): "
    ).split()
    currency = format_input_str(currency)
    currency_value = float(currency_value)

    return currency, currency_value


CURRENCY_DATA_PROVIDER = {
    "local": LocalCurrencyDataProvider,
    "nbp": NBPCurrencyDataProvider,
}

DB_CONNECTOR = {
    "dev": JsonFileDatabaseConnector,
    "prod": SQLiteDatabaseConnector,
}


def main():
    try:
        env = handle_env_param()

        LOGGER.info("Job started!")
        source = handle_source_input()

        currency_data_provider: CurrencyDataProvider = CURRENCY_DATA_PROVIDER[source]()

        currency_data = currency_data_provider.fetch_currencies_data()

        if len(currency_data) == 0:
            raise ValueError("No currency data found")

        for currency in currency_data:
            print(currency)

        currency, currency_value = handle_currency_input()

        currency_converter = PriceCurrencyConverterToPLN(currency_data_provider)
        converted_price_pln = currency_converter.convert_to_pln(
            currency, currency_value
        )

        database: DatabaseConnector = DB_CONNECTOR[env]()

        new_entity = CurrencyConversionPLN(
            currency=converted_price_pln.currency,
            rate=converted_price_pln.currency_rate,
            date=converted_price_pln.currency_rate_fetch_date,
            price_in_pln=converted_price_pln.price_in_pln,
        )

        database.save(new_entity)
        database.close_connection()

        LOGGER.info("Job done!")
    except ValueError as e:
        LOGGER.error(e)


if __name__ == "__main__":
    main()
