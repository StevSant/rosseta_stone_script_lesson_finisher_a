from typing import Union

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import (
    CourseCatalogPagePort,
)

from ..ports.use_case import UseCasePort


class SelectCourseUseCase(UseCasePort):
    """
    Use case for selecting a course in Fluency Builder.
    Orchestrates navigation from workspace to course catalog and course selection.
    """

    def __init__(
        self,
        web_session: IWebSession,
        course_catalog_page: CourseCatalogPagePort,
    ):
        self.web_session = web_session
        self.course_catalog_page = course_catalog_page

    async def execute(self, course_pattern: Union[str, object]) -> None:
        """
        Select a course by pattern.

        Args:
            course_pattern: Course name or regex pattern to match
        """
        self.logger.info(f"Selecting course with pattern: {course_pattern}")

        await self.course_catalog_page.select_course(course_pattern)
        await self.web_session.navigator.wait_for_load()

        self.logger.info(f"Successfully selected course: {course_pattern}")
        await self.web_session.debug_dumpper.dump_screenshot("course_selected")
