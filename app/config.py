from urllib.parse import quote_plus

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    api_v1_prefix: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_value(cls, value: bool | str) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release"}:
                return False
        raise ValueError("DEBUG must be a boolean-compatible value")

    @computed_field
    @property
    def database_url(self) -> str:
        quoted_password = quote_plus(self.db_password)
        return (
            f"mysql+aiomysql://{self.db_user}:{quoted_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )


settings = Settings()
