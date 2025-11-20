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
        self.FOUNDATIONS_BTN = Selector.by_text(LessonPatterns.FOUNDATIONS)

    async def open_foundations(self) -> None:
        """Navigate to Foundations from the dashboard."""
        self.logger.info("Attempting to open Foundations from dashboard")
        # Try button first, then link
        try:
            if await self.web_session.interactor.exists(
                self.FOUNDATIONS_BTN, timeout=2000
            ):
                self.logger.info("Found Fluency Builder button, clicking it")
                await self.web_session.interactor.click(self.FOUNDATIONS_BTN)
            else:
                self.logger.error("Fluency Builder navigation element not found")
                raise RuntimeError("Fluency Builder navigation element not found")
            self.logger.info("Successfully opened Fluency Builder")
        except Exception as e:
            self.logger.error(f"Failed to navigate to Fluency Builder: {e}")
            raise RuntimeError(f"Failed to navigate to Fluency Builder: {e}")
