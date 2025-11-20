from __future__ import annotations

from typing import Union

from rosseta_stone_script_a.application.ports.web.control import Selector
from rosseta_stone_script_a.application.ports.web.page import (
    DragContext,
    DragDropWidgetPort,
    MatchingWidgetPort,
    MultipleChoiceWidgetPort,
    RadioGroupWidgetPort,
)
from rosseta_stone_script_a.application.ports.web.session import IWebSession


class MultipleChoiceWidget(MultipleChoiceWidgetPort):
    """Implementation of multiple choice widget."""

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

    async def choose_option(self, text_pattern: Union[str, object]) -> None:
        """Choose an option by text pattern."""
        self.logger.info(f"Choosing multiple choice option: {text_pattern}")
        # Try multiple selector strategies for options
        selectors = [
            Selector.role_button(text_pattern),
            Selector.role_checkbox(text_pattern),
            Selector.by_text(text_pattern),
        ]

        for i, selector in enumerate(selectors):
            self.logger.info(
                f"Trying selector strategy {i+1}/{len(selectors)} for multiple choice"
            )
            if await self.web_session.interactor.exists(selector, timeout=2000):
                self.logger.info("Found option element, clicking it")
                await self.web_session.interactor.click(selector)
                self.logger.info(f"Successfully chose option: {text_pattern}")
                return

        self.logger.error(f"Multiple choice option not found: {text_pattern}")
        raise RuntimeError(f"Multiple choice option not found: {text_pattern}")


class RadioGroupWidget(RadioGroupWidgetPort):
    """Implementation of radio group widget."""

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

    async def choose(self, index_or_text: Union[int, str]) -> None:
        """Choose an option by index or text."""
        self.logger.info(f"Choosing radio option: {index_or_text}")
        if isinstance(index_or_text, int):
            # Find radio buttons and select by index
            self.logger.info(f"Selecting radio by index: {index_or_text}")
            radio_selector = Selector.role_radio(".*")  # Match any radio
            if await self.web_session.interactor.exists(radio_selector, timeout=3000):
                radio_elements = await self.web_session.interactor.find(radio_selector)
                await radio_elements.nth(index_or_text).click()
                self.logger.info(
                    f"Successfully chose radio option at index: {index_or_text}"
                )
                return
        else:
            # Select by text
            self.logger.info(f"Selecting radio by text: {index_or_text}")
            text_selector = Selector.role_radio(index_or_text)
            if await self.web_session.interactor.exists(text_selector, timeout=2000):
                await self.web_session.interactor.click(text_selector)
                self.logger.info(f"Successfully chose radio option: {index_or_text}")
                return

        self.logger.error(f"Radio option not found: {index_or_text}")
        raise RuntimeError(f"Radio option not found: {index_or_text}")


class PlaywrightDragContext(DragContext):
    """Playwright-specific drag context implementation."""

    def __init__(self, web_session: IWebSession, source_element) -> None:
        super().__init__()
        self.web_session = web_session
        self.source_element = source_element

    async def to(self, target_text: Union[str, object]) -> None:
        """Complete drag operation to target text."""
        self.logger.info(f"Completing drag operation to target: {target_text}")
        target_selector = Selector.by_text(target_text)
        if await self.web_session.interactor.exists(target_selector, timeout=2000):
            target_element = await self.web_session.interactor.find(target_selector)
            # Perform drag and drop
            self.logger.info("Performing drag and drop operation")
            await self.source_element.drag_to(target_element.first)
            self.logger.info(f"Successfully completed drag to: {target_text}")
        else:
            self.logger.error(f"Drag target not found: {target_text}")
            raise RuntimeError(f"Drag target not found: {target_text}")


class DragDropWidget(DragDropWidgetPort):
    """Implementation of drag and drop widget."""

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

    async def drag(self, source_text: Union[str, object]) -> DragContext:
        """Start dragging from source text. Returns context for chaining."""
        self.logger.info(f"Starting drag from source: {source_text}")
        source_selector = Selector.by_text(source_text)
        if await self.web_session.interactor.exists(source_selector, timeout=2000):
            source_element = await self.web_session.interactor.find(source_selector)
            self.logger.info("Found drag source element, creating drag context")
            return PlaywrightDragContext(self.web_session, source_element)
        else:
            self.logger.error(f"Drag source not found: {source_text}")
            raise RuntimeError(f"Drag source not found: {source_text}")


class MatchingWidget(MatchingWidgetPort):
    """Implementation of matching/pairing widget."""

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

    async def match(
        self, left_text: Union[str, object], right_text: Union[str, object]
    ) -> None:
        """Match left text with right text."""
        self.logger.info(f"Matching elements: {left_text} -> {right_text}")
        # Implementation depends on the specific matching UI
        # This is a simplified version - actual implementation may vary
        left_selector = Selector.by_text(left_text)
        right_selector = Selector.by_text(right_text)

        if await self.web_session.interactor.exists(
            left_selector, timeout=2000
        ) and await self.web_session.interactor.exists(right_selector, timeout=2000):

            # Click left first, then right (common matching pattern)
            self.logger.info("Found both matching elements, performing match")
            await self.web_session.interactor.click(left_selector)
            await self.web_session.interactor.click(right_selector)
            self.logger.info(f"Successfully matched: {left_text} -> {right_text}")
        else:
            self.logger.error(
                f"Matching elements not found: {left_text} -> {right_text}"
            )
            raise RuntimeError(
                f"Matching elements not found: {left_text} -> {right_text}"
            )
