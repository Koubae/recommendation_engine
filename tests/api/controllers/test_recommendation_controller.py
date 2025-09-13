import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from recommendation_engine.app.recommendation.repository import (
    RecommendationDuplicate,
    RecommendationRepositoryException,
)


@pytest.mark.unit
class TestUnitRecommendationResponse:
    web_client: TestClient
    mock_recommendation_repository: Mock

    @pytest.fixture(autouse=True)
    async def setup_class(self, web_client, mock_recommendation_repository):
        self.web_client = web_client
        self.mock_recommendation_repository = mock_recommendation_repository
        yield

    def test_show_invalid_id_returns_400(self):
        r = self.web_client.get("/api/v1/recommendations/not-a-valid-object-id")

        assert r.status_code == 400
        assert r.json()["detail"] == "Invalid ID format"

    def test_show_not_found_returns_404(self):
        _id = str(ObjectId())
        self.mock_recommendation_repository.get.return_value = None

        r = self.web_client.get(f"/api/v1/recommendations/{_id}")
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()

        self.mock_recommendation_repository.get.assert_awaited_once_with(_id)

    def test_show_repo_exception_returns_500(self):
        _id = str(ObjectId())
        self.mock_recommendation_repository.get.side_effect = RecommendationRepositoryException("boom")

        r = self.web_client.get(f"/api/v1/recommendations/{_id}")
        assert r.status_code == 500
        assert "unexpected error" in r.json()["detail"].lower()

    def test_show_success_returns_document(self):
        _id = str(ObjectId())
        doc = {
            "_id": _id,
            "fingerprint": "abc123",
            "sequence": [1, 2],
            "subsequences": [[1], [2], [1, 2]],
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        self.mock_recommendation_repository.get.return_value = doc

        r = self.web_client.get(f"/api/v1/recommendations/{_id}")
        assert r.status_code == 200
        body = r.json()
        assert body["fingerprint"] == "abc123"
        assert body["sequence"] == [1, 2]
        assert body["subsequences"] == [[1], [2], [1, 2]]

    def test_create_conflict_returns_409(self):
        self.mock_recommendation_repository.create.side_effect = RecommendationDuplicate("exists!")

        r = self.web_client.post("/api/v1/recommendations", json={"product_ids": [3, 1, 2, 2]})
        assert r.status_code == 409
        assert "already exists" in r.json()["detail"].lower()

    def test_create_repo_exception_returns_500(self):
        self.mock_recommendation_repository.create.side_effect = RecommendationRepositoryException("db down")

        r = self.web_client.post("/api/v1/recommendations", json={"product_ids": [1, 2, 3]})
        assert r.status_code == 500
        assert "unexpected error" in r.json()["detail"].lower()

    def test_create_success_returns_document(self):
        doc = {
            "fingerprint": str(uuid.uuid4()),
            "sequence": [1, 2, 3],
            "subsequences": [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]],
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }
        self.mock_recommendation_repository.create.return_value = doc

        r = self.web_client.post("/api/v1/recommendations", json={"product_ids": [3, 1, 2, 2]})
        args, _ = self.mock_recommendation_repository.create.await_args
        body = r.json()

        assert r.status_code == 201
        assert body["sequence"] == [1, 2, 3]
        assert [1, 2] in body["subsequences"]
        assert args[1] == [1, 2, 3]
        assert len(args[2]) == 7

    def test_list_success_returns_only_sequence_and_subsequences(self):
        docs = [
            SimpleNamespace(sequence=[1, 2], subsequences=[[1], [2], [1, 2]]),
            SimpleNamespace(sequence=[2, 3], subsequences=[[2], [3], [2, 3]]),
        ]
        self.mock_recommendation_repository.paginate.return_value = docs

        r = self.web_client.get("/api/v1/recommendations")
        body = r.json()

        assert r.status_code == 200
        assert isinstance(body, list)
        assert body[0] == {"sequence": [1, 2], "subsequences": [[1], [2], [1, 2]]}
        assert body[1] == {"sequence": [2, 3], "subsequences": [[2], [3], [2, 3]]}
        self.mock_recommendation_repository.paginate.assert_awaited_once_with(limit=10)

    def test_list_repo_exception_returns_500(self):
        self.mock_recommendation_repository.paginate.side_effect = RecommendationRepositoryException("nope")

        r = self.web_client.get("/api/v1/recommendations")
        assert r.status_code == 500
        assert "unexpected error" in r.json()["detail"].lower()
