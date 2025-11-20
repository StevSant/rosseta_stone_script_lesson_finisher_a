from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rosseta_stone_script_a.shared.mixins import LoggingMixin


class MultipleChoiceWidgetPort(ABC, LoggingMixin):
    """Port for multiple choice question widgets."""

    @abstractmethod
    async def choose_option(self, text_pattern: Union[str, object]) -> None:
        """Choose an option by text pattern."""
        ...


class RadioGroupWidgetPort(ABC, LoggingMixin):
    """Port for radio group widgets."""

    @abstractmethod
    async def choose(self, index_or_text: Union[int, str]) -> None:
        """Choose an option by index or text."""
        ...


class DragDropWidgetPort(ABC, LoggingMixin):
    """Port for drag and drop widgets."""

    @abstractmethod
    async def drag(self, source_text: Union[str, object]) -> "DragContext":
        """Start dragging from source text. Returns context for chaining with to()."""
        ...


class DragContext(ABC, LoggingMixin):
    """Context for completing drag operations."""

    @abstractmethod
    async def to(self, target_text: Union[str, object]) -> None:
        """Complete drag operation to target text."""
        ...


class MatchingWidgetPort(ABC, LoggingMixin):
    """Port for matching/pairing widgets."""

    @abstractmethod
    async def match(
        self, left_text: Union[str, object], right_text: Union[str, object]
    ) -> None:
        """Match left text with right text."""
        ...
