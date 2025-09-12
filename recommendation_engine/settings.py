import os
import typing as t
from dataclasses import dataclass, field

from recommendation_engine.app.auth.exceptions import AuthCertificateLoadException


@dataclass(frozen=True)
class Settings:
    """Singleton Instance for Application settings"""

    _singleton: t.ClassVar[t.Optional["Settings"]] = None

    ROOT_PATH: t.ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    CONF_PATH: t.ClassVar[str] = os.path.join(ROOT_PATH, "..", "conf")
    TESTS_PATH: t.ClassVar[str] = os.path.join(ROOT_PATH, "..", "tests")

    # ----------------------------
    #   App
    # ----------------------------
    log_level: str
    log_format: str
    app_name: str
    app_version: str
    app_api_cors_allowed_domains: tuple[str, ...]
    app_jwt_expiration_hours: int

    app_admin_username: str
    app_admin_password_hash: str

    # Auth
    cert_private_file_name: str | None = field(repr=False)
    cert_public_file_name: str | None = field(repr=False)

    cert_private: str | None = field(default=None, repr=False)
    cert_public: str | None = field(default=None, repr=False)

    @classmethod
    def get(cls) -> "Settings":
        if cls._singleton is None:
            cert_private_file_name = os.getenv("APP_CERT_PRIVATE_FILE_NAME", None)
            cert_public_file_name = os.getenv("APP_CERT_PUBLIC_FILE_NAME", None)
            if not cert_private_file_name or not cert_public_file_name:
                raise AuthCertificateLoadException("Certificate files not found")

            cert_private, cert_public = cls._load_certificates(cert_private_file_name, cert_public_file_name)
            app_jwt_expiration_hours = min(int(os.getenv("APP_JWT_EXPIRATION_HOURS", 4)), 1)

            cls._singleton = cls(
                log_level=os.getenv("LOG_LEVEL", "DEBUG"),
                log_format=os.getenv("LOG_FORMAT", "%(asctime)s %(message)s"),
                app_name=os.getenv("APP_NAME", "Recommendation Engine"),
                app_version=os.getenv("APP_VERSION", "undefined"),
                app_api_cors_allowed_domains=tuple(os.environ.get("APP_API_CORS_ALLOWED_DOMAINS", "").split(",")),
                app_jwt_expiration_hours=app_jwt_expiration_hours,

                app_admin_username=os.getenv("APP_ADMIN_USERNAME", "admin"),
                app_admin_password_hash=os.getenv("APP_ADMIN_PASS_HASH", "admin"),
                cert_private_file_name=cert_private_file_name,
                cert_public_file_name=cert_public_file_name,
                cert_private=cert_private,
                cert_public=cert_public,
            )
        return cls._singleton

    def get_app_info(self) -> str:
        info = f"{self.app_name} V{self.app_version}!"
        return info

    @staticmethod
    def parse_bool_env(env_name: str, default: bool = False) -> bool:
        return os.getenv(env_name, str(default)).lower() in ("true", "1")

    def get_cert_public(self) -> str:
        return self.cert_public

    def get_cert_private(self) -> str:
        return self.cert_private

    @classmethod
    def _load_certificates(
        cls, cert_private_file_name: str | None, cert_public_file_name: str | None,
    ) -> tuple[str | None, str | None]:
        cert_private: str | None = None
        cert_public: str | None = None

        cert_private_file_name = cert_private_file_name.strip() if cert_private_file_name else None
        cert_public_file_name = cert_public_file_name.strip() if cert_public_file_name else None

        if cert_private_file_name:
            cert_private = cls._load_cert(cert_private_file_name)
        if cert_public_file_name:
            cert_public = cls._load_cert(cert_public_file_name)
        return cert_private, cert_public

    @classmethod
    def _load_cert(cls, cert_file_name: str) -> str:
        try:
            with open(os.path.join(cls.CONF_PATH, cert_file_name), "r") as f:
                certificate = f.read()
        except (FileNotFoundError, PermissionError, UnicodeError) as error:
            raise AuthCertificateLoadException(f"Could not load certificate file {cls}: {error}") from error

        certificate = certificate.strip()
        if not certificate:
            raise AuthCertificateLoadException(f"Certificate file {cert_file_name} is empty")
        return certificate
