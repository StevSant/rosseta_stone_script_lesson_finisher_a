from typing import Any, Dict

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
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

    def __init__(
        self,
        login_use_case: LoginRossetaUseCase,
        navigate_use_case: GoToFundationsUseCase,
    ):
        super().__init__()
        self.login_use_case = login_use_case
        self.navigate_use_case = navigate_use_case

    async def execute(self, credentials: Credentials) -> Dict[str, Any]:
        """
        Execute the OpenFluencyBuilder workflow.

        Args:
            credentials: User credentials for login

        Returns:
            Dict[str, Any]: Captured session data
        """
        self.logger.info("Starting OpenFluencyBuilder workflow")

        # Step 1: Login to Rosetta Stone
        await self.login_use_case.execute(credentials)

        # Step 2: Navigate to Fluency Builder and capture data
        await self.navigate_use_case.execute()

        # Retrieve captured data from the navigate use case's capturer
        captured_data = self.navigate_use_case.session_capturer.get_captured_data()

        # Add user name to captured data
        captured_data["user_name"] = self.navigate_use_case.user_name

        self.logger.info("OpenFluencyBuilder workflow completed successfully")
        return captured_data
