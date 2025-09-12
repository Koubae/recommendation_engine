from recommendation_engine.app.auth.access_token import JWTAccessTokenAuth, HashLibPasswordHasher
from recommendation_engine.app.auth.exceptions import AuthPasswordInvalid, AuthUsernameInvalid
from recommendation_engine.app.auth.models import AccessToken
from recommendation_engine.settings import Settings


class AuthService:
    def __init__(
        self,
        password_hasher: HashLibPasswordHasher,
        auth: JWTAccessTokenAuth,
    ):
        self.password_hasher: HashLibPasswordHasher = password_hasher
        self.auth: JWTAccessTokenAuth = auth
        self.settings: Settings = Settings.get()

    async def login(self, username: str, password: str) -> AccessToken:
        """
        Raises:
            - AuthUsernameInvalid: If username is incorrect.
            - AuthPasswordInvalid: If password is incorrect.
        """
        admin_username = self.settings.app_admin_username
        if username != admin_username:
            raise AuthUsernameInvalid()

        password_hash = self.settings.app_admin_password_hash
        password_match = self.password_hasher.verify_password(password, password_hash)
        if not password_match:
            raise AuthPasswordInvalid()

        access_token = self.auth.generate_access_token(1, username)
        return access_token
