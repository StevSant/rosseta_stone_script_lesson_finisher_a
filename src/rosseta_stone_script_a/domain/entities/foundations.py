from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Path:
    unit_index: int
    lesson_index: int
    curriculum_lesson_index: int
    type: str
    course: str
    num_challenges: int
    time_estimate: int
    complete: bool
    percent_complete: int


@dataclass
class Lesson:
    id: str
    index: int
    lesson_number: int
    paths: List[Path]


@dataclass
class Unit:
    id: str
    index: int
    unit_number: int
    lessons: List[Lesson]


@dataclass
class CourseMenu:
    current_course_id: str
    units: List[Unit]
