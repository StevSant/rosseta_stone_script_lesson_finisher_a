import asyncio
import random
import time

from rosseta_stone_script_a.application.ports.foundations_api import FoundationsApiPort
from rosseta_stone_script_a.application.ports.use_case import UseCasePort
from rosseta_stone_script_a.application.services.content_filter import ContentFilter
from rosseta_stone_script_a.application.services.path_calculator import PathCalculator
from rosseta_stone_script_a.domain.entities.completion_stats import CompletionStats
from rosseta_stone_script_a.domain.entities.path import Path


class CompleteFoundationsUseCase(UseCasePort):
    """
    Use case for automatically completing Rosetta Stone Foundations lessons.
    """

    def __init__(
        self,
        api_port: FoundationsApiPort,
        units_to_complete: list[int] = None,
        lessons_to_complete: list[int] = None,
        path_types_to_complete: list[str] = None,
        target_score_percent: int = 100,
        max_start_time_offset_ms: int = 432000000,
        inter_path_delay_ms: int = 500,
        force_recomplete: bool = False,
    ):
        self.api_port = api_port
        self.stats = CompletionStats()

        # Initialize services
        self.content_filter = ContentFilter(
            units_to_complete=units_to_complete,
            lessons_to_complete=lessons_to_complete,
            path_types_to_complete=path_types_to_complete,
            force_recomplete=force_recomplete,
        )
        self.path_calculator = PathCalculator(
            target_score_percent=target_score_percent,
            max_start_time_offset_ms=max_start_time_offset_ms,
        )
        self.inter_path_delay_ms = inter_path_delay_ms

    async def execute(
        self,
        authorization: str,
        language_code: str,
        session_token: str,
        school_id: str,
        user_id: str,
    ) -> CompletionStats:
        """
        Execute the completion process.

        Args:
            authorization: GraphQL authorization token (JWT)
            language_code: Language code (e.g., ENG)
            session_token: REST API session token
            school_id: School ID
            user_id: User ID

        Returns:
            CompletionStats: Statistics about what was completed
        """
        # Reset stats for this execution
        self.stats = CompletionStats()

        self.logger.info("Starting Foundations completion process...")
        if self.content_filter.units_to_complete:
            self.logger.info(
                f"Target units to complete: {self.content_filter.units_to_complete}"
            )
        else:
            self.logger.info("No specific units configured. Processing ALL units.")
        if self.content_filter.lessons_to_complete:
            self.logger.info(
                f"Target lessons to complete: {self.content_filter.lessons_to_complete}"
            )
        else:
            self.logger.info("No specific lessons configured. Processing ALL lessons.")
        if self.content_filter.path_types_to_complete:
            self.logger.info(
                f"Target path types to complete: {self.content_filter.path_types_to_complete}"
            )
        else:
            self.logger.info(
                "No specific path types configured. Processing ALL path types."
            )

        # 1. Fetch Course Menu
        try:
            course_menu = await self.api_port.get_course_menu(
                authorization, language_code
            )
        except Exception as e:
            self.logger.error(f"Failed to get course menu: {e}")
            return

        self.logger.info(f"Fetched course menu. Total units: {len(course_menu.units)}")

        # 2. Iterate through units
        tasks = []
        sem = asyncio.Semaphore(50)  # Allow 50 concurrent requests

        async def sem_task(task):
            async with sem:
                await task

        for unit in course_menu.units:
            # Filter units if configured
            if not self.content_filter.should_process_unit(unit):
                self.content_filter.log_skip_reason(
                    "Unit", unit.unit_number, "not in target list"
                )
                continue

            self.logger.info(f"Processing Unit {unit.unit_number}")
            self.stats.total_units_processed += 1
            self.stats.units_completed.append(unit.unit_number)

            # Start Time should reset for each unit
            start_time = int(time.time() * 1000) - random.randint(
                0, self.path_calculator.max_start_time_offset_ms
            )
            time_so_far = 0

            for lesson in unit.lessons:
                # Filter lessons if configured
                if not self.content_filter.should_process_lesson(lesson):
                    self.content_filter.log_skip_reason(
                        "Lesson", lesson.lesson_number, "not in target list"
                    )
                    continue

                self.logger.info(f"  Processing Lesson {lesson.lesson_number}")
                self.stats.total_lessons_processed += 1

                for path in lesson.paths:
                    # Log all review paths for debugging
                    if path.type == "review":
                        self.logger.info(
                            f"    [DEBUG] Review found: complete={path.complete}, percent_complete={path.percent_complete}%"
                        )

                    # Filter path types if configured and check completion
                    should_process = self.content_filter.should_process_path(path)

                    if not should_process:
                        # Log why we're skipping
                        if path.type not in (
                            self.content_filter.path_types_to_complete or []
                        ):
                            self.logger.info(
                                f"    Skipping {path.type}: not in target list"
                            )
                        elif path.complete and path.percent_complete >= 100:
                            self.logger.info(
                                f"    Skipping {path.type}: already 100% complete"
                            )
                        else:
                            self.logger.info(
                                f"    Skipping {path.type}: filtered by configuration (complete={path.complete}, percent={path.percent_complete}%)"
                            )
                        self.stats.total_paths_skipped += 1
                        continue

                    # Log if we're forcing recomplete or processing incomplete path
                    if self.content_filter.force_recomplete and path.complete:
                        self.logger.info(
                            f"    FORCE RE-COMPLETING {path.type} (was marked complete)"
                        )
                    elif path.complete and path.percent_complete < 100:
                        self.logger.info(
                            f"    Processing {path.type}: {path.percent_complete}% complete (will complete to 100%)"
                        )

                    # Track path type
                    self.stats.paths_by_type[path.type] = (
                        self.stats.paths_by_type.get(path.type, 0) + 1
                    )
                    self.stats.total_paths_completed += 1

                    task = self._complete_path(
                        path=path,
                        session_token=session_token,
                        school_id=school_id,
                        user_id=user_id,
                        start_time=start_time,
                        time_so_far=time_so_far,
                    )
                    tasks.append(sem_task(task))

                    # Update time_so_far for next path using calculator
                    time_so_far += self.path_calculator.calculate_next_time_increment(
                        path.time_estimate
                    )

        if tasks:
            self.logger.info(f"Executing {len(tasks)} tasks concurrently...")
            await asyncio.gather(*tasks)
        else:
            self.logger.info("No tasks to execute.")

        self.logger.info("Foundations completion process finished.")
        return self.stats

    async def _complete_path(
        self,
        path: Path,
        session_token: str,
        school_id: str,
        user_id: str,
        start_time: int,
        time_so_far: int,
    ) -> None:
        """Complete a single path using the API."""
        # Calculate time and score using calculator service
        calculation = self.path_calculator.calculate_path_completion(
            path, start_time, time_so_far
        )

        self.logger.info(
            f"    Completing path: {path.type} (Course: {path.course}, Unit: {path.unit_index}, Lesson: {path.lesson_index})"
        )

        await self.api_port.update_path_score(
            session_token=session_token,
            school_id=school_id,
            user_id=user_id,
            course=path.course,
            unit_index=path.unit_index % 4,
            lesson_index=path.curriculum_lesson_index,
            path_type=path.type,
            score_correct=calculation.questions_correct,
            score_incorrect=calculation.questions_incorrect,
            duration_ms=calculation.time_in_milliseconds,
            timestamp_ms=calculation.time_completed,
            num_challenges=path.num_challenges,
        )
