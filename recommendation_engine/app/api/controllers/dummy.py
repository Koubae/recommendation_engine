import logging

from fastapi import APIRouter, Depends

from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.app.auth.secure import restrict
from recommendation_engine.settings import Settings

logger = logging.getLogger(__name__)


class DummyController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/dummy", endpoint=self.dummy, methods=["GET"])

    @staticmethod
    async def dummy(access_token: AccessToken = Depends(restrict())) -> dict:
        print("OK")
        print(access_token)
        return {"dummy": "OK"}
