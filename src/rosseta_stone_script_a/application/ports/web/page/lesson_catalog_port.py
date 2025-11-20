from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class LessonCatalogPagePort(ABC, LoggingMixin):
    """
    Port for lessons within a specific course.
    Handles lesson selection and management within a course.
    """

    @abstractmethod
    async def select_lesson(self, lesson_name_or_index: Union[str, int]) -> None:
        """Select a lesson by text or index."""
        ...
