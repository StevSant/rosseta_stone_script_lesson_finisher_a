from __future__ import annotations

from rosseta_stone_script_a.application.ports.web.control import Selector
from rosseta_stone_script_a.application.ports.web.page import DashboardPagePort
from rosseta_stone_script_a.application.ports.web.session import IWebSession
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.patterns import (
    LessonPatterns,
)


class DashboardPage(DashboardPagePort):
    """
    Dashboard page adapter for navigating to Fluency Builder.
    All interactions go through self.web_session.interactor.
    """

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

        # Selectors for Fluency Builder navigation
        self.FLUENCY_BUILDER_LINK = Selector.by_text(LessonPatterns.FLUENCY_BUILDER)
        self.FLUENCY_BUILDER_BTN = Selector.role_button(LessonPatterns.FLUENCY_BUILDER)

    async def open_fluency_builder(self) -> None:
        """Navigate to Fluency Builder from the dashboard."""
        self.logger.info("Attempting to open Fluency Builder")
        # Try button first, then link
        try:
            if await self.web_session.interactor.exists(
                self.FLUENCY_BUILDER_BTN, timeout=2000
            ):
                self.logger.info("Found Fluency Builder button, clicking it")
                await self.web_session.interactor.click(self.FLUENCY_BUILDER_BTN)
            elif await self.web_session.interactor.exists(
                self.FLUENCY_BUILDER_LINK, timeout=2000
            ):
                self.logger.info("Found Fluency Builder link, clicking it")
                await self.web_session.interactor.click(self.FLUENCY_BUILDER_LINK)
            else:
                self.logger.error("Fluency Builder navigation element not found")
                raise RuntimeError("Fluency Builder navigation element not found")
            self.logger.info("Successfully opened Fluency Builder")
        except Exception as e:
            self.logger.error(f"Failed to navigate to Fluency Builder: {e}")
            raise RuntimeError(f"Failed to navigate to Fluency Builder: {e}")
