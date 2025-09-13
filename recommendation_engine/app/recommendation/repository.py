import json
import logging
import typing as t
from datetime import datetime, timezone

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError, PyMongoError, WriteError

from recommendation_engine.app.core.database.repository_base import RepositoryBase
from recommendation_engine.app.recommendation.models import RecommendationModel
from recommendation_engine.app.recommendation.types import (
    TProductIdsFingerPrint,
    TProductIdsOrderedAndUnique,
    TRecommendationSubSequences,
)


logger = logging.getLogger(__name__)


class RecommendationRepositoryException(Exception):
    pass


class RecommendationDuplicate(RecommendationRepositoryException):
    pass


class RecommendationRepository(RepositoryBase):
    COLLECTION_NAME: t.ClassVar[str] = "recommendations"
    COLLECTION_INDEXES: t.ClassVar[list[dict[str, t.Any]]] = [
        {"key": "fingerprint", "unique": True, "order": ASCENDING},
        {"key": "createdAt", "unique": False, "order": DESCENDING},
    ]
    COLLECTION_VALIDATOR: t.ClassVar[dict[str, t.Any]] = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["fingerprint", "sequence", "subsequences", "createdAt"],
            "properties": {
                "_id": {"bsonType": "objectId"},
                "fingerprint": {"bsonType": "string"},
                "sequence": {"bsonType": "array", "items": {"bsonType": "int"}, "minItems": 1},
                "subsequences": {"bsonType": "array", "items": {"bsonType": "array", "items": {"bsonType": "int"}}},
                "createdAt": {"bsonType": "date"},
            },
            "additionalProperties": False,
        }
    }

    async def create(
        self,
        fingerprint: TProductIdsFingerPrint,
        product_ids: TProductIdsOrderedAndUnique,
        recommendations: TRecommendationSubSequences,
    ) -> RecommendationModel:
        document_model = RecommendationModel(
            fingerprint=fingerprint,
            sequence=product_ids,
            subsequences=recommendations,
            createdAt=datetime.now(timezone.utc),
        )

        document_serialized = document_model.model_dump(by_alias=True, exclude={"id", "_id"})

        try:
            result = await self.collection.insert_one(document_serialized)
        except DuplicateKeyError as error:
            logger.debug(
                f"Product_ids {product_ids} (fingerprint={fingerprint}) Already exists\nError: {error!r}",
            )
            raise RecommendationDuplicate("Document already exists.")
        except WriteError as error:
            document_prettified = json.dumps(document_serialized, indent=4, default=str)
            logger.error(
                f"Exception while inserting document: \n{document_prettified}\nError: {error!r}",
            )
            raise RecommendationRepositoryException("WriteError while inserting document")

        document_model.id = str(result.inserted_id)
        return document_model

    async def get(self, object_id: str) -> RecommendationModel | None:
        try:
            document = await self.collection.find_one({"_id": ObjectId(object_id)})
        except PyMongoError as error:
            logger.error(f"Exception while getting document {object_id}, error: {error!r}")
            raise RecommendationRepositoryException("PyMongoError while getting document")

        if not document:
            return None
        return RecommendationModel(**document)

    async def paginate(self, limit: int) -> list[RecommendationModel]:
        docs = await (self.collection.find().sort([("createdAt", -1), ("_id", -1)]).limit(limit)).to_list()
        return [RecommendationModel(**d) for d in docs]
