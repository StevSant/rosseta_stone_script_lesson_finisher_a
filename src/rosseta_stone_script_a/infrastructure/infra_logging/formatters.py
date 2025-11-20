# infrastructure/logging/formatters.py
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from .utils import relpath


class RelPathFormatter(logging.Formatter):
    """Añade record.relpath para usarlo en formatos."""

    def __init__(self, *args, project_root, **kwargs):
        super().__init__(*args, **kwargs)
        self._project_root = project_root

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        try:
            pathname = getattr(record, "pathname", "") or ""
            record.relpath = relpath(pathname, self._project_root)  # type: ignore[attr-defined]
        except Exception:
            record.relpath = getattr(record, "filename", "")  # type: ignore[attr-defined]
        return super().format(record)


class JsonFormatter(logging.Formatter):
    """JSON formatter minimalista: ideal para Prod / parsers (ELK/Datadog)."""

    def __init__(self, *, project_root, datefmt="%Y-%m-%dT%H:%M:%S"):
        super().__init__(datefmt=datefmt)
        self._project_root = project_root
        self._datefmt = datefmt

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        # Prepara relpath
        try:
            pathname = getattr(record, "pathname", "") or ""
            rel = relpath(pathname, self._project_root)
        except Exception:
            rel = getattr(record, "filename", "") or ""

        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).strftime(self._datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno,
            "path": rel,
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)
