from fastapi import APIRouter
from starlette.responses import HTMLResponse

from recommendation_engine.settings import Settings


class IndexController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/", endpoint=self.home, methods=["GET"])
        self.router.add_api_route(path="/ping", endpoint=self.ping, methods=["GET"])
        self.router.add_api_route(path="/alive", endpoint=self.alive, methods=["GET"])
        self.router.add_api_route(path="/ready", endpoint=self.ready, methods=["GET"])

    async def home(self) -> HTMLResponse:
        info = f"Welcome to {self.settings.get_app_info()}"
        info = info.replace("\n", "<br>")
        return HTMLResponse(content=info, status_code=200)

    @staticmethod
    async def ping() -> HTMLResponse:
        return HTMLResponse(
            content="pong",
            status_code=200,
        )

    @staticmethod
    async def alive() -> HTMLResponse:
        return HTMLResponse(
            content="OK",
            status_code=200,
        )

    @staticmethod
    async def ready() -> HTMLResponse:
        return HTMLResponse(
            content="OK",
            status_code=200,
        )
