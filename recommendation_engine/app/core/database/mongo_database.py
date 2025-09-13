import logging
from urllib.parse import quote_plus

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi

from recommendation_engine.settings import Settings

logger = logging.getLogger(__name__)


class MongoDatabaseException(Exception):
    pass


class MongoDatabaseInitDBException(MongoDatabaseException):
    pass


class MongoDatabase:

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

    async def init_db(self) -> None:
        logger.info("Initializing MongoDB database")
        await self._ping()

        db = self.db
        app_collection = ("recommendations",)
        collections = await db.list_collection_names()
        for collection in app_collection:
            if collection not in collections:
                await db.create_collection(collection)

        logger.info("MongoDB database initialized")

    async def close(self) -> None:
        logger.info("Closing MongoDB  database")

        await self._client.close()

        logger.info("MongoDB  database closed")

    async def _ping(self) -> None:
        try:
            await self._client.admin.command({'ping': 1})
        except ConnectionFailure as error:
            logger.error(f"MongoDB connection failed: {error}")
            raise MongoDatabaseInitDBException(
                "Error while pinging MongoDB server. Check your connection settings and try again.",
            )
        logger.info("MongoDB ping OK.")
