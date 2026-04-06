from playwright.sync_api import Page, Locator
from core.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator('[data-testid="username"]')
        self.password_input: Locator = page.locator('[data-testid="password"]')
        self.login_button: Locator = page.locator('[data-testid="login-button"]')
        self.error_message: Locator = page.locator('[data-testid="error-message"]')
        self.remember_me: Locator = page.locator('[data-testid="remember-me"]')
        self.logo: Locator = page.locator('[data-testid="logo"]')
        self.forgot_password: Locator = page.locator('[data-testid="forgot-password"]')

    def goto(self, base_url: str) -> None:
        if base_url.endswith("demo_app.html"):
            self.navigate_to(base_url)
        else:
            self.navigate_to(f"{base_url}/demo_app.html")

    def login(self, username: str, password: str, remember: bool = False) -> None:
        self.wait_for_visible(self.username_input)
        self.fill_and_verify(self.username_input, username)
        self.fill_and_verify(self.password_input, password)

        if remember:
            self.check(self.remember_me)

        self.click_and_wait(self.login_button)

    def get_error_message(self) -> str:
        self.wait_for_visible(self.error_message)
        return self.get_text(self.error_message)

    def is_login_button_enabled(self) -> bool:
        return self.is_enabled(self.login_button)

    def is_login_form_visible(self) -> bool:
        return (
            self.is_visible(self.username_input)
            and self.is_visible(self.password_input)
            and self.is_visible(self.login_button)
        )

    def click_forgot_password(self) -> None:
        self.click_and_wait(self.forgot_password)

    def get_page_title(self) -> str:
        return self.get_title()
