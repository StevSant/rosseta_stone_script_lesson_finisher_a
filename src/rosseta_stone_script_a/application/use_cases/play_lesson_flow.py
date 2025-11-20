from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import LessonPlayerPagePort

from ..ports.use_case import UseCasePort


class PlayLessonFlowUseCase(UseCasePort):
    """
    Use case for managing the lesson playing flow.
    Handles common lesson player interactions and activity progression.

    Note: This use case is maintained for backward compatibility.
    For new implementations, consider using PlayActivityFlowUseCase which better
    reflects the Course → Lesson → Activity hierarchy by operating at the Activity level.
    """

    def __init__(
        self, web_session: IWebSession, lesson_player_page: LessonPlayerPagePort
    ):
        self.web_session = web_session
        self.lesson_player_page = lesson_player_page

    async def execute(self) -> None:
        """Execute the lesson flow with common interactions."""
        self.logger.info("Starting lesson play flow")

        # Handle voice prompt if it appears
        try:
            await self.lesson_player_page.continue_without_voice()
            self.logger.info("Continued without voice")
        except Exception as e:
            self.logger.info(f"No voice prompt or already handled: {e}")

        # Main lesson flow - this is a basic implementation
        # In practice, this would be more sophisticated with activity detection
        self.logger.info("Lesson flow ready - player controls available")
        self.logger.info(
            "Use lesson_player.widgets.* methods to interact with activities"
        )
        self.logger.info("Use lesson_player.next_activity() to progress")

        await self.web_session.debug_dumpper.dump_screenshot("lesson_flow_ready")

    async def handle_activity_progression(self) -> None:
        """Handle progression to next activity."""
        self.logger.info("Progressing to next activity")

        try:
            await self.lesson_player_page.review_answer()
            self.logger.info("Reviewed answer")
        except Exception as e:
            self.logger.info(f"No review needed or not available: {e}")

        try:
            await self.lesson_player_page.next_activity()
            self.logger.info("Moved to next activity")
        except Exception as e:
            self.logger.warning(f"Could not proceed to next activity: {e}")
            # Fallback: try skip
            await self.lesson_player_page.skip_activity()
            self.logger.info("Skipped activity as fallback")

        await self.web_session.navigator.wait_for_load()
