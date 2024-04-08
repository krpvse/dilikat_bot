from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_ID: int
    TELEGRAM_NOTIFICATION_ID: int

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    CATALOG_UPDATING_INTERVAL: int = 3600  # 3600 sec = 1 hour
    CATALOG_CACHE_EXPIRE_TIME: int = 600000  # 600 000 ms = 10 min

    EMAIL_NOTIFICATION_FROM_LOGIN: str
    EMAIL_NOTIFICATION_FROM_PASSWORD: str
    EMAIL_NOTIFICATION_TO: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def DATABASE_URL(cls):
        return f'postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}'


settings = Settings()
