from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    DB_DSN: str

    class Config:
        env_file = '.env'


config = Settings()  # type: ignore
