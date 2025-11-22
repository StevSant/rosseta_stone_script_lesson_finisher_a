from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.complete_foundations import (
    CompleteFoundationsUseCase,
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
    3. Complete Foundations lessons (if data captured)

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        login_use_case: LoginRossetaUseCase,
        navigate_use_case: GoToFundationsUseCase,
        complete_foundations_use_case: CompleteFoundationsUseCase,
    ):
        super().__init__()
        self.login_use_case = login_use_case
        self.navigate_use_case = navigate_use_case
        self.complete_foundations_use_case = complete_foundations_use_case

    async def execute(self, credentials: Credentials) -> None:
        """
        Execute the complete OpenFluencyBuilder workflow.

        Args:
            credentials: User credentials for login
        """
        self.logger.info("Starting OpenFluencyBuilder workflow")

        # Step 1: Login to Rosetta Stone
        await self.login_use_case.execute(credentials)

        # Step 2: Navigate to Fluency Builder and capture data
        await self.navigate_use_case.execute()
        
        # Retrieve captured data from the navigate use case's capturer
        # Note: We need to access the capturer from the use case. 
        # Ideally, the use case should return the data, but for now we access it directly 
        # or we can modify the use case to return it.
        # Let's assume we can access it via the use case instance for now.
        captured_data = self.navigate_use_case.session_capturer.get_captured_data()
        
        if all(captured_data.values()):
            self.logger.info("Session data captured successfully. Starting completion...")
            # Step 3: Complete Foundations
            await self.complete_foundations_use_case.execute(
                authorization=captured_data["authorization"],
                language_code=captured_data["lang_code"],
                session_token=captured_data["session_token"],
                school_id=captured_data["school_id"],
                user_id=captured_data["user_id"]
            )
        else:
            self.logger.warning("Missing captured session data. Skipping completion.")
            self.logger.debug(f"Captured data state: {captured_data}")

        self.logger.info("OpenFluencyBuilder workflow completed successfully")
