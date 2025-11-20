# infrastructure/logging/options.py
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Sequence

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
Rotation = Literal["size", "time", "none"]


@dataclass(frozen=True)
class FileHandlerOptions:
    enabled: bool = True
    level: LogLevel = "INFO"
    filename: Path | None = None  # p.ej. Path("logs/dev.log")
    rotation: Rotation = "size"
    max_bytes: int = 10_485_760  # 10MB
    backup_count: int = 5
    when: str = "midnight"  # para rotation="time"
    interval: int = 1
    encoding: str = "utf-8"
    delay: bool = True
    filters: Sequence[str] = ("exclude_venv",)


@dataclass(frozen=True)
class ConsoleHandlerOptions:
    enabled: bool = True
    level: LogLevel = "INFO"
    formatter: Literal["console", "detailed", "json"] = "console"
    filters: Sequence[str] = ("exclude_venv",)


@dataclass(frozen=True)
class LoggingOptions:
    level: LogLevel = "INFO"
    project_root: Path | None = None
    log_dir: Path | None = None
    console: ConsoleHandlerOptions = field(default_factory=ConsoleHandlerOptions)
    file_info: FileHandlerOptions = field(
        default_factory=lambda: FileHandlerOptions(
            level="INFO", filename=Path("logs/dev.log")
        )
    )
    file_error: FileHandlerOptions = field(
        default_factory=lambda: FileHandlerOptions(
            level="ERROR", filename=Path("logs/dev_errors.log")
        )
    )
    use_json_formatter: bool = False
    disable_existing_loggers: bool = False
    logger_name: str = "app"
    propagate: bool = False
