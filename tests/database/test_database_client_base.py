from unittest.mock import patch

import pytest
from pymongo.errors import ConnectionFailure

from recommendation_engine.app.core.database.mongo_database import MongoDatabase, MongoDatabaseInitDBException
from recommendation_engine.settings import Settings


@pytest.mark.asyncio
@pytest.mark.integration
class TestIntegrationMongoDatabase:
    db: MongoDatabase

    @pytest.fixture(autouse=True)
    async def setup_class(self):
        settings = Settings.build_settings()
        mongo_db = MongoDatabase(settings=settings)

        self.db = mongo_db

        yield

        await self.db.close()

    async def test_ping(self):
        response = await self.db.ping()
        assert response is True

    async def test_ping_on_connection_error(self):
        with (
            patch(
                "pymongo.asynchronous.database.AsyncDatabase.command",
                side_effect=ConnectionFailure("mock connection error"),
            ),
            pytest.raises(MongoDatabaseInitDBException),
        ):
            await self.db.ping()
