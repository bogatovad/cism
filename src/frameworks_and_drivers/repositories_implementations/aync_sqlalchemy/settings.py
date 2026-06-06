from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str = Field(default="cism", validation_alias="POSTGRES_USER")
    password: str = Field(default="password", validation_alias="POSTGRES_PASSWORD")
    db: str = Field(default="cism", validation_alias="POSTGRES_DB")
    host: str = Field(default="pgbouncer", validation_alias="POSTGRES_HOST")
    port: int = Field(default=6432, validation_alias="POSTGRES_PORT")
    direct_host: str = Field(default="db", validation_alias="POSTGRES_DIRECT_HOST")
    direct_port: int = Field(default=5432, validation_alias="POSTGRES_DIRECT_PORT")
    echo: bool = Field(default=False, validation_alias="DATABASE_ECHO")
    pool_size: int = Field(default=10, validation_alias="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=5, validation_alias="DATABASE_MAX_OVERFLOW")

    model_config = SettingsConfigDict(
        env_file="environments/db.env",
        extra="ignore",
    )

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    @property
    def alembic_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.direct_host}:{self.direct_port}/{self.db}"
        )


database_settings = DatabaseSettings()
