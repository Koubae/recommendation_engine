from datetime import datetime

from pydantic import BaseModel, Field

from recommendation_engine.app.core.database.collections import PyObjectId
from recommendation_engine.app.recommendation.types import (
    TProductIdsFingerPrint,
    TRecommendationSubSequences,
    TProductIdsOrderedAndUnique,
)


class RecommendationModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)

    fingerprint: TProductIdsFingerPrint = Field(..., description="SHA1 hash of the original sequence (unique)")
    sequence: TProductIdsOrderedAndUnique = Field(..., description="The original sequence of product_ids")
    subsequences: TRecommendationSubSequences = Field(..., description="All generated subsequences")
    createdAt: datetime = Field(..., description="Insertion timestamp in UTC")
