import logging
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, conlist

from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.app.auth.secure import LoggedIn
from recommendation_engine.app.providers import RecommendationRepositorySingleton
from recommendation_engine.app.recommendation.algorithm import (
    generate_recommendation_subsequences,
    generate_product_ids_fingerprint,
)
from recommendation_engine.app.recommendation.models import RecommendationModel
from recommendation_engine.app.recommendation.repository import (
    RecommendationRepositoryException,
    RecommendationDuplicate,
)
from recommendation_engine.app.recommendation.types import (
    TProductIdsFingerPrint,
    TProductIdsOrderedAndUnique,
    TRecommendationSubSequences,
)
from recommendation_engine.settings import Settings

logger = logging.getLogger(__name__)


class CreateRequest(BaseModel):
    product_ids: conlist(int, min_length=1) = Field(..., description="Sequence of product IDs")


class ListResponse(BaseModel):
    sequence: TProductIdsOrderedAndUnique
    subsequences: TRecommendationSubSequences


class RecommendationResponse(BaseModel):
    fingerprint: TProductIdsFingerPrint
    sequence: list[int]
    subsequences: list[list[int]]
    createdAt: datetime


class RecommendationController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/{recommendation_id}", endpoint=self.show, methods=["GET"])
        self.router.add_api_route(path="/", endpoint=self.create, methods=["POST"], status_code=status.HTTP_201_CREATED)
        self.router.add_api_route(path="/", endpoint=self.list, methods=["GET"])

    @staticmethod
    async def show(
        recommendation_id: str,
        repository: RecommendationRepositorySingleton,
        _: AccessToken = Depends(LoggedIn),
    ) -> RecommendationModel:
        if not ObjectId.is_valid(recommendation_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        try:
            document = await repository.get(recommendation_id)
        except RecommendationRepositoryException as _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error, please try again later...",
            )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recommendation subsequence of {recommendation_id} not found",
            )
        return document

    @staticmethod
    async def create(
        payload: CreateRequest,
        repository: RecommendationRepositorySingleton,
        _: AccessToken = Depends(LoggedIn),
    ) -> RecommendationModel:
        unique_ordered_product_ids, recommendations = generate_recommendation_subsequences(payload.product_ids)
        fingerprint = generate_product_ids_fingerprint(unique_ordered_product_ids)

        try:
            document = await repository.create(fingerprint, unique_ordered_product_ids, recommendations)
        except RecommendationDuplicate as _:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Product_ids {unique_ordered_product_ids} (fingerprint={fingerprint}) Already exists",
            )
        except RecommendationRepositoryException as _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error, please try again later...",
            )

        logger.info(f"Created recommendation document: {document}, sequence: {unique_ordered_product_ids}")
        return document

    @staticmethod
    async def list(
        repository: RecommendationRepositorySingleton,
        _: AccessToken = Depends(LoggedIn),
    ) -> list[ListResponse]:
        try:
            documents = await repository.paginate(limit=10)
        except RecommendationRepositoryException as _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error, please try again later...",
            )

        response = [
            ListResponse(sequence=document.sequence, subsequences=document.subsequences)
            for document in documents
        ]
        return response
