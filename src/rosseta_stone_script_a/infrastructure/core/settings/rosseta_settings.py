from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RosettaSettings(BaseSettings):
    rosetta_base_url: str = "https://www.rosettastone.com"
    rosetta_login_url: str = "https://login.rosettastone.com/login"
    rosetta_email: str | None = None
    rosetta_password: str | None = None
    rosetta_units_to_complete: List[int] = []

    # Progress and timing settings
    rosetta_target_score_percent: int = 100
    rosetta_max_start_time_offset_ms: int = 432000000  # ~5 days
    rosetta_inter_path_delay_ms: int = 500

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("rosetta_units_to_complete", mode="before")
    @classmethod
    def parse_units_to_complete(cls, v: Union[str, List[int]]) -> List[int]:
        if isinstance(v, str):
            if not v.strip():
                return []
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v
