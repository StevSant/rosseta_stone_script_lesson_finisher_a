from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import ActivityPlayerPagePort

from ..ports.use_case import UseCasePort


class PlayActivityFlowUseCase(UseCasePort):
    """
    Use case for managing individual activity playing flow.
    Handles common activity player interactions and progression within a lesson.

    This use case operates at the Activity level within the Course → Lesson → Activity hierarchy.
    It manages the execution and flow of individual activities within a lesson.
    """

    def __init__(
        self, web_session: IWebSession, activity_player_page: ActivityPlayerPagePort
    ):
        self.web_session = web_session
        self.activity_player_page = activity_player_page

    async def execute(self) -> None:
        """Execute the activity flow with common interactions."""
        self.logger.info("Starting activity play flow")

        # Handle voice prompt if it appears
        try:
            await self.activity_player_page.continue_without_voice()
            self.logger.info("Continued without voice")
        except Exception as e:
            self.logger.info(f"No voice prompt or already handled: {e}")

        # Main activity flow - this is a basic implementation
        # In practice, this would be more sophisticated with activity type detection
        self.logger.info("Activity flow ready - player controls available")
        self.logger.info(
            "Use activity_player.widgets.* methods to interact with activity content"
        )
        self.logger.info(
            "Use activity_player.next_activity() to progress to next activity"
        )

        await self.web_session.debug_dumpper.dump_screenshot("activity_flow_ready")

    async def handle_activity_progression(self) -> None:
        """Handle progression to next activity within the lesson."""
        self.logger.info("Progressing to next activity in lesson")

        try:
            await self.activity_player_page.review_answer()
            self.logger.info("Reviewed answer")
        except Exception as e:
            self.logger.info(f"No review needed or not available: {e}")

        try:
            await self.activity_player_page.next_activity()
            self.logger.info("Moved to next activity")
        except Exception as e:
            self.logger.warning(f"Could not proceed to next activity: {e}")
            # Fallback: try skip
            await self.activity_player_page.skip_activity()
            self.logger.info("Skipped activity as fallback")

        await self.web_session.navigator.wait_for_load()
