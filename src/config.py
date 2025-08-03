from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(..., env="JWT_ALGORITHM")
    

    model_config = SettingsConfigDict(
        env_file=".env",  # Specify the .env file to load environment variables from
        extra="ignore",  # Ignore any extra fields not defined in the model
      
    )

Config = Settings()

# This config file uses Pydantic to load environment variables from a .env file.
# The DATABASE_URL variable is required and will be loaded from the .env file.
# You can add more settings as needed, and they will be automatically loaded from the .env file.
# The Config class specifies the .env file to use and its encoding.
# Make sure to create a .env file in the same directory as this config.py file with the DATABASE_URL variable defined.
# Example .env file content:
# DATABASE_URL=postgresql+asyncpg://bookly_admin:admin123@localhost:5432/bookly_db
# You can also add other settings like SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES as needed.
# Example:
# SECRET_KEY=your-secret-key-here               