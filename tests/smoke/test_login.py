import pytest
import json
from pathlib import Path
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(scope="module")
def test_users():
    users_path = Path(__file__).parent.parent.parent / "data" / "users.json"
    with open(users_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.smoke
@pytest.mark.P0
class TestLoginSmoke:
    def test_login_success(self, page, base_url, test_users):
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.goto(base_url)
        assert login_page.is_login_form_visible(), "Login form should be visible"

        login_page.login(
            test_users["valid"]["username"],
            test_users["valid"]["password"]
        )

        assert dashboard_page.is_title_visible(), "Dashboard should be visible after login"
        assert dashboard_page.is_logged_in(), "User should be logged in"

    def test_login_page_elements(self, page, base_url):
        login_page = LoginPage(page)
        login_page.goto(base_url)

        assert login_page.is_visible(login_page.username_input), "Username input should be visible"
        assert login_page.is_visible(login_page.password_input), "Password input should be visible"
        assert login_page.is_visible(login_page.login_button), "Login button should be visible"
        assert login_page.is_visible(login_page.logo), "Logo should be visible"

    def test_login_button_state(self, page, base_url):
        login_page = LoginPage(page)
        login_page.goto(base_url)

        assert login_page.is_login_button_enabled(), "Login button should be enabled initially"


@pytest.mark.regression
@pytest.mark.P1
class TestLoginRegression:
    def test_login_failed_with_invalid_password(self, page, base_url, test_users):
        login_page = LoginPage(page)
        login_page.goto(base_url)

        login_page.login(
            test_users["invalid_password"]["username"],
            test_users["invalid_password"]["password"]
        )

        error_msg = login_page.get_error_message()
        assert "Invalid credentials" in error_msg, f"Expected error message about invalid credentials, got: {error_msg}"

    def test_login_failed_with_nonexistent_user(self, page, base_url, test_users):
        login_page = LoginPage(page)
        login_page.goto(base_url)

        login_page.login(
            test_users["invalid_username"]["username"],
            test_users["invalid_username"]["password"]
        )

        error_msg = login_page.get_error_message()
        assert "Invalid credentials" in error_msg, f"Expected error message about invalid credentials, got: {error_msg}"

    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "Test123456", "Username is required"),
        ("testuser@example.com", "", "Password is required"),
    ])
    def test_login_empty_fields(self, page, base_url, username, password, expected_error):
        login_page = LoginPage(page)
        login_page.goto(base_url)

        login_page.login(username, password)

        error_msg = login_page.get_error_message()
        assert expected_error in error_msg, f"Expected '{expected_error}' in error message, got: {error_msg}"


@pytest.mark.regression
@pytest.mark.P2
class TestDashboardRegression:
    def test_dashboard_elements_visible(self, page, base_url, test_users):
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.goto(base_url)
        login_page.login(
            test_users["valid"]["username"],
            test_users["valid"]["password"]
        )

        assert dashboard_page.is_title_visible(), "Dashboard title should be visible"
        assert dashboard_page.is_logged_in(), "Welcome message should be visible"

    def test_logout(self, page, base_url, test_users):
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.goto(base_url)
        login_page.login(
            test_users["valid"]["username"],
            test_users["valid"]["password"]
        )

        dashboard_page.click_logout()

        assert login_page.is_login_form_visible(), "Login form should be visible after logout"
