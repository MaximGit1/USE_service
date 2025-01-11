from dataclasses import dataclass
from datetime import timedelta
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class JWTConfig:
    private_key: str
    public_key: str
    algorithm: str
    access_token_expire_minutes: timedelta


@dataclass(frozen=True)
class CookieConfig:
    access_token_key: str
    max_age_days: int


@dataclass(frozen=True)
class Config:
    jwt: JWTConfig
    cookie: CookieConfig


def create_cookie_config() -> CookieConfig:
    env_not_loaded = "Virtual environment variables not loaded."

    access_token_key = getenv("JWT_ACCESS_TOKEN_KEY")
    max_age_days_str = getenv("COOKIE_MAX_AGE_DAYS")

    if access_token_key is None or max_age_days_str is None:
        raise ValueError(env_not_loaded) from None

    try:
        max_age_days = int(max_age_days_str)
        max_age_days *= 24 * 60 * 60
    except ValueError:
        exception_msg = "max_age_days is not number."
        raise ValueError(exception_msg) from None

    return CookieConfig(
        access_token_key=access_token_key,
        max_age_days=max_age_days,
    )


def create_config() -> Config:
    base_path: Path = Path.cwd().parent.parent

    private_key_path = getenv("PRIVATE_KEY_PATH")
    public_key_path = getenv("PUBLIC_KEY_PATH")
    algorithm = getenv("ALGORITHM")
    access_token_expire_minutes_str = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    if (
        not private_key_path
        or not public_key_path
        or not algorithm
        or not access_token_expire_minutes_str
    ):
        error_msg = "Environment variables not loaded or missing."
        raise ValueError(error_msg)

    try:
        access_token_expire_minutes = int(access_token_expire_minutes_str)
    except ValueError:
        error_msg = "token expire minutes must be an integer."
        raise ValueError(error_msg) from None

    return Config(
        jwt=JWTConfig(
            private_key=base_path.joinpath(private_key_path).read_text(),
            public_key=base_path.joinpath(public_key_path).read_text(),
            algorithm=algorithm,
            access_token_expire_minutes=timedelta(
                minutes=access_token_expire_minutes
            ),
        ),
        cookie=create_cookie_config(),
    )
