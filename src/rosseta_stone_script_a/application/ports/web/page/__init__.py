"""Page-specific ports for web application interfaces."""

from .activity_catalog_port import ActivityCatalogPagePort
from .activity_player_port import ActivityPlayerPagePort, WidgetFactory
from .auth_port import AuthPort
from .course_catalog_port import CourseCatalogPagePort
from .dashboard_port import DashboardPagePort
from .lesson_catalog_port import LessonCatalogPagePort
from .lesson_player_port import LessonPlayerPagePort
from .unit_catalog_port import UnitCatalogPagePort
from .unit_lessons_port import UnitLessonsPagePort
from .widget_ports import (
    DragContext,
    DragDropWidgetPort,
    MatchingWidgetPort,
    MultipleChoiceWidgetPort,
    RadioGroupWidgetPort,
)

__all__ = [
    "AuthPort",
    "ActivityCatalogPagePort",
    "ActivityPlayerPagePort",
    "CourseCatalogPagePort",
    "DashboardPagePort",
    "LessonCatalogPagePort",
    "UnitCatalogPagePort",
    "UnitLessonsPagePort",
    "LessonPlayerPagePort",  # Keep for backward compatibility during transition
    "WidgetFactory",
    "MultipleChoiceWidgetPort",
    "RadioGroupWidgetPort",
    "DragDropWidgetPort",
    "MatchingWidgetPort",
    "DragContext",
]
