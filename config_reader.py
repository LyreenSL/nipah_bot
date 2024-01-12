from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, StrictStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_address: StrictStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
