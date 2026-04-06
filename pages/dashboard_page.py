from playwright.sync_api import Page, Locator
from core.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_title: Locator = page.locator('[data-testid="dashboard-title"]')
        self.welcome_message: Locator = page.locator('[data-testid="welcome-message"]')
        self.logout_button: Locator = page.locator('[data-testid="logout-button"]')
        self.profile_link: Locator = page.locator('[data-testid="profile-link"]')
        self.settings_link: Locator = page.locator('[data-testid="settings-link"]')

    def is_title_visible(self) -> bool:
        return self.is_visible(self.dashboard_title)

    def get_welcome_message(self) -> str:
        self.wait_for_visible(self.welcome_message)
        return self.get_text(self.welcome_message)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.welcome_message)

    def click_logout(self) -> None:
        self.click_and_wait(self.logout_button)

    def click_profile(self) -> None:
        self.click_and_wait(self.profile_link)

    def click_settings(self) -> None:
        self.click_and_wait(self.settings_link)
