from pydantic_settings import BaseSettings, SettingsConfigDict  

class Settings(BaseSettings):
    APP_NAME: str="KILIMOSOKO"
    APP_ENV: str="development"
    DEBUG: bool=True
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30
    
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings=Settings()