from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine


class NetworkMonitorPort(ABC):
    """Port for monitoring network traffic."""

    @abstractmethod
    def add_request_listener(
        self, listener: Callable[[Any], Coroutine[Any, Any, None]]
    ) -> None:
        """Add a listener for network requests."""
        ...

    @abstractmethod
    def remove_request_listener(
        self, listener: Callable[[Any], Coroutine[Any, Any, None]]
    ) -> None:
        """Remove a listener for network requests."""
        ...
