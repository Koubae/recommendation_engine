import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from recommendation_engine.app.api.controllers.index import IndexController


@pytest.mark.unit
class TestUnitIndexController:
    @pytest.fixture
    def app(self):
        app = FastAPI()
        app.include_router(IndexController().router)
        return app

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    def test_home_endpoint(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert response.text and isinstance(response.text, str)

    def test_ping_endpoint(self, client):
        """Test the ping endpoint returns pong."""
        response = client.get("/ping")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert response.text == "pong"

    def test_alive_endpoint(self, client):
        response = client.get("/alive")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert response.text == "OK"

    def test_ready_endpoint(self, client):
        response = client.get("/ready")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert response.text == "OK"
