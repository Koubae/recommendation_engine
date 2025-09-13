import typing as t
from abc import ABC

from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from recommendation_engine.app.core.database.database_client_base import DatabaseClientBase


class RepositoryBase(ABC):
    COLLECTION_NAME: t.ClassVar[str]
    COLLECTION_INDEXES: t.ClassVar[list[dict[str, t.Any]]]
    COLLECTION_VALIDATOR: t.ClassVar[dict[str, t.Any]]

    def __init__(self, database_client: DatabaseClientBase) -> None:
        self._database_client: DatabaseClientBase = database_client

    @property
    def db(self) -> AsyncDatabase:
        return self._database_client.db

    @property
    def collection(self) -> AsyncCollection:
        return self.db[self.COLLECTION_NAME]
