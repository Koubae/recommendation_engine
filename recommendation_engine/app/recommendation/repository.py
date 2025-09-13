import typing as t

from pymongo import ASCENDING, DESCENDING

from recommendation_engine.app.core.database.repository_base import RepositoryBase


class RecommendationRepository(RepositoryBase):
    COLLECTION_NAME: t.ClassVar[str] = "recommendations"
    COLLECTION_INDEXES: t.ClassVar[list[dict[str, t.Any]]] = [
        {"key": "fingerprint", "unique": True, "order": ASCENDING},
        {"key": "createdAt", "unique": False, "order": DESCENDING},
    ]
    COLLECTION_VALIDATOR: t.ClassVar[dict[str, t.Any]] = {
        "$jsonSchema": {
            "bsonType"            : "object",
            "required"            : ["fingerprint", "sequence", "subSequences", "createdAt"],
            "properties"          : {
                "fingerprint" : {"bsonType": "string"},
                "sequence"    : {
                    "bsonType": "array",
                    "items"   : {"bsonType": "int"},
                    "minItems": 1
                },
                "subSequences": {
                    "bsonType": "array",
                    "items"   : {
                        "bsonType": "array",
                        "items"   : {"bsonType": "int"}
                    }
                },
                "createdAt"   : {"bsonType": "date"}
            },
            "additionalProperties": False
        }
    }
