"""Pattern definitions for web element matching.

This package re-exports grouped pattern classes. Modules are split by concern
to keep the `patterns` package modular (auth, navigation, form, modal).
"""

from .auth_patterns import AuthPatterns
from .form_patterns import FormPatterns

__all__ = [
    "AuthPatterns",
    "FormPatterns",
]
