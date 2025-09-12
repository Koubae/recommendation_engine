import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from recommendation_engine.app.api.providers import AuthServiceSingleton
from recommendation_engine.app.auth.exceptions import AuthPasswordInvalid, AuthUsernameInvalid
from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.settings import Settings

logger = logging.getLogger(__name__)


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
        try:
            access_token: AccessToken = await auth_service.login(request.username, request.password)
        except (AuthUsernameInvalid, AuthPasswordInvalid) as error:
            logger.info(
                f"Login failed, invalid password for account {request.username}: {repr(error)}",
                extra={"extra": {"username": request.username}},
            )
            raise HTTPException(
                status_code=401,
                detail={"error": "Username or Password is incorrect!"},
            )

        return LoginResponse(
            access_token=access_token.access_token,
            expires=access_token.expires,
        )
