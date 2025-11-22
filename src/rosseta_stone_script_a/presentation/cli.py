import asyncio
from typing import Optional, Union

from rosseta_stone_script_a.domain.entities.credentials import Credentials
from rosseta_stone_script_a.infrastructure.adapters.web import PlaywrightBrowserProvider
from rosseta_stone_script_a.infrastructure.core import settings
from rosseta_stone_script_a.shared.mixins import LoggingMixin

from .dependency_factory import DependencyFactory


class RosettaCLI(LoggingMixin):
    """CLI interface with centralized logging."""

    async def enter_rosetta(
        self,
        *,
        rosseta_login_url: str,
        user_credentials: Credentials,
        units_to_complete: list[int] = None,
    ):
        """
        Run a hierarchical learning session following Course → Lesson → Activity flow.
        This follows the proper Rosetta Stone hierarchy.
        """
        browser_settings = settings.browser_settings

        provider = PlaywrightBrowserProvider(
            headless=browser_settings.headless,
            slow_mo=browser_settings.slow_mo,
            user_agent=browser_settings.user_agent,
            locale=browser_settings.locale,
            viewport={
                "width": browser_settings.viewport_width,
                "height": browser_settings.viewport_height,
            },
        )

        await provider.start()
        self.logger.info("BrowserProvider started")

        try:
            web = provider.new_web_session()
            async with web.session() as web_session:
                # Create dependency factory
                factory = DependencyFactory(
                    web_session=web_session,
                    rosseta_login_url=rosseta_login_url,
                    units_to_complete=units_to_complete,
                )

                # Create and execute hierarchical learning session orchestrator
                open_fundations = factory.create_open_fundations()

                await open_fundations.execute(
                    credentials=user_credentials,
                )

                self.logger.info("Hierarchical learning session finished successfully")

        finally:
            await provider.stop()
            self.logger.info("BrowserProvider stopped")

    def main_cli(self):
        """
        Entry point invocado desde main.py o directamente si quieres.
        Puede parsear argumentos, aquí lo dejamos simple y usa settings.

        Por defecto ejecuta una sesión completa de aprendizaje.
        """
        rosseta_settings = settings.rosseta_settings
        user_credentials = Credentials(
            email=rosseta_settings.rosetta_email,
            password=rosseta_settings.rosetta_password,
        )

        asyncio.run(
            self.enter_rosetta(
                rosseta_login_url=rosseta_settings.rosetta_login_url,
                user_credentials=user_credentials,
                units_to_complete=rosseta_settings.rosetta_units_to_complete,
            )
        )


def main_cli():
    """Legacy function - use CLI().main_cli() instead."""
    cli = RosettaCLI()
    cli.main_cli()
