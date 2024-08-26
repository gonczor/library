from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str = Field(..., alias="POSTGRES_DB")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_password: str = Field(..., alias="POSTGRES_PASSWORD")
    db_port: int = Field(..., alias="POSTGRES_PORT")
    db_host: str = Field(..., alias="POSTGRES_HOST")


@lru_cache()
def get_settings():
    return Settings()
