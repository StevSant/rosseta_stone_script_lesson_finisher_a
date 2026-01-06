import json

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import DashboardPagePort
from rosseta_stone_script_a.application.services.rosetta_session_capturer import (
    RosettaSessionCapturer,
)

from ..ports.use_case import UseCasePort


class GoToFundationsUseCase(UseCasePort):
    """
    Use case for navigating to Fluency Builder from the dashboard.
    Handles the initial navigation after login.
    """

    def __init__(
        self,
        web_session: IWebSession,
        dashboard_page: DashboardPagePort,
        session_capturer: RosettaSessionCapturer,
    ):
        self.web_session = web_session
        self.dashboard_page = dashboard_page
        self.session_capturer = session_capturer
        self.user_name: str | None = None

    async def execute(self) -> None:
        """Navigate to Foundations from dashboard."""
        self.logger.info("Navigating to Foundations from dashboard")

        # Capture user name from dashboard
        await self._capture_user_name()

        # --- Start Interception Logic ---
        if self.web_session.network_monitor:
            self.web_session.network_monitor.add_request_listener(
                self.session_capturer.handle_request
            )
        else:
            self.logger.warning("Network monitor not available")
        # --------------------------------

        await self.dashboard_page.open_foundations()

        # Wait for page to load
        await self.web_session.navigator.wait_for_load()

        # --- End Interception Logic ---
        if self.web_session.network_monitor:
            self.logger.info(
                f"Captured Data: {json.dumps(self.session_capturer.get_captured_data(), indent=2)}"
            )
            self.web_session.network_monitor.remove_request_listener(
                self.session_capturer.handle_request
            )
        # ------------------------------

        self.logger.info("Successfully navigated to Fluency Builder")
        await self.web_session.debug_dumpper.dump_screenshot(
            "fluency_builder_workspace"
        )

    async def _capture_user_name(self) -> None:
        """Capture the user name from the dashboard."""
        try:
            self.user_name = await self.dashboard_page.get_user_name()
            if self.user_name:
                self.logger.info(f"Captured user name: {self.user_name}")
            else:
                self.logger.warning("Could not capture user name from dashboard")
        except Exception as e:
            self.logger.error(f"Error capturing user name: {e}")
