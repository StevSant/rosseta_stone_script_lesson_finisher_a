from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.go_to_fluency_builder import (
    GoToFluencyBuilderUseCase,
)
from rosseta_stone_script_a.application.use_cases.login_rosseta import (
    LoginRossetaUseCase,
)
from rosseta_stone_script_a.domain.entities.credentials import Credentials


class OpenFluencyBuilder(OrchestratorPort):
    """
    Orchestrator that composes login and navigation to Fluency Builder.

    Workflow:
    1. Login to Rosetta Stone
    2. Navigate to Fluency Builder workspace

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        login_use_case: LoginRossetaUseCase,
        navigate_use_case: GoToFluencyBuilderUseCase,
    ):
        super().__init__()
        self.login_use_case = login_use_case
        self.navigate_use_case = navigate_use_case

    async def execute(self, credentials: Credentials) -> None:
        """
        Execute the complete OpenFluencyBuilder workflow.

        Args:
            credentials: User credentials for login
        """
        self.logger.info("Starting OpenFluencyBuilder workflow")

        # Step 1: Login to Rosetta Stone
        await self.login_use_case.execute(credentials)

        # Step 2: Navigate to Fluency Builder
        await self.navigate_use_case.execute()

        self.logger.info("OpenFluencyBuilder workflow completed successfully")
