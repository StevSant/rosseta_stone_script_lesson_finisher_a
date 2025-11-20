from pydantic_settings import BaseSettings

from .settings import BrowserSettings, RosettaSettings


class Settings(BaseSettings):
    rosseta_settings: RosettaSettings = RosettaSettings()
    browser_settings: BrowserSettings = BrowserSettings()


settings = Settings()
