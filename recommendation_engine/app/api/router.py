from fastapi import APIRouter

from recommendation_engine.app.api.controllers.auth import AuthController
from recommendation_engine.app.api.controllers.index import IndexController
from recommendation_engine.app.api.controllers.recommendation import RecommendationController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])

    api_v1 = APIRouter(prefix="/api/v1")

    auth_controller = AuthController()
    api_v1.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])

    recommendation_controller = RecommendationController()
    api_v1.include_router(recommendation_controller.router, prefix="/recommendations", tags=["Recommendations"])

    router.include_router(api_v1)
    return router
