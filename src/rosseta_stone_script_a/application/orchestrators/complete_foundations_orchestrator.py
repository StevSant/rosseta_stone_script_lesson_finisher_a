from typing import Any, Dict

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.complete_foundations import (
    CompleteFoundationsUseCase,
)


class CompleteFoundationsOrchestrator(OrchestratorPort):
    """
    Orchestrator that handles the completion of Foundations lessons.
    """

    def __init__(self, complete_foundations_use_case: CompleteFoundationsUseCase):
        super().__init__()
        self.complete_foundations_use_case = complete_foundations_use_case

    async def execute(self, captured_data: Dict[str, Any]) -> None:
        """
        Execute the completion workflow using captured session data.

        Args:
            captured_data: Data captured from the session (tokens, ids, etc.)
        """
        if all(captured_data.values()):
            self.logger.info(
                "Session data captured successfully. Starting completion..."
            )
            await self.complete_foundations_use_case.execute(
                authorization=captured_data["authorization"],
                language_code=captured_data["lang_code"],
                session_token=captured_data["session_token"],
                school_id=captured_data["school_id"],
                user_id=captured_data["user_id"],
            )
        else:
            self.logger.warning("Missing captured session data. Skipping completion.")
            self.logger.debug(f"Captured data state: {captured_data}")
