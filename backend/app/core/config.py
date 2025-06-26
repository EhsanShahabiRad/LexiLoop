from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str
    debug: bool
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_v1_str: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
