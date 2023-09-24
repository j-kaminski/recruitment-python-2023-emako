import os
from unittest.mock import patch
from .base import TestBaseCase
from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.models import CurrencyConversionPLN

TEST_JSON_DATABASE_NAME = "test_database.json"


class TestDbJson(TestBaseCase):
    @patch("task.connectors.database.json.JSON_DATABASE_NAME", TEST_JSON_DATABASE_NAME)
    def setUp(self) -> None:
        super().setUp()
        self.db = JsonFileDatabaseConnector()

    def tearDown(self) -> None:
        super().tearDown()
        self.db.close_connection()
        os.remove(TEST_JSON_DATABASE_NAME)

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

        saved_model = self.db._data[id]
        self.assertEqual(entity, saved_model)
        self.assertEqual(len(self.db.get_all()), 1)
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
        saved_models = self.db.get_all()
        self.assertEqual(entities, saved_models)
        self.assertEqual(ids, [1, 2])

    def test_save_currency_conversion_existing(self):
        entity = CurrencyConversionPLN(
            currency="EUR",
            rate=4.5,
            date="2021-01-01",
            price_in_pln=45,
        )

        first_id = self.db.save(entity)
        second_id = self.db.save(entity)
        self.assertEqual(len(self.db.get_all()), 1)
        self.assertEqual(first_id, second_id)
