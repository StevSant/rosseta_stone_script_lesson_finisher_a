from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.ports.web.page import DashboardPagePort

from ..ports.use_case import UseCasePort


class GoToFluencyBuilderUseCase(UseCasePort):
    """
    Use case for navigating to Fluency Builder from the dashboard.
    Handles the initial navigation after login.
    """

    def __init__(self, web_session: IWebSession, dashboard_page: DashboardPagePort):
        self.web_session = web_session
        self.dashboard_page = dashboard_page

    async def execute(self) -> None:
        """Navigate to Fluency Builder from dashboard."""
        self.logger.info("Navigating to Fluency Builder from dashboard")
        await self.dashboard_page.open_fluency_builder()

        # Wait for page to load
        await self.web_session.navigator.wait_for_load()

        self.logger.info("Successfully navigated to Fluency Builder")
        await self.web_session.debug_dumpper.dump_screenshot(
            "fluency_builder_workspace"
        )
