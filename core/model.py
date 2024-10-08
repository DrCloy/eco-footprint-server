from dataclasses import dataclass, field


@dataclass
class AuthInput:
    username: str
    password: str


@dataclass
class AuthOutput:
    token: str
    expired: int
