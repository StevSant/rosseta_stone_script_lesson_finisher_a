from rosseta_stone_script_a.application.orchestrators.complete_lesson_workflow import (
    CompleteLessonWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.full_learning_session import (
    FullLearningSession,
)

from rosseta_stone_script_a..application.orchestrators.open_fluency_builder import (
    OpenFluencyBuilder,
)
from rosseta_stone_script_a.application.orchestrators.select_activity_workflow import (
    SelectActivityWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.select_course_workflow import (
    SelectCourseWorkflow,
)
from rosseta_stone_script_a.application.orchestrators.select_lesson_workflow import (
    SelectLessonWorkflow,
)

from rosseta_stone_script_a.application.ports.web import IWebSession
from rosseta_stone_script_a.application.use_cases.exit_lesson import ExitLessonUseCase
from rosseta_stone_script_a.application.use_cases.go_to_fluency_builder import (
    GoToFluencyBuilderUseCase,
)
from rosseta_stone_script_a.application.use_cases.login_rosseta import (
    LoginRossetaUseCase,
)
from rosseta_stone_script_a.application.use_cases.play_lesson_flow import (
    PlayLessonFlowUseCase,
)
from rosseta_stone_script_a.application.use_cases.play_activity_flow import (
    PlayActivityFlowUseCase,
)
from rosseta_stone_script_a.application.use_cases.select_activity import (
    SelectActivityUseCase,
)
from rosseta_stone_script_a.application.use_cases.select_course import (
    SelectCourseUseCase,
)
from rosseta_stone_script_a.application.use_cases.select_lesson import (
    SelectLessonUseCase,
)
from rosseta_stone_script_a.application.use_cases.start_or_resume_activity import (
    StartOrResumeActivityUseCase,
)


from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.activity_catalog_page import (
    ActivityCatalogPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.course_catalog_page import (
    CourseCatalogPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.dashboard_page import (
    DashboardPage,
)

from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.lesson_catalog_page import (
    LessonCatalogPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.lesson_player_page import (
    LessonPlayerPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.activity_player_page import (
    ActivityPlayerPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.login_page import (
    LoginPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.unit_catalog_page import (
    UnitCatalogPage,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.page.unit_lessons_page import (
    UnitLessonsPage,
)


class DependencyFactory:
    """Factory for creating orchestrators with proper dependency injection."""

    def __init__(self, web_session: IWebSession, rosseta_login_url: str):
        self.web_session = web_session
        self.rosseta_login_url = rosseta_login_url

    def create_open_fluency_builder(self) -> OpenFluencyBuilder:
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
        navigate_use_case = GoToFluencyBuilderUseCase(
            web_session=self.web_session, dashboard_page=dashboard_page
        )

        # Create orchestrator
        return OpenFluencyBuilder(
            login_use_case=login_use_case, navigate_use_case=navigate_use_case
        )

    def create_complete_lesson_workflow(self) -> CompleteLessonWorkflow:
        """Create CompleteLessonWorkflow orchestrator with dependencies."""
        # Create pages
        lesson_player_page = LessonPlayerPage(web_session=self.web_session)
        activity_player_page = ActivityPlayerPage(web_session=self.web_session)

        # Create use cases
        play_lesson_use_case = PlayLessonFlowUseCase(
            web_session=self.web_session, lesson_player_page=lesson_player_page
        )
        play_activity_use_case = PlayActivityFlowUseCase(
            web_session=self.web_session, activity_player_page=activity_player_page
        )
        exit_lesson_use_case = ExitLessonUseCase(
            web_session=self.web_session, lesson_player_page=lesson_player_page
        )

        # Create orchestrator
        return CompleteLessonWorkflow(
            play_lesson_use_case=play_lesson_use_case,
            exit_lesson_use_case=exit_lesson_use_case,
        )

    def create_select_course_workflow(self) -> SelectCourseWorkflow:
        """Create SelectCourseWorkflow orchestrator with dependencies."""
        # Create pages
        course_catalog_page = CourseCatalogPage(web_session=self.web_session)

        # Create use cases
        select_course_use_case = SelectCourseUseCase(
            web_session=self.web_session,
            course_catalog_page=course_catalog_page,
        )

        # Create orchestrator
        return SelectCourseWorkflow(
            select_course_use_case=select_course_use_case,
        )

    def create_select_lesson_workflow(self) -> SelectLessonWorkflow:
        """Create SelectLessonWorkflow orchestrator with dependencies."""
        # Create pages
        lesson_catalog_page = LessonCatalogPage(web_session=self.web_session)

        # Create use cases
        select_lesson_use_case = SelectLessonUseCase(
            web_session=self.web_session,
            lesson_catalog_page=lesson_catalog_page,
        )

        # Create orchestrator
        return SelectLessonWorkflow(
            select_lesson_use_case=select_lesson_use_case,
        )

    def create_select_activity_workflow(self) -> SelectActivityWorkflow:
        """Create SelectActivityWorkflow orchestrator with dependencies."""
        # Create pages
        activity_catalog_page = ActivityCatalogPage(web_session=self.web_session)

        # Create use cases
        select_activity_use_case = SelectActivityUseCase(
            web_session=self.web_session,
            activity_catalog_page=activity_catalog_page,
        )
        start_activity_use_case = StartOrResumeActivityUseCase(
            web_session=self.web_session,
            activity_catalog_page=activity_catalog_page,
        )

        # Create orchestrator
        return SelectActivityWorkflow(
            select_activity_use_case=select_activity_use_case,
            start_activity_use_case=start_activity_use_case,
        )

    def create_full_learning_session(
        self,
    ) -> FullLearningSession:
        """Create FullHierarchicalLearningSession orchestrator with all dependencies."""
        open_fluency_builder = self.create_open_fluency_builder()
        select_course_workflow = self.create_select_course_workflow()
        select_lesson_workflow = self.create_select_lesson_workflow()
        select_activity_workflow = self.create_select_activity_workflow()
        complete_lesson_workflow = self.create_complete_lesson_workflow()

        return FullLearningSession(
            open_fluency_builder=open_fluency_builder,
            select_course_workflow=select_course_workflow,
            select_lesson_workflow=select_lesson_workflow,
            select_activity_workflow=select_activity_workflow,
            complete_lesson_workflow=complete_lesson_workflow,
        )
