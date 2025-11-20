from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from rosseta_stone_script_a.application.ports.web import (
    CookieConsentPort,
    InteractorPort,
    Selector,
)
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.patterns import (
    ModalPatterns,
    NavigationPatterns,
)
from rosseta_stone_script_a.shared.mixins.loggin_mixin import LoggingMixin


class CookieConsentAdapter(CookieConsentPort, LoggingMixin):
    def __init__(self, interactor: InteractorPort) -> None:
        super().__init__()
        self.interactor = interactor

        # --- Selectors ---
        self.ACCEPT_BTN = Selector.role_button(name_pattern=ModalPatterns.ACCEPT)
        self.CLOSE_BTN = Selector.role_button(name_pattern=NavigationPatterns.CLOSE)

    async def dismiss(self) -> bool:
        # 1) Intentar ACEPTAR
        try:
            self.logger.info("Attempting to dismiss cookie consent...")
            if await self.interactor.exists(self.ACCEPT_BTN, timeout=2000):
                await self.interactor.click_first(self.ACCEPT_BTN, timeout=2000)
                self.logger.info("Cookie banner accepted.")
                return True
            else:
                self.logger.info("No accept button found or not enabled.")
        except PlaywrightTimeoutError as e:
            self.logger.info(f"Cookie banner accept timeout: {e}")
        except Exception as e:
            self.logger.info(f"Cookie banner accept failed: {e}")

        # 2) Intentar CERRAR
        try:
            self.logger.info("Attempting to close cookie consent...")
            if await self.interactor.exists(self.CLOSE_BTN, timeout=2000):
                await self.interactor.click_first(self.CLOSE_BTN, timeout=2000)
                self.logger.info("Cookie banner closed.")
                return True
            else:
                self.logger.info("No close button found or not enabled.")
        except PlaywrightTimeoutError as e:
            self.logger.info(f"Cookie close timeout: {e}")
        except Exception as e:
            self.logger.info(f"Cookie close failed: {e}")

        return False
