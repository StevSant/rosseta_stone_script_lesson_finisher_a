from __future__ import annotations

from dataclasses import dataclass

from rosseta_stone_script_a.application.ports.web import AuthPort, IWebSession, Selector
from rosseta_stone_script_a.domain.entities.credentials import Credentials
from rosseta_stone_script_a.infrastructure.adapters.web.playwright.patterns import (
    AuthPatterns,
)
from rosseta_stone_script_a.shared.utils.compile_case_insensitive import (
    compile_case_insensitive,
)

cci = compile_case_insensitive


@dataclass(frozen=True)
class LoginPagePatterns:
    """Local patterns specific to the login page."""

    EMAIL_LABEL = cci(r"correo\s*electr[óo]nico|email\s*address")
    PASSWORD_LABEL = cci(r"contrase[ñn]a|password")


class LoginPage(AuthPort):
    """
    Page Object del Login que usa selectores semánticos (regex permitido en patrones).
    Todas las acciones pasan por self.web_session.interactor.
    """

    def __init__(
        self,
        web_session: IWebSession,
        rosetta_login_url: str,
    ) -> None:
        super().__init__()
        self.web_session = web_session
        self.rosetta_login_url = rosetta_login_url

        # --- Selectors ---

        self.EMAIL_INPUT = Selector.role_textbox(
            name_pattern=LoginPagePatterns.EMAIL_LABEL
        )
        self.PASSWORD_INPUT = Selector.role_textbox(
            name_pattern=LoginPagePatterns.PASSWORD_LABEL
        )
        self.SIGN_IN_BTN = Selector.role_button(name_pattern=AuthPatterns.SIGN_IN)

    async def login(self, creds: "Credentials") -> None:
        """Implementation of AuthPort interface using Credentials."""
        self.logger.info("Starting login process")

        await self.web_session.navigator.go_to(
            self.rosetta_login_url, wait_for_load=True
        )
        self.logger.info("Navigated to login URL")

        await self.web_session.debug_dumpper.dump_screenshot("before_login")

        # Fill email using interactor with Selector
        self.logger.info(f"Filling email field for user: {creds.email}")
        await self.web_session.interactor.fill(self.EMAIL_INPUT, str(creds.email))

        # Fill password using interactor with Selector
        self.logger.info("Filling password field")
        await self.web_session.interactor.fill(self.PASSWORD_INPUT, creds.password)

        # Click submit button using interactor with Selector
        self.logger.info("Clicking sign-in button")
        await self.web_session.interactor.click(self.SIGN_IN_BTN)

        await self.web_session.navigator.wait_for_load()
        self.logger.info("Login process completed successfully")
