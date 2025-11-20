"""
Lesson-specific patterns for Fluency Builder flows.
"""

from dataclasses import dataclass

from rosseta_stone_script_a.shared.utils.compile_case_insensitive import (
    compile_case_insensitive,
)

cci = compile_case_insensitive


@dataclass(frozen=True)
class LessonPatterns:
    """Patterns for lesson management and navigation."""

    # Fluency Builder navigation
    FOUNDATIONS = cci(r"foundations|fundamentos")



    LAUNCH_COURSE_BUTTON = "LaunchCourseButton"
