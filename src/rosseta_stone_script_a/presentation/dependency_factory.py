from rosseta_stone_script_a.application.orchestrators.open_fundations import (
    OpenFundations,
)
from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.use_cases.go_to_fluency_builder import (
    GoToFundationsUseCase,
)
from rosseta_stone_script_a.application.use_cases.login_rosseta import (
    LoginRossetaUseCase,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.dashboard_page import (
    DashboardPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.login_page import (
    LoginPage,
)


class DependencyFactory:
    """Factory for creating orchestrators with proper dependency injection."""

    def __init__(self, web_session: IWebSession, rosseta_login_url: str):
        self.web_session = web_session
        self.rosseta_login_url = rosseta_login_url

    def create_open_fundations(self) -> OpenFundations:
        """Create OpenFluencyBuilder orchestrator with dependencies."""
        # Create pages
        login_page = LoginPage(
            web_session=self.web_session, rosetta_login_url=self.rosseta_login_url
        )
        dashboard_page = DashboardPage(web_session=self.web_session)

        # Create use cases
        login_use_case = LoginRossetaUseCase(
            web_session=self.web_session, login_page=login_page
        )
        navigate_use_case = GoToFundationsUseCase(
            web_session=self.web_session, dashboard_page=dashboard_page
        )

        # Create orchestrator
        return OpenFundations(
            login_use_case=login_use_case, navigate_use_case=navigate_use_case
        )
