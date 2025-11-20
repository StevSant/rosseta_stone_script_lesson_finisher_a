from __future__ import annotations

from typing import Optional

from playwright.async_api import Browser, Playwright, async_playwright

from rosseta_stone_script_a.application.ports.web import BrowserProviderPort
from rosseta_stone_script_a.shared.mixins.loggin_mixin import LoggingMixin

from ..common.viewport import Viewport
from .playwright_web_session import PlaywrightWebSession


class PlaywrightBrowserProvider(BrowserProviderPort, LoggingMixin):
    def __init__(
        self,
        *,
        headless: bool,
        slow_mo: int = 0,
        user_agent: str,
        locale: str,
        viewport: Viewport,
        enable_no_sandbox: bool = True,
    ) -> None:
        self._playwright_instance: Optional[Playwright] = None
        self.browser: Optional[Browser] = None

        self.headless = headless
        self.slow_mo = slow_mo
        self.user_agent = user_agent
        self.locale = locale

        # Validación simple del viewport
        if not isinstance(viewport.get("width"), int) or not isinstance(
            viewport.get("height"), int
        ):
            raise ValueError("viewport must have integer 'width' and 'height'")
        self.viewport = viewport

        self.enable_no_sandbox = enable_no_sandbox

    async def start(self) -> None:
        if self.browser is not None:
            return

        self._playwright_instance = await async_playwright().start()

        self._playwright_instance.selectors.set_test_id_attribute("data-qa")

        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
        ]
        if self.enable_no_sandbox:
            launch_args.append("--no-sandbox")

        self.browser = await self._playwright_instance.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=launch_args,
        )

    async def stop(self) -> None:
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self._playwright_instance:
            await self._playwright_instance.stop()
            self._playwright_instance = None

    def new_web_session(self) -> PlaywrightWebSession:
        if self.browser is None:
            raise RuntimeError("The browser is not started. Call start() first.")
        return PlaywrightWebSession(
            self.browser,
            user_agent=self.user_agent,
            locale=self.locale,
            viewport=self.viewport,
        )
