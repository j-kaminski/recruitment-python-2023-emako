import os
from .base import TestBaseCase
from task.connectors.database.sqlite_connector import SQLiteDatabaseConnector
from task.connectors.database.models import CurrencyConversionPLN
from unittest.mock import patch

TEST_SQLITE_DATABASE_NAME = "test_database.db"


class TestSqliteConnector(TestBaseCase):
    @patch(
        "task.connectors.database.sqlite_connector.SQLITE_DATABASE_NAME",
        TEST_SQLITE_DATABASE_NAME,
    )
    def setUp(self) -> None:
        super().setUp()
        self.db = SQLiteDatabaseConnector()

    def tearDown(self) -> None:
        super().tearDown()
        self.db.close_connection()
        os.remove(TEST_SQLITE_DATABASE_NAME)

    def test_get_by_id(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )
        self.db.save(entity)

        saved_model = self.db.get_by_id(1)
        self.assertEqual(entity, saved_model)

    def test_get_by_id_not_existing(self):
        saved_model = self.db.get_by_id(1)
        self.assertEqual(saved_model, None)

    def test_get_all(self):
        entities = [
            CurrencyConversionPLN(
                currency="EUR",
                rate=4.5,
                date="2021-01-01",
                price_in_pln=45,
            ),
            CurrencyConversionPLN(
                currency="USD",
                rate=4,
                date="2021-01-01",
                price_in_pln=20,
            ),
        ]

        ids = [self.db.save(entity) for entity in entities]
        saved_models = self.db.get_all()
        self.assertEqual(entities, saved_models)
        self.assertEqual(ids, [1, 2])

    def test_get_all_empty(self):
        saved_models = self.db.get_all()
        self.assertEqual(saved_models, [])

    def test_save_currency_conversion(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )

        id = self.db.save(entity)

        saved_model = self.db._session.get(CurrencyConversionPLN, id)
        self.assertEqual(entity, saved_model)
        self.assertEqual(self.db._session.query(CurrencyConversionPLN).count(), 1)
        self.assertEqual(id, 1)

    def test_save_few_currency_conversion(self):
        entities = [
            CurrencyConversionPLN(
                currency="EUR",
                rate=4.5,
                date="2021-01-01",
                price_in_pln=45,
            ),
            CurrencyConversionPLN(
                currency="USD",
                rate=4,
                date="2021-01-01",
                price_in_pln=20,
            ),
        ]

        ids = [self.db.save(entity) for entity in entities]
        saved_models = [self.db.get_by_id(id) for id in ids]
        self.assertEqual(entities, saved_models)
        self.assertEqual(ids, [1, 2])

    def test_save_currency_conversion_existing(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )

        id = self.db.save(entity)
        id2 = self.db.save(entity)
        self.assertEqual(self.db._session.query(CurrencyConversionPLN).count(), 1)
        self.assertEqual(id, id2)
