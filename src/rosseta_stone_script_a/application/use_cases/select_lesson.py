from typing import Union

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import LessonCatalogPagePort

from ..ports.use_case import UseCasePort


class SelectLessonUseCase(UseCasePort):
    """
    Use case for selecting a lesson within a course.
    Handles lesson selection from the lesson catalog.
    """

    def __init__(
        self,
        web_session: IWebSession,
        lesson_catalog_page: LessonCatalogPagePort,
    ):
        self.web_session = web_session
        self.lesson_catalog_page = lesson_catalog_page

    async def execute(self, lesson_pattern: Union[str, int]) -> None:
        """
        Select a lesson by pattern or index.

        Args:
            lesson_pattern: Lesson name, index, or regex pattern to match
        """
        self.logger.info(f"Selecting lesson with pattern: {lesson_pattern}")

        # Select the lesson from catalog
        await self.lesson_catalog_page.select_lesson(lesson_pattern)
        await self.web_session.navigator.wait_for_load()

        self.logger.info(f"Successfully selected lesson: {lesson_pattern}")
        await self.web_session.debug_dumpper.dump_screenshot("lesson_selected")
