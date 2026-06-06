from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    url: str = Field(default="redis://redis:6379/0", validation_alias="REDIS_URL")
    status_ttl_seconds: int = Field(
        default=5, validation_alias="REDIS_STATUS_TTL_SECONDS"
    )

    model_config = SettingsConfigDict(
        env_file="environments/redis.env",
        extra="ignore",
    )


redis_settings = RedisSettings()
