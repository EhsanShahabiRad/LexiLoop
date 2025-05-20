from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "LexiLoop"
    debug: bool = True
    database_url: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    api_v1_str: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")



settings = Settings()
