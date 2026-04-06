from playwright.sync_api import Page, Locator, expect
from typing import Optional
import logging


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate_to(self, path: str, base_url: Optional[str] = None) -> None:
        url = f"{base_url}{path}" if base_url else path
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="networkidle")

    def wait_for_visible(self, locator: Locator, timeout: int = 30000) -> None:
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: int = 30000) -> None:
        locator.wait_for(state="hidden", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 30000) -> Optional[Locator]:
        return self.page.wait_for_selector(selector, timeout=timeout)

    def fill_and_verify(self, locator: Locator, value: str) -> None:
        locator.clear()
        locator.fill(value)
        expect(locator).to_have_value(value)

    def click_and_wait(self, locator: Locator, timeout: int = 30000) -> None:
        locator.click(timeout=timeout)
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str, full_page: bool = False) -> bytes:
        return self.page.screenshot(path=f"screenshots/{name}.png", full_page=full_page)

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def is_visible(self, locator: Locator) -> bool:
        return locator.is_visible()

    def is_enabled(self, locator: Locator) -> bool:
        return locator.is_enabled()

    def get_text(self, locator: Locator) -> str:
        return locator.text_content() or ""

    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        return locator.get_attribute(attribute)

    def hover(self, locator: Locator) -> None:
        locator.hover()

    def check(self, locator: Locator) -> None:
        locator.check()

    def uncheck(self, locator: Locator) -> None:
        locator.uncheck()

    def select_option(self, locator: Locator, value: str) -> None:
        locator.select_option(value)

    def scroll_to_element(self, locator: Locator) -> None:
        locator.scroll_into_view_if_needed()

    def reload(self) -> None:
        self.page.reload(wait_until="networkidle")

    def go_back(self) -> None:
        self.page.go_back(wait_until="networkidle")

    def go_forward(self) -> None:
        self.page.go_forward(wait_until="networkidle")
