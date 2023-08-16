from pydantic_settings import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str 
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"
        extra = Extra.forbid


settings = Settings()