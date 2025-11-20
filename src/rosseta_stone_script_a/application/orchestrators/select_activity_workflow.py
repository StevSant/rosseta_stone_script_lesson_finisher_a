from typing import Literal, Union

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.select_activity import (
    SelectActivityUseCase,
)
from rosseta_stone_script_a.application.use_cases.start_or_resume_activity import (
    StartOrResumeActivityUseCase,
)


class SelectActivityWorkflow(OrchestratorPort):
    """
    Orchestrator that handles activity selection and initiation within a lesson.

    Workflow:
    1. Select specified activity within the lesson
    2. Start or resume activity based on preference

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        select_activity_use_case: SelectActivityUseCase,
        start_activity_use_case: StartOrResumeActivityUseCase,
    ):
        super().__init__()
        self.select_activity_use_case = select_activity_use_case
        self.start_activity_use_case = start_activity_use_case

    async def execute(
        self,
        activity_pattern: Union[str, int],
        action: Literal["resume", "start"] = "resume",
    ) -> None:
        """
        Execute the complete SelectActivityWorkflow.

        Args:
            activity_pattern: Activity name, index, or regex pattern to match
            action: Either "resume" to resume activity or "start" to start new activity
        """
        self.logger.info(
            f"Starting SelectActivityWorkflow for activity: {activity_pattern}"
        )

        # Step 1: Select the specified activity
        await self.select_activity_use_case.execute(activity_pattern)

        # Step 2: Start or resume activity
        await self.start_activity_use_case.execute(action)

        self.logger.info(
            f"SelectActivityWorkflow completed successfully for activity: {activity_pattern}"
        )
