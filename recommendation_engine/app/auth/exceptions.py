class AuthCertificateLoadException(Exception):
    pass


class AuthError(Exception):
    pass


class AuthAccessTokenInvalid(AuthError):
    pass


class AuthAccessTokenExpired(AuthError):
    pass


class AuthPasswordInvalid(AuthError):
    def __init__(self) -> None:
        super().__init__("Invalid password")
