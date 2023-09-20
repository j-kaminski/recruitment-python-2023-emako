import os
from logging import getLogger

from .currency_converter import PriceCurrencyConverterToPLN
from .connectors.local.local_currency_data_provider import LocalCurrencyDataProvider
from .connectors.nbp.nbp_currency_data_provider import NBPCurrencyDataProvider


logger = getLogger(__name__)


def main():
    try:
        env = "dev"  # or prod
        source = "local"

        # input read source
        # TODO: handling invalid input
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
            # TODO handle value not float
            currency_data_provider.validate_currency(currency_select, currency_value)

            if env == "dev":
                database = ""

            currency_converter = PriceCurrencyConverterToPLN()

        logger.info("Job done!")
    except Exception as err:
        pass


if __name__ == "__main__":
    main()
