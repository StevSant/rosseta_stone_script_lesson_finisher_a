from pydantic_settings import BaseSettings

from .settings import AgentSettings, BrowserSettings, RosettaSettings


class Settings(BaseSettings):
    rosseta_settings: RosettaSettings = RosettaSettings()
    browser_settings: BrowserSettings = BrowserSettings()
    agent_settings: AgentSettings = AgentSettings()


settings = Settings()
