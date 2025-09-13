from recommendation_engine.app.auth.access_token import HashLibPasswordHasher, JWTAccessTokenAuth
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
        """Authenticates a user by their username and password.

        Verifies the provided credentials against the stored administrator
        credentials and generates an access token if authentication
        succeeds. Only the administrator account is supported for login.


        Raises:
            AuthUsernameInvalid: If the provided username does not match the administrator username.
            AuthPasswordInvalid: If the provided password does not match the stored password hash for
                the administrator account.
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
