from typing import Literal

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import ActivityCatalogPagePort

from ..ports.use_case import UseCasePort


class StartOrResumeActivityUseCase(UseCasePort):
    """
    Use case for starting or resuming activities.
    Handles both resume and start operations from activity catalog.
    """

    def __init__(
        self,
        web_session: IWebSession,
        activity_catalog_page: ActivityCatalogPagePort,
    ):
        self.web_session = web_session
        self.activity_catalog_page = activity_catalog_page

    async def execute(self, target: Literal["resume", "start"]) -> None:
        """
        Start or resume an activity.

        Args:
            target: Either "resume" to resume activity or "start" to start new activity
        """
        self.logger.info(f"Executing activity action: {target}")

        if target == "resume":
            await self.activity_catalog_page.resume_activity()
            self.logger.info("Resumed activity")
        elif target == "start":
            await self.activity_catalog_page.start_activity()
            self.logger.info("Started activity")
        else:
            raise ValueError(f"Invalid target: {target}. Must be 'resume' or 'start'")

        # Wait for activity to load
        await self.web_session.navigator.wait_for_load()

        self.logger.info(f"Successfully executed {target} activity")
        await self.web_session.debug_dumpper.dump_screenshot(f"activity_{target}ed")
