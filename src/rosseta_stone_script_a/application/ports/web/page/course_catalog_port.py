from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class CourseCatalogPagePort(ABC, LoggingMixin):
    """
    Port for the course catalog/listing page.
    Handles browsing and selecting courses in Fluency Builder.
    """

    @abstractmethod
    async def select_course(self, course_name_or_pattern: Union[str, object]) -> None:
        """Select a course from the catalog by name or pattern."""
        ...
