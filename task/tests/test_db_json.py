import os
from unittest.mock import patch
from .base import TestBaseCase
from task.connectors.database.json import JsonFileDatabaseConnector

TEST_JSON_DATABASE_NAME = "test_database.json"

class TestDbJson(TestBaseCase):
    @patch("task.connectors.database.json.JSON_DATABASE_NAME", TEST_JSON_DATABASE_NAME)
    def setUp(self) -> None:
        self.db = JsonFileDatabaseConnector()

    def tearDown(self) -> None:
        self.db.close_connection()
        os.remove(TEST_JSON_DATABASE_NAME)

    def test_init_read_json_db(self):
        pass
    
    def test_save_currency_conversion(self):
        pass

    def test_save_few_currency_conversion(self):
        pass

    def test_save_currency_conversion_existing(self):
        pass
