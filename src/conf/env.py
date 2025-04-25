""" Environment configuration for the application. """

import os

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()

db_path = os.path.join(os.path.abspath(os.path.curdir), "pokemonle.db")

class Settings(BaseSettings):
    """ Settings class for manage environment variables. """

    DB_CONNECTION: str = Field(
        default= f"sqlite:///{db_path}",
        description="Database connection string"
    )

    PORT: int = Field(
        default=9000,
        description="Port for the application"
    )

    API_ONLY: bool = Field(
        default=False,
        description="API only mode"
    )


settings = Settings()