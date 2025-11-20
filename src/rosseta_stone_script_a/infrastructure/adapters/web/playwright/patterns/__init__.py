"""Pattern definitions for web element matching.

This package re-exports grouped pattern classes. Modules are split by concern
to keep the `patterns` package modular (auth, navigation, form, modal).
"""

from .auth_patterns import AuthPatterns
from .form_patterns import FormPatterns
from .lesson_patterns import ActivityPatterns, LessonPatterns, PlayerPatterns
from .modal_patterns import ModalPatterns
from .navigation_patterns import NavigationPatterns

__all__ = [
    "AuthPatterns",
    "NavigationPatterns",
    "FormPatterns",
    "ModalPatterns",
    "LessonPatterns",
    "PlayerPatterns",
    "ActivityPatterns",
]
