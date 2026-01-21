from typing import List

from rosseta_stone_script_a.domain.entities.lesson import Lesson
from rosseta_stone_script_a.domain.entities.path import Path
from rosseta_stone_script_a.domain.entities.unit import Unit
from rosseta_stone_script_a.shared.mixins.loggin_mixin import LoggingMixin


class ContentFilter(LoggingMixin):
    """Service for filtering units, lessons, and paths based on configuration."""

    def __init__(
        self,
        units_to_complete: List[int] = None,
        lessons_to_complete: List[int] = None,
        path_types_to_complete: List[str] = None,
    ):
        self.units_to_complete = units_to_complete or []
        self.lessons_to_complete = lessons_to_complete or []
        self.path_types_to_complete = path_types_to_complete or []

    def should_process_unit(self, unit: Unit) -> bool:
        """Check if a unit should be processed based on configuration."""
        if not self.units_to_complete:
            return True
        return unit.unit_number in self.units_to_complete

    def should_process_lesson(self, lesson: Lesson) -> bool:
        """Check if a lesson should be processed based on configuration."""
        if not self.lessons_to_complete:
            return True
        return lesson.lesson_number in self.lessons_to_complete

    def should_process_path(self, path: Path) -> bool:
        """Check if a path should be processed based on configuration and completion status."""
        # Skip if already complete
        if path.complete:
            return False

        # Check path type filter
        if not self.path_types_to_complete:
            return True
        return path.type in self.path_types_to_complete

    def log_skip_reason(
        self, item_type: str, item_identifier: str | int, reason: str
    ) -> None:
        """Log why an item was skipped."""
        self.logger.debug(f"Skipping {item_type} {item_identifier} ({reason})")
