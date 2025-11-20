from typing import Union

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.select_course import (
    SelectCourseUseCase,
)


class SelectCourseWorkflow(OrchestratorPort):
    """
    Orchestrator that handles course selection and initiation.

    Workflow:
    1. Select specified course in Fluency Builder
    2. Start or resume course based on preference

    This orchestrator is idempotent - can be retried safely if any step fails.
    """

    def __init__(
        self,
        select_course_use_case: SelectCourseUseCase,
    ):
        super().__init__()
        self.select_course_use_case = select_course_use_case

    async def execute(
        self,
        course_pattern: Union[str, object],
    ) -> None:
        """
        Execute the complete SelectCourseWorkflow.

        Args:
            course_pattern: Course name or regex pattern to match
            action: Either "resume" to resume course or "start" to start new course
        """
        self.logger.info(f"Starting SelectCourseWorkflow for course: {course_pattern}")

        # Step 1: Select the specified course
        await self.select_course_use_case.execute(course_pattern)

        self.logger.info(
            f"SelectCourseWorkflow completed successfully for course: {course_pattern}"
        )
