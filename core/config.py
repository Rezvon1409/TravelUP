from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str = 'sqlite:///./TravelUp.db'
    SECRET_KEY : str = 'Rezvon0880'
    ALGORITHM : str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
    REFRESH_TOKEN_EXPIRE_DAYS : int = 7

    class Config:
        env_file = '.env'

settings = Settings()

