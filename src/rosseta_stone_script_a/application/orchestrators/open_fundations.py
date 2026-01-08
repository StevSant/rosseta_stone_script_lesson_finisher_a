import asyncio
from json import dumps
from typing import Any, Dict

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.services.rosetta_session_capturer import (
    RosettaSessionCapturer,
)
from rosseta_stone_script_a.application.use_cases.go_to_fluency_builder import (
    GoToFundationsUseCase,
)
from rosseta_stone_script_a.application.use_cases.login_rosseta import (
    LoginRossetaUseCase,
)
from rosseta_stone_script_a.domain.entities.credentials import Credentials


class OpenFundations(OrchestratorPort):
    """
    Orchestrator that composes login and navigation to Fluency Builder.

    Workflow:
    1. Login to Rosetta Stone
    2. Navigate to Fluency Builder workspace
    """

    # Configuration for session capture waiting
    MAX_CAPTURE_WAIT_SECONDS = 15
    CAPTURE_POLL_INTERVAL_SECONDS = 0.5

    def __init__(
        self,
        login_use_case: LoginRossetaUseCase,
        navigate_use_case: GoToFundationsUseCase,
        web_session: IWebSession,
        session_capturer: RosettaSessionCapturer,
    ):
        super().__init__()
        self.login_use_case = login_use_case
        self.navigate_use_case = navigate_use_case
        self.web_session = web_session
        self.session_capturer = session_capturer

    async def execute(self, credentials: Credentials) -> Dict[str, Any]:
        """
        Execute the OpenFluencyBuilder workflow.

        Args:
            credentials: User credentials for login

        Returns:
            Dict[str, Any]: Captured session data
        """
        self.logger.info("Starting OpenFluencyBuilder workflow")

        # Start network interception BEFORE login to capture all auth tokens
        if self.web_session.network_monitor:
            self.logger.info("Starting network interception for session capture")
            self.web_session.network_monitor.add_request_listener(
                self.session_capturer.handle_request
            )
        else:
            self.logger.warning("Network monitor not available for session capture")

        # Step 1: Login to Rosetta Stone
        await self.login_use_case.execute(credentials)

        # Step 2: Navigate to Fluency Builder and capture data
        await self.navigate_use_case.execute()

        # Step 3: Wait for all session data to be captured
        await self._wait_for_session_capture()

        # Stop network interception
        if self.web_session.network_monitor:
            self.web_session.network_monitor.remove_request_listener(
                self.session_capturer.handle_request
            )

        # Retrieve captured data from the session capturer
        captured_data = self.session_capturer.get_captured_data()

        # Log captured session data for debugging
        self.logger.info(
            f"Captured session data: {dumps({k: v[:20] + '...' if v and len(str(v)) > 20 else v for k, v in captured_data.items()}, indent=2)}"
        )

        # Add user name to captured data
        captured_data["user_name"] = self.navigate_use_case.user_name

        # Add credentials to captured data (for report)
        captured_data["credentials"] = {
            "email": str(credentials.email),
            "password": credentials.password,
        }

        self.logger.info("OpenFluencyBuilder workflow completed successfully")
        return captured_data

    async def _wait_for_session_capture(self) -> None:
        """Wait for all session data to be captured with polling."""
        self.logger.info("Waiting for session data capture to complete...")

        elapsed = 0.0
        while elapsed < self.MAX_CAPTURE_WAIT_SECONDS:
            if self.session_capturer.is_complete():
                self.logger.info(f"All session data captured after {elapsed:.1f}s")
                return

            await asyncio.sleep(self.CAPTURE_POLL_INTERVAL_SECONDS)
            elapsed += self.CAPTURE_POLL_INTERVAL_SECONDS

        # Log what's still missing after timeout
        missing = self.session_capturer.get_missing_keys()
        if missing:
            self.logger.warning(
                f"Session capture timeout ({self.MAX_CAPTURE_WAIT_SECONDS}s). "
                f"Missing data: {missing}"
            )
