from playwright.sync_api import Page, Locator, expect
from typing import Any, Optional


class CustomAssertions:
    @staticmethod
    def assert_element_visible(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_visible()

    @staticmethod
    def assert_element_hidden(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        expect(locator).to_be_hidden()

    @staticmethod
    def assert_element_text(page: Page, selector: str, expected_text: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_have_text(expected_text)

    @staticmethod
    def assert_element_contains_text(page: Page, selector: str, expected_text: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_contain_text(expected_text)

    @staticmethod
    def assert_url_contains(page: Page, text: str) -> None:
        expect(page).to_have_url(f".*{text}.*")

    @staticmethod
    def assert_title_contains(page: Page, text: str) -> None:
        expect(page).to_have_title(f".*{text}.*")

    @staticmethod
    def assert_input_value(page: Page, selector: str, expected_value: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_have_value(expected_value)

    @staticmethod
    def assert_element_enabled(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_enabled()

    @staticmethod
    def assert_element_disabled(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        expect(locator).to_be_disabled()

    @staticmethod
    def assert_element_checked(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        expect(locator).to_be_checked()

    @staticmethod
    def assert_element_not_checked(page: Page, selector: str, timeout: int = 30000) -> None:
        locator = page.locator(selector)
        expect(locator).not_to_be_checked()

    @staticmethod
    def assert_response_status(page: Page, expected_status: int) -> None:
        response = page.evaluate("""() => {
            return window.__LAST_RESPONSE_STATUS__;
        }""")
        assert response == expected_status, f"Expected status {expected_status}, got {response}"

    @staticmethod
    def assert_no_console_errors(page: Page) -> None:
        console_errors: list = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        assert len(console_errors) == 0, f"Console errors found: {console_errors}"

    @staticmethod
    def take_full_page_screenshot(page: Page, name: str) -> bytes:
        return page.screenshot(path=f"screenshots/{name}.png", full_page=True)
