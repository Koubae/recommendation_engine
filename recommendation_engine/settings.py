import os
import typing as t
from dataclasses import dataclass


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

    app_admin_username: str
    app_admin_password: str

    @classmethod
    def get(cls) -> "Settings":
        if cls._singleton is None:
            cls._singleton = cls(
                log_level=os.getenv("LOG_LEVEL", "DEBUG"),
                log_format=os.getenv("LOG_FORMAT", "%(asctime)s %(message)s"),
                app_name=os.getenv("APP_NAME", "Recommendation Engine"),
                app_version=os.getenv("APP_VERSION", "undefined"),
                app_api_cors_allowed_domains=tuple(os.environ.get("APP_API_CORS_ALLOWED_DOMAINS", "").split(",")),

                app_admin_username=os.getenv("APP_ADMIN_USERNAME", "admin"),
                app_admin_password=os.getenv("APP_ADMIN_PASS", "admin"),
            )
        return cls._singleton

    def get_app_info(self) -> str:
        info = f"{self.app_name} V{self.app_version}!"
        return info

    @staticmethod
    def parse_bool_env(env_name: str, default: bool = False) -> bool:
        return os.getenv(env_name, str(default)).lower() in ("true", "1")
