import asyncio
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict

from rosseta_stone_script_a.application.ports.foundations_api import FoundationsApiPort
from rosseta_stone_script_a.application.ports.use_case import UseCasePort
from rosseta_stone_script_a.domain.entities.path import Path


@dataclass
class CompletionStats:
    """Statistics about the completion process."""

    total_units_processed: int = 0
    total_lessons_processed: int = 0
    total_paths_completed: int = 0
    total_paths_skipped: int = 0  # Already completed
    units_completed: list = field(default_factory=list)
    paths_by_type: Dict[str, int] = field(default_factory=dict)
    errors: list = field(default_factory=list)


class CompleteFoundationsUseCase(UseCasePort):
    """
    Use case for automatically completing Rosetta Stone Foundations lessons.
    """

    def __init__(
        self,
        api_port: FoundationsApiPort,
        units_to_complete: list[int] = None,
        target_score_percent: int = 100,
        max_start_time_offset_ms: int = 432000000,
        inter_path_delay_ms: int = 500,
    ):
        self.api_port = api_port
        self.units_to_complete = units_to_complete or []
        self.target_score_percent = target_score_percent
        self.max_start_time_offset_ms = max_start_time_offset_ms
        self.inter_path_delay_ms = inter_path_delay_ms
        self.stats = CompletionStats()

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
        if self.units_to_complete:
            self.logger.info(f"Target units to complete: {self.units_to_complete}")
        else:
            self.logger.info("No specific units configured. Processing ALL units.")

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
            if (
                self.units_to_complete
                and unit.unit_number not in self.units_to_complete
            ):
                self.logger.debug(
                    f"Skipping Unit {unit.unit_number} (not in target list)"
                )
                continue

            self.logger.info(f"Processing Unit {unit.unit_number}")
            self.stats.total_units_processed += 1
            self.stats.units_completed.append(unit.unit_number)
            # Start Time should reset for each unit (logic from JS)
            # JS: const startTime = Date.now() - getRndInteger(0, 432000000);
            start_time = int(time.time() * 1000) - random.randint(
                0, self.max_start_time_offset_ms
            )
            time_so_far = 0

            for lesson in unit.lessons:
                self.logger.info(f"  Processing Lesson {lesson.lesson_number}")
                self.stats.total_lessons_processed += 1

                for path in lesson.paths:
                    if path.complete:
                        self.logger.debug(f"    Skipping completed path: {path.type}")
                        self.stats.total_paths_skipped += 1
                        continue

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

                    # Update time_so_far for next path
                    # Logic from JS:
                    # timeInMinutes = timeEstimate + getRndInteger(...)
                    # timeInMilliseconds = timeInMinutes * 60000 + getRndInteger(...)
                    # timeSoFar += timeInMilliseconds + getRndInteger(...)

                    time_estimate = path.time_estimate
                    time_in_minutes = time_estimate + random.randint(
                        -1 * math.floor(time_estimate / 3),
                        math.floor(time_estimate / 3),
                    )
                    time_in_milliseconds = time_in_minutes * 60000 + random.randint(
                        0, 6000
                    )

                    time_so_far += time_in_milliseconds + random.randint(0, 60000)

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
        # Calculate time and score
        time_estimate = path.time_estimate
        time_in_minutes = time_estimate + random.randint(
            -1 * math.floor(time_estimate / 3), math.floor(time_estimate / 3)
        )
        time_in_milliseconds = time_in_minutes * 60000 + random.randint(0, 6000)

        # JS: const percentCorrect = 100;
        percent_correct = self.target_score_percent
        questions_correct = math.ceil(path.num_challenges * (percent_correct / 100))

        # JS: let timeCompleted = startTime + timeSoFar;
        time_completed = start_time + time_so_far + time_in_milliseconds

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
            score_correct=questions_correct,
            score_incorrect=path.num_challenges - questions_correct,
            duration_ms=time_in_milliseconds,
            timestamp_ms=time_completed,
            num_challenges=path.num_challenges,
        )
