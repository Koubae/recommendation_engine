# pragma: no cover
import typing as t

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from recommendation_engine.app.auth.access_token import JWTAccessTokenAuth
from recommendation_engine.app.auth.exceptions import AuthAccessTokenExpired, AuthAccessTokenInvalid
from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.app.providers import provide_access_token_auth

security = HTTPBearer()


def restrict() -> t.Callable[
    [HTTPAuthorizationCredentials, JWTAccessTokenAuth], t.Coroutine[t.Any, t.Any, AccessToken]
]:
    """Create a FastAPI dependency for JWT authentication with role checking.

    Validates an Authorization header with the following Structure:

            Authorization: Bearer deadbeef12346

    Raises:
        - AuthAccessTokenInvalid: if the access token is invalid
        - AuthAccessTokenInvalid: if the access token is expired
        - HTTPException: if the user role is not allowed to access the endpoint
    """

    async def _(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        jwt_auth: JWTAccessTokenAuth = Depends(provide_access_token_auth),
    ) -> AccessToken:
        try:
            access_token = jwt_auth.parse_access_token(credentials.credentials)
        except AuthAccessTokenExpired:
            raise HTTPException(status_code=401, detail="Token has expired")
        except AuthAccessTokenInvalid:
            raise HTTPException(status_code=401, detail="Invalid token")

        return access_token

    return _


LoggedIn = restrict()
