from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class UnitLessonsPagePort(ABC, LoggingMixin):
    """
    Port for lessons within a specific unit.
    Handles lesson selection and management within a unit.
    """

    @abstractmethod
    async def select_lesson(self, lesson_name_or_index: Union[str, int]) -> None:
        """Select a lesson by text or index."""
        ...

    @abstractmethod
    async def start_lesson(self) -> None:
        """Start the selected lesson."""
        ...

    @abstractmethod
    async def resume_lesson(self) -> None:
        """Resume the selected lesson."""
        ...
