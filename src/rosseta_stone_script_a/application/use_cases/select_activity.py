from typing import Union

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import ActivityCatalogPagePort

from ..ports.use_case import UseCasePort


class SelectActivityUseCase(UseCasePort):
    """
    Use case for selecting an activity within a lesson.
    Handles activity selection from the activity catalog.
    """

    def __init__(
        self,
        web_session: IWebSession,
        activity_catalog_page: ActivityCatalogPagePort,
    ):
        self.web_session = web_session
        self.activity_catalog_page = activity_catalog_page

    async def execute(self, activity_pattern: Union[str, int]) -> None:
        """
        Select an activity by pattern or index.

        Args:
            activity_pattern: Activity name, index, or regex pattern to match
        """
        self.logger.info(f"Selecting activity with pattern: {activity_pattern}")

        # Select the activity from catalog
        await self.activity_catalog_page.select_activity(activity_pattern)
        await self.web_session.navigator.wait_for_load()

        self.logger.info(f"Successfully selected activity: {activity_pattern}")
        await self.web_session.debug_dumpper.dump_screenshot("activity_selected")
