from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    agent_api_key: SecretStr | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
