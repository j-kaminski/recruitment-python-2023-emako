import os
from .base import TestBaseCase
from task.connectors.database.sqlite_connector import SQLiteDatabaseConnector
from task.connectors.database.models import CurrencyConversionPLN 
from unittest.mock import patch

TEST_SQLITE_DATABASE_NAME = "test_database.db"


class TestSqliteConnector(TestBaseCase):

    @patch("task.connectors.database.sqlite_connector.SQLITE_DATABASE_NAME", TEST_SQLITE_DATABASE_NAME)
    def setUp(self) -> None:
        self.db = SQLiteDatabaseConnector()

    def tearDown(self) -> None:
        self.db.close_connection()
        os.remove(TEST_SQLITE_DATABASE_NAME)

    def test_save_currency_conversion(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )

        id = self.db.save(entity)

        saved_model = self.db._session.get(CurrencyConversionPLN, id)
        self.assertIsNotNone(saved_model)

    def test_save_few_currency_conversion(self):
        pass

    def test_save_currency_conversion_existing(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )

        id = self.db.save(entity)
        id2 = self.db.save(entity)
        self.assertEqual(id, id2)
        self.assertEqual(self.db._session.query(CurrencyConversionPLN).count(), 1)

