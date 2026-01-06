from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class DashboardPagePort(ABC, LoggingMixin):
    """
    Port for Dashboard navigation after login.
    Responsible for navigating to different sections from the main dashboard.
    """

    @abstractmethod
    async def open_foundations(self) -> None:
        """Navigate to Foundations from the dashboard (e.g., click on 'Foundations')."""
        ...

    @abstractmethod
    async def get_user_name(self) -> Optional[str]:
        """Get the user's name displayed on the dashboard."""
        ...
