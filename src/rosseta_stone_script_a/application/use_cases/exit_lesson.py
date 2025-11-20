from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import LessonPlayerPagePort

from ..ports.use_case import UseCasePort


class ExitLessonUseCase(UseCasePort):
    """
    Use case for exiting lessons.
    Handles lesson exit with proper cleanup.
    """

    def __init__(
        self, web_session: IWebSession, lesson_player_page: LessonPlayerPagePort
    ):
        self.web_session = web_session
        self.lesson_player_page = lesson_player_page

    async def execute(self) -> None:
        """Exit the current lesson."""
        self.logger.info("Exiting lesson")

        await self.lesson_player_page.exit_lesson()
        await self.web_session.navigator.wait_for_load()

        self.logger.info("Successfully exited lesson")
        await self.web_session.debug_dumpper.dump_screenshot("lesson_exited")
