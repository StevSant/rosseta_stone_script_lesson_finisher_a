import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.complete_foundations import (
    CompleteFoundationsUseCase,
    CompletionStats,
)


class CompleteFoundationsOrchestrator(OrchestratorPort):
    """
    Orchestrator that handles the completion of Foundations lessons.
    """

    def __init__(self, complete_foundations_use_case: CompleteFoundationsUseCase):
        super().__init__()
        self.complete_foundations_use_case = complete_foundations_use_case

    async def execute(self, captured_data: Dict[str, Any]) -> None:
        """
        Execute the completion workflow using captured session data.

        Args:
            captured_data: Data captured from the session (tokens, ids, user_name, etc.)
        """
        user_name = captured_data.get("user_name")

        # Check required session data (excluding user_name which is optional for report)
        required_keys = [
            "authorization",
            "lang_code",
            "session_token",
            "school_id",
            "user_id",
        ]
        missing_keys = [k for k in required_keys if not captured_data.get(k)]

        if missing_keys:
            self.logger.warning(
                f"Missing captured session data: {missing_keys}. Skipping completion."
            )
            self.logger.debug(f"Captured data state: {captured_data}")
            return

        self.logger.info("Session data captured successfully. Starting completion...")
        stats = await self.complete_foundations_use_case.execute(
            authorization=captured_data["authorization"],
            language_code=captured_data["lang_code"],
            session_token=captured_data["session_token"],
            school_id=captured_data["school_id"],
            user_id=captured_data["user_id"],
        )

        # Generate completion report
        await self._generate_report(user_name, stats, captured_data)

    async def _generate_report(
        self,
        user_name: str | None,
        stats: CompletionStats,
        captured_data: Dict[str, Any],
    ) -> None:
        """Generate a completion report with user info and statistics."""
        try:
            # Create output directory
            output_dir = Path("logs/user_data")
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with user name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if user_name:
                # Sanitize name for filename: replace spaces with underscores, remove special chars
                safe_name = re.sub(r"[^\w\s-]", "", user_name)
                safe_name = re.sub(r"\s+", "_", safe_name).strip("_")
                file_name = f"{safe_name}_{timestamp}.txt"
            else:
                file_name = f"unknown_user_{timestamp}.txt"

            file_path = output_dir / file_name

            # Build report content
            report_lines = [
                "=" * 60,
                "ROSETTA STONE - COMPLETION REPORT",
                "=" * 60,
                "",
                "USER INFORMATION",
                "-" * 40,
                f"  Name: {user_name or 'Unknown'}",
                f"  User ID: {captured_data.get('user_id', 'N/A')}",
                f"  School ID: {captured_data.get('school_id', 'N/A')}",
                f"  Language: {captured_data.get('lang_code', 'N/A')}",
                "",
                "SESSION INFORMATION",
                "-" * 40,
                f"  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "COMPLETION STATISTICS",
                "-" * 40,
                f"  Units Processed: {stats.total_units_processed}",
                f"  Units Completed: {stats.units_completed}",
                f"  Lessons Processed: {stats.total_lessons_processed}",
                f"  Paths Completed: {stats.total_paths_completed}",
                f"  Paths Skipped (already done): {stats.total_paths_skipped}",
                "",
                "PATHS BY TYPE",
                "-" * 40,
            ]

            # Add paths by type
            for path_type, count in sorted(stats.paths_by_type.items()):
                report_lines.append(f"  {path_type}: {count}")

            if stats.errors:
                report_lines.extend(
                    [
                        "",
                        "ERRORS",
                        "-" * 40,
                    ]
                )
                for error in stats.errors:
                    report_lines.append(f"  - {error}")

            report_lines.extend(
                [
                    "",
                    "=" * 60,
                    "END OF REPORT",
                    "=" * 60,
                ]
            )

            # Write report
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines))

            self.logger.info(f"Completion report saved to {file_path}")

        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
