import json
from ...config import JSON_DATABASE_NAME
from task.connectors.common import read_json_file


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = read_json_file(JSON_DATABASE_NAME)

    def save(self, entity: ...) -> int:
        raise NotImplementedError()

    def get_all(self) -> list[...]:
        raise NotImplementedError()

    def get_by_id(self) -> ...:
        raise NotImplementedError()
