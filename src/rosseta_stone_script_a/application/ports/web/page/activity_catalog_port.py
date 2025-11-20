from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class ActivityCatalogPagePort(ABC, LoggingMixin):
    """
    Port for activities within a specific lesson.
    Handles activity selection and management within a lesson.
    """

    @abstractmethod
    async def select_activity(self, activity_name_or_index: Union[str, int]) -> None:
        """Select an activity by text or index."""
        ...

    @abstractmethod
    async def start_activity(self) -> None:
        """Start the selected activity."""
        ...

    @abstractmethod
    async def resume_activity(self) -> None:
        """Resume the selected activity."""
        ...

    @abstractmethod
    async def select_fluency_builder(self) -> None:
        """Select the Fluency Builder option from the main menu."""
        ...
