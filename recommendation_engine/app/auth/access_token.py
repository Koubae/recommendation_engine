import hashlib
import logging
import typing as t
from datetime import UTC, datetime, timedelta

import jwt

from recommendation_engine.app.auth.exceptions import AuthAccessTokenExpired, AuthAccessTokenInvalid
from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.settings import Settings


logger = logging.getLogger(__name__)


class HashLibPasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.hash_password(plain_password) == hashed_password


class JWTAccessTokenAuth:
    JWT_ALGORITHM: t.ClassVar[str] = "RS256"

    def generate_access_token(self, user_id: int, username: str) -> AccessToken:
        settings = Settings.get()
        expires_seconds = (datetime.now(UTC) + timedelta(hours=settings.app_jwt_expiration_hours)).timestamp()
        payload = {
            "sub": str(user_id),
            "exp": expires_seconds,
            "iat": datetime.now(UTC),
            "username": username,
        }
        cert = settings.get_cert_private()
        token = jwt.encode(payload, cert, algorithm=self.JWT_ALGORITHM)
        access_token = AccessToken(
            username=username,
            expires=expires_seconds,
            access_token=token,
        )
        return access_token

    def parse_access_token(self, access_token: str) -> AccessToken:
        settings = Settings.get()
        try:
            payload = jwt.decode(
                access_token,
                settings.get_cert_public(),
                algorithms=[self.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError as error:
            logger.debug(
                "Access-Token expired",
                extra={"extra": {"access_token": access_token, "error": repr(error)}},
            )
            raise AuthAccessTokenExpired("Token expired")
        except jwt.InvalidTokenError as error:
            logger.info(
                "Invalid Access-Token",
                extra={"extra": {"access_token": access_token, "error": repr(error)}},
            )
            raise AuthAccessTokenInvalid("Invalid token")

        try:
            username: str = payload["username"]
            expires: int = payload["exp"]
        except KeyError as error:
            logger.warning(
                f"Invalid Access-Token while parsing, error: {error}",
                extra={
                    "extra": {
                        "access_token": access_token,
                        "payload": payload,
                        "error": repr(error),
                    }
                },
            )
            raise AuthAccessTokenInvalid(f"Invalid token payload: {error}") from error

        return AccessToken(
            username=username,
            expires=expires,
            access_token=access_token,
        )
