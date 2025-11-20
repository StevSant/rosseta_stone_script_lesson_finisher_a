from .activity_catalog_page import ActivityCatalogPage
from .activity_player_page import ActivityPlayerPage, PlaywrightWidgetFactory
from .course_catalog_page import CourseCatalogPage
from .dashboard_page import DashboardPage
from .lesson_catalog_page import LessonCatalogPage
from .lesson_player_page import LessonPlayerPage
from .login_page import LoginPage
from .unit_catalog_page import UnitCatalogPage
from .unit_lessons_page import UnitLessonsPage
from .widgets import (
    DragDropWidget,
    MatchingWidget,
    MultipleChoiceWidget,
    PlaywrightDragContext,
    RadioGroupWidget,
)

__all__ = [
    "LoginPage",
    "ActivityCatalogPage",
    "ActivityPlayerPage",
    "CourseCatalogPage",
    "DashboardPage",
    "LessonCatalogPage",
    "UnitCatalogPage",
    "UnitLessonsPage",
    "LessonPlayerPage",  # Keep for backward compatibility during transition
    "PlaywrightWidgetFactory",
    "MultipleChoiceWidget",
    "RadioGroupWidget",
    "DragDropWidget",
    "MatchingWidget",
    "PlaywrightDragContext",
]
