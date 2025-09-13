import typing as t
from abc import ABC


class RepositoryBase(ABC):
    COLLECTION_NAME: t.ClassVar[str]
    COLLECTION_INDEXES: t.ClassVar[list[dict[str, t.Any]]]
    COLLECTION_VALIDATOR: t.ClassVar[dict[str, t.Any]]
