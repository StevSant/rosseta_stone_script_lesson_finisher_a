from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from rosseta_stone_script_a.shared.mixins import LoggingMixin

if TYPE_CHECKING:
    from .widget_ports import (
        DragDropWidgetPort,
        MatchingWidgetPort,
        MultipleChoiceWidgetPort,
        RadioGroupWidgetPort,
    )


class WidgetFactory(ABC, LoggingMixin):
    """Factory for creating activity widgets based on detected UI."""

    @abstractmethod
    def multiple_choice(self) -> "MultipleChoiceWidgetPort":
        """Create a multiple choice widget for the current activity."""
        ...

    @abstractmethod
    def radio_group(self) -> "RadioGroupWidgetPort":
        """Create a radio group widget for the current activity."""
        ...

    @abstractmethod
    def drag_drop(self) -> "DragDropWidgetPort":
        """Create a drag and drop widget for the current activity."""
        ...

    @abstractmethod
    def matching(self) -> "MatchingWidgetPort":
        """Create a matching widget for the current activity."""
        ...


class LessonPlayerPagePort(ABC, LoggingMixin):
    """
    Port for the lesson player container.
    Handles player controls and provides widget factory for activity interactions.

    Note: This component is maintained for backward compatibility.
    For new implementations, consider using ActivityPlayerPagePort which better
    reflects the Course → Lesson → Activity hierarchy by operating at the Activity level.
    """

    @property
    @abstractmethod
    def widgets(self) -> WidgetFactory:
        """Access to widget factory for current activity."""
        ...

    # Player controls
    @abstractmethod
    async def continue_without_voice(self) -> None:
        """Continue without voice features ('Continuar sin voz')."""
        ...

    @abstractmethod
    async def exit_lesson(self) -> None:
        """Exit the current lesson ('Salir de la lección')."""
        ...

    @abstractmethod
    async def next_activity(self) -> None:
        """Move to next activity ('Próxima actividad')."""
        ...

    @abstractmethod
    async def review_answer(self) -> None:
        """Review the answer ('Revisar respuesta')."""
        ...

    @abstractmethod
    async def skip_activity(self) -> None:
        """Skip current activity ('Omitir')."""
        ...

    # Optional features
    @abstractmethod
    async def open_explanation(self) -> None:
        """Open explanation if available."""
        ...

    @abstractmethod
    async def open_objectives(self) -> None:
        """Open objectives if available."""
        ...
