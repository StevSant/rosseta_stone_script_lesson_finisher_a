from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.exit_lesson import ExitLessonUseCase
from rosseta_stone_script_a.application.use_cases.play_lesson_flow import (
    PlayLessonFlowUseCase,
)


class CompleteLessonWorkflow(OrchestratorPort):
    """
    Orchestrator that handles lesson play and completion.

    Workflow:
    1. Initialize lesson play flow
    2. Handle lesson activities (extensible for future activity handling)
    3. Exit lesson cleanly

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        play_lesson_use_case: PlayLessonFlowUseCase,
        exit_lesson_use_case: ExitLessonUseCase,
    ):
        super().__init__()
        self.play_lesson_use_case = play_lesson_use_case
        self.exit_lesson_use_case = exit_lesson_use_case

    async def execute(self, auto_exit: bool = True) -> None:
        """
        Execute the complete lesson workflow.

        Args:
            auto_exit: Whether to automatically exit lesson after play (default: True)
        """
        self.logger.info("Starting CompleteLessonWorkflow")

        # Step 1: Initialize lesson play flow
        await self.play_lesson_use_case.execute()

        # Step 2: Handle lesson activities (basic implementation)
        # This can be extended to handle specific activity types and interactions
        await self._handle_basic_activities()

        # Step 3: Exit lesson if requested
        if auto_exit:
            await self.exit_lesson_use_case.execute()

        self.logger.info("CompleteLessonWorkflow completed successfully")

    async def _handle_basic_activities(self) -> None:
        """
        Handle basic lesson activities.

        This is a placeholder for more sophisticated activity handling.
        Future implementations can extend this to handle specific activity types,
        user interactions, and progression logic.
        """
        self.logger.info("Basic lesson activities handling - ready for extension")

        # For now, we just handle one activity progression as an example
        # This demonstrates how the orchestrator can manage complex workflows
        try:
            await self.play_lesson_use_case.handle_activity_progression()
            self.logger.info("Handled one activity progression")
        except Exception as e:
            self.logger.warning(f"Activity progression not available or completed: {e}")

    async def handle_multiple_activities(self, max_activities: int = 5) -> int:
        """
        Extended method to handle multiple activities in sequence.

        Args:
            max_activities: Maximum number of activities to handle

        Returns:
            Number of activities successfully processed
        """
        activities_processed = 0

        for i in range(max_activities):
            try:
                await self.play_lesson_use_case.handle_activity_progression()
                activities_processed += 1
            except Exception as e:
                self.logger.info(f"Activity {i+1} completed or not available: {e}")
                break

        self.logger.info(f"Processed {activities_processed} activities")
        return activities_processed
