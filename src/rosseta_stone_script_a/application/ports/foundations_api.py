from abc import ABC, abstractmethod
from typing import Any, Dict

from rosseta_stone_script_a.domain.entities.foundations import CourseMenu


class FoundationsApiPort(ABC):
    """Port for interacting with Rosetta Stone Foundations API."""

    @abstractmethod
    async def get_course_menu(
        self, authorization: str, language_code: str
    ) -> CourseMenu:
        """Fetch the course menu structure."""
        ...

    @abstractmethod
    async def update_path_score(
        self,
        session_token: str,
        school_id: str,
        user_id: str,
        course: str,
        unit_index: int,
        lesson_index: int,
        path_type: str,
        score_correct: int,
        score_incorrect: int,
        duration_ms: int,
        timestamp_ms: int,
        num_challenges: int,
    ) -> None:
        """Update the score/progress for a specific path (activity)."""
        ...
