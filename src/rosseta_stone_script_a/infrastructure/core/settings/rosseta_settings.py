from pydantic_settings import BaseSettings, SettingsConfigDict


class RosettaSettings(BaseSettings):
    rosetta_base_url: str = "https://www.rosettastone.com"
    rosetta_login_url: str = "https://login.rosettastone.com/login"
    rosetta_email: str | None = None
    rosetta_password: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
