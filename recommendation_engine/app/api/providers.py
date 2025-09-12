from functools import cache
from typing import Annotated

from fastapi import Depends

from recommendation_engine.app.auth.access_token import HashLibPasswordHasher, JWTAccessTokenAuth
from recommendation_engine.app.auth.service import AuthService


@cache
def auth_service() -> AuthService:
    service = AuthService(
        password_hasher=HashLibPasswordHasher(),
        auth=JWTAccessTokenAuth(),
    )
    return service


AuthServiceSingleton = Annotated[AuthService, Depends(auth_service)]
