import logging
from urllib.parse import quote_plus

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import ConnectionFailure, CollectionInvalid
from pymongo.server_api import ServerApi

from recommendation_engine.app.core.database.database_client_base import DatabaseClientBase
from recommendation_engine.app.core.database.repository_base import RepositoryBase
from recommendation_engine.settings import Settings

logger = logging.getLogger(__name__)


class MongoDatabaseException(Exception):
    pass


class MongoDatabaseInitDBException(MongoDatabaseException):
    pass


class MongoDatabase(DatabaseClientBase):

    def __init__(self, settings: Settings | None = None):
        self._settings: Settings = settings or Settings.get()
        self._database_name: str = self._settings.db_mongo_db_name
        self._uri: str = "mongodb://%s:%s@%s" % (
            quote_plus(self._settings.db_mongo_username), quote_plus(self._settings.db_mongo_password),
            f"{self._settings.db_mongo_host}:{self._settings.db_mongo_port}",
        )
        self._client: AsyncMongoClient = AsyncMongoClient(
            self._uri,
            minPoolSize=self._settings.db_mongo_min_pool_size,
            maxPoolSize=self._settings.db_mongo_max_pool_size,
            server_api=ServerApi(
                "1",
                strict=True,
                deprecation_errors=True,
            ),
        )

    @property
    def db(self) -> AsyncDatabase:
        return self._client.get_database(self._database_name)

    async def init_db(self, repositories: tuple[RepositoryBase, ...]) -> None:
        logger.info("Initializing MongoDB database")
        await self.ping()

        db = self.db
        for repository in repositories:
            collection_name = repository.COLLECTION_NAME

            try:
                await db.create_collection(collection_name, validator=repository.COLLECTION_VALIDATOR)
            except CollectionInvalid:
                pass

            collection: AsyncCollection = db[collection_name]
            for index in repository.COLLECTION_INDEXES:
                await collection.create_index([(index["key"], index["order"])], unique=index["unique"])
            logger.info(f"Collection {collection_name} initialized")

        logger.info("MongoDB database initialized")

    async def close(self) -> None:
        logger.info("Closing MongoDB  database")

        await self._client.close()

        logger.info("MongoDB  database closed")

    async def ping(self) -> bool:
        try:
            await self._client.admin.command({'ping': 1})
        except ConnectionFailure as error:
            logger.error(f"MongoDB connection failed: {error}")
            raise MongoDatabaseInitDBException(
                "Error while pinging MongoDB server. Check your connection settings and try again.",
            )
        logger.info("MongoDB ping OK.")
        return True
