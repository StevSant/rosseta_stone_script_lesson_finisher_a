from typing import Literal, Optional, Union

from rosseta_stone_script_a.application.orchestrators.complete_lesson_workflow import (
    CompleteLessonWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.open_fluency_builder import (
    OpenFluencyBuilder,
)
from rosseta_stone_script_a.application.orchestrators.select_activity_workflow import (
    SelectActivityWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.select_course_workflow import (
    SelectCourseWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.select_lesson_workflow import (
    SelectLessonWorkflow,
)
from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.domain.entities.credentials import Credentials


class FullLearningSession(OrchestratorPort):
    """
    Master orchestrator that follows the proper Rosetta Stone hierarchy:
    Course → Lesson → Activity

    Workflow:
    1. Login and navigate to Fluency Builder (OpenFluencyBuilder)
    2. Select course (SelectCourseWorkflow)
    3. Select lesson within course (SelectLessonWorkflow)
    4. Select activity within lesson (SelectActivityWorkflow)
    5. Play through lesson activities (CompleteLessonWorkflow)

    This orchestrator maintains Clean Architecture principles and idempotency.
    """

    def __init__(
        self,
        open_fluency_builder: OpenFluencyBuilder,
        select_course_workflow: SelectCourseWorkflow,
        select_lesson_workflow: SelectLessonWorkflow,
        select_activity_workflow: SelectActivityWorkflow,
        complete_lesson_workflow: CompleteLessonWorkflow,
    ):
        super().__init__()
        self.open_fluency_builder = open_fluency_builder
        self.select_course_workflow = select_course_workflow
        self.select_lesson_workflow = select_lesson_workflow
        self.select_activity_workflow = select_activity_workflow
        self.complete_lesson_workflow = complete_lesson_workflow

    async def execute(
        self,
        credentials: Credentials,
        course_pattern: Union[str, object],
        lesson_pattern: Union[str, int] = 1,  # Default to first lesson
        activity_pattern: Union[str, int] = 1,  # Default to first activity
        action: Literal["resume", "start"] = "resume",
        max_activities: Optional[int] = None,
        auto_exit: bool = True,
    ) -> dict:
        """
        Execute a complete hierarchical learning session.

        Args:
            credentials: User credentials for login
            course_pattern: Course name or regex pattern to match
            lesson_pattern: Lesson name/index within the course
            activity_pattern: Activity name/index within the lesson
            action: Either "resume" or "start" for each level
            max_activities: Maximum number of activities to handle
            auto_exit: Whether to automatically exit after completion

        Returns:
            Dictionary with session results and metrics
        """
        session_results = {
            "user": credentials.email,
            "course": str(course_pattern),
            "lesson": str(lesson_pattern),
            "activity": str(activity_pattern),
            "action": action,
            "activities_completed": 0,
            "success": False,
        }

        self.logger.info("Starting FullHierarchicalLearningSession")

        try:
            # Step 1: Login and navigate to Fluency Builder
            await self.open_fluency_builder.execute(credentials)

            # Step 2: Select and enter course
            await self.select_course_workflow.execute(course_pattern)

            # Step 3: Select and enter lesson within course
            await self.select_lesson_workflow.execute(lesson_pattern)

            # Step 4: Select and start activity within lesson
            await self.select_activity_workflow.execute(activity_pattern, action)

            # Step 5: Complete lesson activities
            if max_activities is not None:
                # Handle specific number of activities
                activities_completed = (
                    await self.complete_lesson_workflow.handle_multiple_activities(
                        max_activities
                    )
                )
                session_results["activities_completed"] = activities_completed

                # Exit if requested and we handled activities manually
                if auto_exit:
                    await self.complete_lesson_workflow.exit_lesson_use_case.execute()
            else:
                # Use default lesson completion flow
                await self.complete_lesson_workflow.execute(auto_exit)
                session_results["activities_completed"] = 1  # Basic handling

            session_results["success"] = True
            self.logger.info(
                "FullHierarchicalLearningSession completed successfully",
                extra=session_results,
            )

        except Exception as error:
            session_results["error"] = str(error)
            self.logger.error(
                "FullHierarchicalLearningSession failed", extra=session_results
            )
            raise

        return session_results
