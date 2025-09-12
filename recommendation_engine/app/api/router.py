from fastapi import APIRouter

from recommendation_engine.app.api.controllers.index import IndexController

__all__ = ("get_router",)


def get_router() -> APIRouter:
    router = APIRouter()

    index_controller = IndexController()
    router.include_router(index_controller.router, tags=["Index"])
    return router
