from typing import Union

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import (
    ActivityPlayerPagePort,
    LessonPlayerPagePort,
)

from ..ports.use_case import UseCasePort


class ExitActivityUseCase(UseCasePort):
    """
    Use case for exiting activities and lessons.
    Handles lesson exit with proper cleanup from the activity level.

    This use case can work with both ActivityPlayerPagePort (recommended)
    and LessonPlayerPagePort (for backward compatibility) to provide consistent exit functionality.
    """

    def __init__(
        self,
        web_session: IWebSession,
        player_page: Union[ActivityPlayerPagePort, LessonPlayerPagePort],
    ):
        self.web_session = web_session
        self.player_page = player_page

    async def execute(self) -> None:
        """Exit the current lesson/activity."""
        self.logger.info("Exiting current lesson from activity level")

        await self.player_page.exit_lesson()
        await self.web_session.navigator.wait_for_load()

        self.logger.info("Successfully exited lesson")
        await self.web_session.debug_dumpper.dump_screenshot("lesson_exited")
