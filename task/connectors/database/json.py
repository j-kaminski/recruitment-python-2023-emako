import json
import os

from task.connectors.common import read_json_file
from task.connectors.database.base import DatabaseConnector
from task.logger import LOGGER

from ...config import JSON_DATABASE_NAME
from .models import CurrencyConversionPLN


class JsonFileDatabaseConnector(DatabaseConnector):
    def __init__(self) -> None:
        if not os.path.exists(JSON_DATABASE_NAME):
            with open(JSON_DATABASE_NAME, "w", encoding="utf-8") as file:
                file.write("{}")
            LOGGER.info(f"Created new database file: {JSON_DATABASE_NAME}")
            self._data: dict[CurrencyConversionPLN] = {}
        else:
            LOGGER.info(f"Using existing database file: {JSON_DATABASE_NAME}")
            self._data: dict[CurrencyConversionPLN] = read_json_file(JSON_DATABASE_NAME)
            for item in self._data:
                self._data[item] = CurrencyConversionPLN(**self._data[item])

    def close_connection(self):
        pass

    def _generate_id(self) -> int:
        if not self._data:
            return 1

        all_ids = [int(key) for key in self._data.keys()]
        highest_id = max(all_ids)

        if len(all_ids) != highest_id:
            return min(set(range(1, highest_id)) - set(all_ids))

        return highest_id + 1

    def save(self, entity: CurrencyConversionPLN) -> int:
        if entity.id in self._data:
            return entity.id

        entity.id = self._generate_id()

        with open(JSON_DATABASE_NAME, "w") as file:
            self._data.update({entity.id: entity})
            sorted_keys = sorted(self._data.keys(), key=lambda x: int(x))
            dict_data = {key: self._data[key].to_dict() for key in sorted_keys}

            file.write(json.dumps(dict_data, indent=4))

        LOGGER.info(f"Entity saved: {entity}")

        return entity.id

    def get_all(self) -> list[CurrencyConversionPLN]:
        return list(self._data.values())

    def get_by_id(self, id: int) -> CurrencyConversionPLN:
        if not id in self._data:
            return None
        return self._data[id]
