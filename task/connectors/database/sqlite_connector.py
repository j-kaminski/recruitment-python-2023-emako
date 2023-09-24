import logging
from typing import Optional

from task.logger import LOGGER
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
        LOGGER.info(f"Connected to database: {SQLITE_DATABASE_NAME}")

    def close_connection(self):
        self._session.close()

    def save(self, entity: CurrencyConversionPLN) -> int:
        self._session.add(entity)
        self._session.commit()
        LOGGER.info(f"Entity saved: {entity}")
        return entity.id

    def get_all(self) -> list[CurrencyConversionPLN]:
        all_entities = self._session.query(CurrencyConversionPLN).all()
        return all_entities

    def get_by_id(self, entity_id: int) -> Optional[CurrencyConversionPLN]:
        entity = self._session.get(CurrencyConversionPLN, entity_id)

        if entity is None:
            return None

        return entity
