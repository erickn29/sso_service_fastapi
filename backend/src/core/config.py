from pathlib import Path

from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_HOSTS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://ssofront:3000",
]


class MainConfig(BaseSettings):
    debug: bool = False
    secret_key: str = "123"
    frontend_url: str = "http://localhost:3000"


class AuthConfig(BaseSettings):
    access_token_expire: int = 60 * 5
    refresh_token_expire: int = 60 * 60 * 24 * 15
    recovery_token_expire: int = 60 * 60 * 24
    token_type: str = "Bearer"
    algorithm: str = "HS256"
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DatabaseConfig(BaseSettings):
    driver: str = "asyncpg"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 600
    pool_pre_ping: bool = True

    @property
    def url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class RedisConfig(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

    @property
    def url_broker(self) -> str:
        return f"redis://{self.host}:{self.port}/11"

    @property
    def url_backend(self) -> str:
        return f"redis://{self.host}:{self.port}/12"


class EmailConfig(BaseSettings):
    host: str = "smtp.gmail.com"
    user: str = "main@gmail.com"
    password: str = "aaaa bbbb cccc dddd"
    port: int = 465


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).resolve().parent.parent.parent}/secrets/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="ignore",
    )
    app: MainConfig = MainConfig()
    auth: AuthConfig = AuthConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    email: EmailConfig = EmailConfig()


config = Config()
