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
    FLUENCY_BUILDER = cci(r"fluency\s+builder|constructor\s+de\s+fluidez")

    # Course actions
    RESUME = cci(r"^(reanudar|resume)$")
    START = cci(r"^(iniciar lecci[óo]n|start (new )?lesson)$")
    EXIT = cci(r"^(salir de la lecci[óo]n|exit lesson|leave lesson)$")

    # Navigation patterns
    COURSE_PATTERN = cci(r"curso\s*\d+|course\s*\d+|mis\s+cursos|my\s+courses")
    UNIT_PATTERN = cci(r"unit[oa]?\s*\d+|unidad\s*\d+")
    LESSON_PATTERN = cci(r"lesson\s*\d+|lecci[óo]n\s*\d+")
    ACTIVITY_PATTERN = cci(r"activity\s*\d+|actividad\s*\d+")

    LAUNCH_COURSE_BUTTON = "LaunchCourseButton"


@dataclass(frozen=True)
class PlayerPatterns:
    """Patterns for lesson player interactions."""

    # Player controls
    CONTINUE_NO_VOICE = cci(r"^continuar sin voz$")
    NEXT_ACTIVITY = cci(r"^(pr[óo]xima actividad|next activity)$")
    REVIEW_ANSWER = cci(r"^(revisar respuesta|review answer)$")
    SKIP = cci(r"^(omitir|skip)$")

    # Player state
    EXPLANATION = cci(r"^(explicaci[óo]n|explanation)$")
    OBJECTIVES = cci(r"^(objetivos|objectives)$")


@dataclass(frozen=True)
class ActivityPatterns:
    """Patterns for activity widget types."""

    # Widget types
    MULTIPLE_CHOICE = cci(r"multiple.choice|opci[óo]n.m[úu]ltiple")
    RADIO_GROUP = cci(r"radio.group|selecci[óo]n.[úu]nica")
    DRAG_DROP = cci(r"drag.drop|arrastrar.soltar")
    MATCHING = cci(r"matching|emparejar|asociar")

    # Activity actions
    CHOOSE_OPTION = cci(r"^(elegir|choose|select)$")
    DRAG_TO = cci(r"^(arrastrar a|drag to)$")
    MATCH_WITH = cci(r"^(emparejar con|match with)$")
