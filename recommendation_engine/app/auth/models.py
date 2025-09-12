from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccessToken:
    access_token: str = field(repr=False)
    username: str
    expires: float
