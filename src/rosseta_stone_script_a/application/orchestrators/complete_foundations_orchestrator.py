import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

from rosseta_stone_script_a.application.ports.orchestrator import OrchestratorPort
from rosseta_stone_script_a.application.use_cases.complete_foundations import (
    CompleteFoundationsUseCase,
    CompletionStats,
)

# Total units in Rosetta Stone Foundations
TOTAL_UNITS = 20


class CompleteFoundationsOrchestrator(OrchestratorPort):
    """
    Orchestrator that handles the completion of Foundations lessons.
    """

    def __init__(self, complete_foundations_use_case: CompleteFoundationsUseCase):
        super().__init__()
        self.complete_foundations_use_case = complete_foundations_use_case
        self.output_dir = Path("logs/user_data")

    async def execute(self, captured_data: Dict[str, Any]) -> None:
        """
        Execute the completion workflow using captured session data.

        Args:
            captured_data: Data captured from the session (tokens, ids, user_name, credentials, etc.)
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

    def _get_safe_name(self, user_name: str | None) -> str:
        """Generate a safe filename prefix from user name."""
        if user_name:
            safe_name = re.sub(r"[^\w\s-]", "", user_name)
            safe_name = re.sub(r"\s+", "_", safe_name).strip("_")
            return safe_name
        return "unknown_user"

    def _get_previous_reports(self, safe_name: str) -> List[Path]:
        """Find all previous reports for a user."""
        if not self.output_dir.exists():
            return []
        # Match files that start with the user's safe name
        pattern = f"{safe_name}_*.txt"
        return sorted(self.output_dir.glob(pattern))

    def _extract_completed_units_from_report(self, report_path: Path) -> Set[int]:
        """Extract completed units from a previous report."""
        completed_units = set()
        try:
            content = report_path.read_text(encoding="utf-8")
            # Look for the line with units completed, e.g., "  Units Completed: [1, 2, 3, 4, 5]"
            match = re.search(
                r"Units Completed \(this session\):\s*\[([^\]]+)\]", content
            )
            if match:
                units_str = match.group(1)
                for unit in units_str.split(","):
                    unit = unit.strip()
                    if unit.isdigit():
                        completed_units.add(int(unit))
        except Exception as e:
            self.logger.warning(f"Could not read previous report {report_path}: {e}")
        return completed_units

    def _get_all_historically_completed_units(self, safe_name: str) -> Set[int]:
        """Get all units completed across all previous reports for this user."""
        all_completed = set()
        previous_reports = self._get_previous_reports(safe_name)
        for report_path in previous_reports:
            completed = self._extract_completed_units_from_report(report_path)
            all_completed.update(completed)
            self.logger.debug(f"From {report_path.name}: found units {completed}")
        return all_completed

    async def _generate_report(
        self,
        user_name: str | None,
        stats: CompletionStats,
        captured_data: Dict[str, Any],
    ) -> None:
        """Generate a completion report with user info and statistics."""
        try:
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with user name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self._get_safe_name(user_name)
            file_name = f"{safe_name}_{timestamp}.txt"
            file_path = self.output_dir / file_name

            # Get historically completed units from previous reports
            historically_completed = self._get_all_historically_completed_units(
                safe_name
            )
            self.logger.info(
                f"Previously completed units (from history): {sorted(historically_completed)}"
            )

            # Current session completed units
            current_completed = set(stats.units_completed)

            # All completed units (history + current)
            all_completed = historically_completed.union(current_completed)

            # Calculate pending units
            all_units = set(range(1, TOTAL_UNITS + 1))
            pending_units = sorted(all_units - all_completed)

            # Get credentials
            credentials = captured_data.get("credentials", {})
            email = credentials.get("email", "N/A")
            password = credentials.get("password", "N/A")

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
                "CREDENTIALS USED",
                "-" * 40,
                f"  Email: {email}",
                f"  Password: {password}",
                "",
                "SESSION INFORMATION",
                "-" * 40,
                f"  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "COMPLETION STATISTICS (THIS SESSION)",
                "-" * 40,
                f"  Units Processed: {stats.total_units_processed}",
                f"  Units Completed (this session): {sorted(stats.units_completed)}",
                f"  Lessons Processed: {stats.total_lessons_processed}",
                f"  Paths Completed: {stats.total_paths_completed}",
                f"  Paths Skipped (already done): {stats.total_paths_skipped}",
                "",
                "HISTORICAL PROGRESS",
                "-" * 40,
                f"  Previously Completed Units: {sorted(historically_completed) if historically_completed else 'None'}",
                f"  All Completed Units (total): {sorted(all_completed)}",
                f"  Total Units Completed: {len(all_completed)} / {TOTAL_UNITS}",
                "",
                "PENDING UNITS",
                "-" * 40,
                f"  Units Still Pending: {pending_units if pending_units else 'None - All Complete!'}",
                f"  Total Pending: {len(pending_units)} / {TOTAL_UNITS}",
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
