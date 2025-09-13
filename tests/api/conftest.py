import typing as t
import uuid
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.app.auth.secure import LoggedIn
from recommendation_engine.app.providers import get_database, recommendation_repository
from recommendation_engine.app.recommendation.repository import RecommendationRepository
from recommendation_engine.asgi import create_app


@pytest.fixture()
def mock_db_client() -> t.Any:
    class FakeDB:
        pass

    return FakeDB()


@pytest.fixture()
def mock_recommendation_repository() -> Mock:
    repo = Mock(spec=RecommendationRepository)
    repo.get = AsyncMock()
    repo.create = AsyncMock()
    repo.paginate = AsyncMock()
    return repo


@pytest.fixture(autouse=True)
def clear_get_database_cache():
    get_database.cache_clear()
    yield
    get_database.cache_clear()


@pytest.fixture(scope="function")
def app(mock_db_client, mock_recommendation_repository) -> t.Generator[FastAPI, None, None]:
    app = create_app()

    getattr(app, "dependency_overrides", {})[get_database] = lambda: mock_db_client
    getattr(app, "dependency_overrides", {})[recommendation_repository] = lambda: mock_recommendation_repository

    # Bypass auth: override the *callable returned by* restrict()
    # Return anything truthy (the value is unused by the endpoints)
    access_token = AccessToken(
        username="admin",
        expires=99999999,
        access_token=str(uuid.uuid4()),
    )
    getattr(app, "dependency_overrides", {})[LoggedIn] = lambda: access_token

    yield app


@pytest.fixture(scope="function")
def web_client(app) -> t.Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
