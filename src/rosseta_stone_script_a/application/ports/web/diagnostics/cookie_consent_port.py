from abc import ABC, abstractmethod


class CookieConsentPort(ABC):
    @abstractmethod
    async def dismiss(self) -> bool: ...
