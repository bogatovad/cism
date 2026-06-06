from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenRouterSettings(BaseSettings):
    api_key: str = Field(validation_alias="OPENROUTER_API_KEY")
    site_url: str = Field(
        default="http://localhost",
        validation_alias="OPENROUTER_SITE_URL",
    )
    site_name: str = Field(default="cism", validation_alias="OPENROUTER_SITE_NAME")
    model: str = Field(
        default="openrouter/owl-alpha",
        validation_alias="OPENROUTER_MODEL",
    )

    model_config = SettingsConfigDict(
        env_file="environments/web.env",
        extra="ignore",
    )


openrouter_settings = OpenRouterSettings()
