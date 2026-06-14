from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    debug: bool = False
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-haiku-4-5"
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()