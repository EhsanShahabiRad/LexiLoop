from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str
    api_v1_str: str
    debug: bool

    database_url: str

    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
