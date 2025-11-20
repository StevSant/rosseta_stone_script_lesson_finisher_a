from __future__ import annotations

import logging
import logging.config
import os
from typing import Literal

from .config import build_config
from .options import FileHandlerOptions, LoggingOptions
from .utils import detect_project_root


def _env_level(
    default: str = "INFO",
) -> Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    env = str(default).upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if env not in valid_levels:
        env = "INFO"
    return env  # type: ignore


def _default_options() -> LoggingOptions:
    project_root = detect_project_root()
    level = _env_level("INFO")

    logs_dir = project_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)  # 👈 asegura carpeta

    return LoggingOptions(
        level=level,
        project_root=project_root,
        file_info=FileHandlerOptions(
            enabled=True,
            level=level,
            filename=logs_dir / "dev.log",  # 👈 ruta absoluta
            rotation="size",
        ),
        file_error=FileHandlerOptions(
            enabled=True,
            level="ERROR",
            filename=logs_dir / "dev_errors.log",  # 👈 ruta absoluta
            rotation="size",
        ),
        use_json_formatter=os.getenv("LOG_JSON", "0") == "1",
    )


def setup_logging(options: LoggingOptions) -> logging.Logger:
    root = logging.getLogger()
    cfg = build_config(options)

    # Si ya hay handlers, revisa si ya existen los file handlers que necesitas.
    # Si faltan, reconfigura.
    has_file_handler = any(isinstance(h, logging.FileHandler) for h in root.handlers)

    if root.handlers and has_file_handler:
        # Ajusta nivel por si cambió
        desired = getattr(logging, options.level, logging.INFO)
        root.setLevel(desired)
        for h in root.handlers:
            h.setLevel(min(h.level or desired, desired))
        return logging.getLogger(options.logger_name)

    # Reconfigura (o configura por primera vez)
    logging.config.dictConfig(cfg)
    return logging.getLogger(options.logger_name)


def get_logger(name: str | None = None) -> logging.Logger:
    setup_logging(_default_options())
    return logging.getLogger(name or "app")
