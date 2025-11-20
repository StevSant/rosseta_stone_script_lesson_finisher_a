from typing import Union

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.select_lesson import (
    SelectLessonUseCase,
)


class SelectLessonWorkflow(OrchestratorPort):
    """
    Orchestrator that handles lesson selection and initiation within a course.

    Workflow:
    1. Select specified lesson within the course
    2. Start or resume lesson based on preference

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        select_lesson_use_case: SelectLessonUseCase,
    ):
        super().__init__()
        self.select_lesson_use_case = select_lesson_use_case

    async def execute(
        self,
        lesson_pattern: Union[str, int],
    ) -> None:
        """
        Execute the complete SelectLessonWorkflow.

        Args:
            lesson_pattern: Lesson name, index, or regex pattern to match
            action: Either "resume" to resume lesson or "start" to start new lesson
        """
        self.logger.info(f"Starting SelectLessonWorkflow for lesson: {lesson_pattern}")

        # Step 1: Select the specified lesson
        await self.select_lesson_use_case.execute(lesson_pattern)

        self.logger.info(
            f"SelectLessonWorkflow completed successfully for lesson: {lesson_pattern}"
        )
