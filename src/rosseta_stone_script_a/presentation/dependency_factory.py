from rosseta_stone_script_a.application.orchestrators.open_fundations import (
    OpenFundations,
)
from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.services.rosetta_session_capturer import (
    RosettaSessionCapturer,
)
from rosseta_stone_script_a.application.use_cases.complete_foundations import (
    CompleteFoundationsUseCase,
)
from rosseta_stone_script_a.application.use_cases.go_to_fluency_builder import (
    GoToFundationsUseCase,
)
from rosseta_stone_script_a.application.use_cases.login_rosseta import (
    LoginRossetaUseCase,
)
from rosseta_stone_script_a.infrastructure.adapters.foundations_api.playwright_foundations_api import (
    PlaywrightFoundationsApiAdapter,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.dashboard_page import (
    DashboardPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.login_page import (
    LoginPage,
)


class DependencyFactory:
    """Factory for creating orchestrators with proper dependency injection."""

    def __init__(
        self,
        web_session: IWebSession,
        rosseta_login_url: str,
        units_to_complete: list[int] = None,
        target_score_percent: int = 100,
        max_start_time_offset_ms: int = 432000000,
        inter_path_delay_ms: int = 500,
    ):
        self.web_session = web_session
        self.rosseta_login_url = rosseta_login_url
        self.units_to_complete = units_to_complete or []
        self.target_score_percent = target_score_percent
        self.max_start_time_offset_ms = max_start_time_offset_ms
        self.inter_path_delay_ms = inter_path_delay_ms

    def create_open_fundations(self) -> OpenFundations:
        """Create OpenFluencyBuilder orchestrator with dependencies."""
        # Create pages
        login_page = LoginPage(
            web_session=self.web_session, rosetta_login_url=self.rosseta_login_url
        )
        dashboard_page = DashboardPage(web_session=self.web_session)

        # Create services
        session_capturer = RosettaSessionCapturer()

        # Create adapters
        # Access the underlying Playwright page to get the request context
        # This assumes PlaywrightWebSession exposes _page or we can get context from it
        # Ideally, IWebSession should expose a way to get an API adapter or context
        # For now, we'll access the protected _page attribute as we know the implementation
        page = getattr(self.web_session, "_page", None)
        if not page:
            raise RuntimeError("Web session not initialized correctly")

        foundations_api_adapter = PlaywrightFoundationsApiAdapter(page.request)

        # Create use cases
        login_use_case = LoginRossetaUseCase(
            web_session=self.web_session, login_page=login_page
        )
        navigate_use_case = GoToFundationsUseCase(
            web_session=self.web_session,
            dashboard_page=dashboard_page,
            session_capturer=session_capturer,
        )
        complete_foundations_use_case = CompleteFoundationsUseCase(
            api_port=foundations_api_adapter,
            units_to_complete=self.units_to_complete,
            target_score_percent=self.target_score_percent,
            max_start_time_offset_ms=self.max_start_time_offset_ms,
            inter_path_delay_ms=self.inter_path_delay_ms,
        )

        # Create orchestrator
        return OpenFundations(
            login_use_case=login_use_case,
            navigate_use_case=navigate_use_case,
            complete_foundations_use_case=complete_foundations_use_case,
        )
