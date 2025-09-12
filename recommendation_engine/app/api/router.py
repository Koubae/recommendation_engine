from fastapi import APIRouter

from recommendation_engine.app.api.controllers.auth import AuthController
from recommendation_engine.app.api.controllers.dummy import DummyController
from recommendation_engine.app.api.controllers.index import IndexController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])

    api_v1 = APIRouter(prefix="/api/v1")

    auth_controller = AuthController()
    api_v1.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])

    dummy_controller = DummyController()
    api_v1.include_router(dummy_controller.router, prefix="/dummy", tags=["Dummy"])

    router.include_router(api_v1)
    return router
