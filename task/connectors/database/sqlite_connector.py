import logging
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from task.config import SQLITE_DATABASE_NAME
from task.connectors.database.base import DatabaseConnector
from .models import Base, CurrencyConversionPLN


class SQLiteDatabaseConnector(DatabaseConnector):
    def __init__(self) -> None:
        self._engine = create_engine(f"sqlite:///{SQLITE_DATABASE_NAME}")
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)()

    def close_connection(self):
        self._session.close()

    def save(self, entity: CurrencyConversionPLN) -> int:
        self._session.add(entity)
        self._session.commit()
        logging.debug(f"save: {entity}")
        return entity.id

    def get_all(self) -> list[CurrencyConversionPLN]:
        all_entities = self._session.get(CurrencyConversionPLN).all()
        logging.debug(f"get_all: {all_entities}")
        return all_entities

    def get_by_id(self, entity_id: int) -> Optional[CurrencyConversionPLN]:
        entity = self._session.get(CurrencyConversionPLN, entity_id)

        logging.debug(f"get_by_id: {entity}")

        if entity is None:
            return None

        return entity
