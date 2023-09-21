import os
import json
from ...config import JSON_DATABASE_NAME
from task.connectors.common import read_json_file
from task.connectors.database.base import DatabaseConnector
from .models import CurrencyConversionPLN


class JsonFileDatabaseConnector(DatabaseConnector):
    def __init__(self) -> None:
        if not os.path.exists(JSON_DATABASE_NAME):
            with open(JSON_DATABASE_NAME, "w") as file:
                file.write("{}")
            self._data: dict[CurrencyConversionPLN] = {}
        else:
            self._data: dict[CurrencyConversionPLN] = read_json_file(JSON_DATABASE_NAME)
            for item in self._data:
                self._data[item] = CurrencyConversionPLN(**self._data[item])
    
    def close_connection(self):
        pass

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            return json.load(file)
    
    def _generate_id(self) -> int:
        return max([int(key) for key in self._data.keys()]) + 1

    def save(self, entity: CurrencyConversionPLN) -> int:
        if entity.id in self._data:
            return entity.id
        
        entity.id = self._generate_id()

        with open(JSON_DATABASE_NAME, "w") as file:
            self._data.update({entity.id: entity})
            dict_data = {key: value.to_dict() for key, value in self._data.items()}
            file.write(json.dumps(dict_data, indent=4))


    def get_all(self) -> list[CurrencyConversionPLN]:
        return self._data

    def get_by_id(self, id: int) -> CurrencyConversionPLN:
        if not id in self._data:
            return None
        return self._data[id]
