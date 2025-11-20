# Session management
# Control interfaces
from .control import (
    InteractorPort,
    NavigatorPort,
    ScreenShootterPort,
    Selector,
    SelectorKind,
)

# Diagnostics and debugging
from .diagnostics import CookieConsentPort, DebugDumperPort

# Page-specific interfaces
from .page import AuthPort
from .session import BrowserProviderPort, IWebSession

__all__ = [
    # Session management
    "BrowserProviderPort",
    "IWebSession",
    # Control interfaces
    "InteractorPort",
    "NavigatorPort",
    "ScreenShootterPort",
    "Selector",
    "SelectorKind",
    # Page-specific interfaces
    "AuthPort",
    # Diagnostics and debugging
    "CookieConsentPort",
    "DebugDumperPort",
]
