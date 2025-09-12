from fastapi import APIRouter
from pydantic import BaseModel, Field

from recommendation_engine.app.api.providers import AuthServiceSingleton
from recommendation_engine.settings import Settings


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)


class LoginResponse(BaseModel):
    access_token: str
    expires: float


class AuthController:
    def __init__(self) -> None:
        self.router: APIRouter = APIRouter()
        self.settings: Settings = Settings.get()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(path="/login", endpoint=self.login, methods=["POST"])

    @staticmethod
    async def login(
        request: LoginRequest,
        auth_service: AuthServiceSingleton,
    ) -> LoginResponse:
        print(request)
        print(auth_service)
        response = LoginResponse(access_token="dummy", expires=0.0)
        return response
