from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    NAME: str
    USERNAME_BOT: str
    BOT_TOKEN: str
    ID_BOT: str
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
   
    DATABASE_URL: str           # асинхронный для SQLAlchemy + asyncpg
    DATABASE_URL_SYNC: str      # синхронный для Alembic
    
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    NOTIFICATION_EMAIL: str
    
    RECIPIENT_IDS: str
    
    class Config:
        env_file = ".env"


settings = Settings()