from abc import ABC, abstractmethod

from pymongo.asynchronous.database import AsyncDatabase


class DatabaseClientBase(ABC):

    @property
    @abstractmethod
    def db(self) -> AsyncDatabase:
        pass
