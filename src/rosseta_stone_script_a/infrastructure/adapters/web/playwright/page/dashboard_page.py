from __future__ import annotations

import re
from typing import Optional

from rosseta_stone_script_a.application.ports.web.control import Selector
from rosseta_stone_script_a.application.ports.web.page import DashboardPagePort
from rosseta_stone_script_a.application.ports.web.session import IWebSession
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.patterns import (
    LessonPatterns,
)


class DashboardPage(DashboardPagePort):
    """
    Dashboard page adapter for navigating to Foundations.
    All interactions go through self.web_session.interactor.
    """

    def __init__(self, web_session: IWebSession) -> None:
        super().__init__()
        self.web_session = web_session

        # Selectors for Foundations navigation
        self.FOUNDATIONS_BTN = Selector.by_text(LessonPatterns.FOUNDATIONS)
        # Selector for user name on dashboard
        self.USER_NAME_SELECTOR = Selector.by_css('[data-qa="DashboardUserName"]')

    async def open_foundations(self) -> None:
        """Navigate to Foundations from the dashboard."""
        self.logger.info("Attempting to open Foundations from dashboard")
        # Try button first, then link
        try:
            if await self.web_session.interactor.exists(
                self.FOUNDATIONS_BTN, timeout=2000
            ):
                self.logger.info("Found Foundations button, clicking it")
                await self.web_session.interactor.click(self.FOUNDATIONS_BTN)
            else:
                self.logger.error("Foundations navigation element not found")
                raise RuntimeError("Foundations navigation element not found")
            self.logger.info("Successfully opened Foundations")
        except Exception as e:
            self.logger.error(f"Failed to navigate to Foundations: {e}")
            raise RuntimeError(f"Failed to navigate to Foundations: {e}")

    async def get_user_name(self) -> Optional[str]:
        """Get the user's name displayed on the dashboard."""
        self.logger.info("Attempting to get user name from dashboard")
        try:
            text = await self.web_session.interactor.get_text(
                self.USER_NAME_SELECTOR, timeout=5000
            )
            if text:
                # Extract just the name from "Hello, Name!" format
                # The text content is like: "Hello, Briggitte Naomy Casquete Valenzuela!"
                match = re.search(r"Hello,\s*(.+?)!", text)
                if match:
                    name = match.group(1).strip()
                    self.logger.info(f"Found user name: {name}")
                    return name
                # If no match, return the raw text without "Hello, " prefix
                name = text.replace("Hello,", "").strip().rstrip("!")
                self.logger.info(f"Extracted user name: {name}")
                return name
            self.logger.warning("User name element found but text is empty")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get user name: {e}")
            return None
