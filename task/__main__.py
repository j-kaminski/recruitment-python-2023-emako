import sys
from logging import getLogger

from .currency_converter import PriceCurrencyConverterToPLN
from .connectors.local.local_currency_data_provider import LocalCurrencyDataProvider
from .connectors.nbp.nbp_currency_data_provider import NBPCurrencyDataProvider
from .connectors.database.sqlite_connector import SQLiteDatabaseConnector
from .connectors.database.json import JsonFileDatabaseConnector
from .connectors.database.models import CurrencyConversionPLN


logger = getLogger(__name__)
# setup logger to debug
logger.setLevel("DEBUG")


def main():
    if len(sys.argv) > 1:
        env = sys.argv[1]
        if env not in ["dev", "prod"]:
            raise ValueError("Invalid env parameter (dev, prod))")
    else:
        raise ValueError("Missing env parameter (dev, prod))")

    # TODO: handling invalid input
    logger.info("Job started!")
    source = input("Please enter source (local or nbp): ")
    if source == "local":
        currency_data_provider = LocalCurrencyDataProvider()
    elif source == "nbp":
        currency_data_provider = NBPCurrencyDataProvider()

    currency_data = currency_data_provider.fetch_currencies_data()
    if len(currency_data) == 0:
        print("No data found")
    else:
        for currency in currency_data:
            print(currency)

        currency_select, currency_value = input(
            "Please enter currency and value (e.g. EUR 10): "
        ).split()
        currency_converter = PriceCurrencyConverterToPLN(currency_data_provider)
        converted_price_pln = currency_converter.convert_to_pln(
            currency_select, float(currency_value)
        )

        if env == "dev":
            database = JsonFileDatabaseConnector()
        elif env == "prod":
            database = SQLiteDatabaseConnector()

        new_entity = CurrencyConversionPLN(
            currency=converted_price_pln.currency,
            rate=converted_price_pln.currency_rate,
            date=converted_price_pln.currency_rate_fetch_date,
            price_in_pln=converted_price_pln.price_in_pln,
        )
        database.save(new_entity)
        database.close_connection()

    logger.info("Job done!")


if __name__ == "__main__":
    main()
