import pytest
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from dotenv import load_dotenv
from data import get_config

load_dotenv()

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(Path(__file__).parent.parent / "browsers")

config = get_config()


def get_demo_url() -> str:
    if config.get_base_url().startswith("file://"):
        return config.get_base_url()
    return f"file:///e:/Trae_project/UI_Auto_demo/data"


@pytest.fixture(scope="session")
def browser() -> Browser:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=config.is_headless(),
        args=["--disable-dev-shm-usage", "--disable-popup-blocking"]
    )
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    storage_state_path = Path("auth/storage_state.json")
    if storage_state_path.exists():
        context = browser.new_context(storage_state=str(storage_state_path))
    else:
        context = browser.new_context()

    trace_dir = Path("traces")
    trace_dir.mkdir(exist_ok=True)

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    yield context
    context.tracing.stop(path=f"traces/trace-test.zip")
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    page.set_default_timeout(config.get_timeout())
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return get_demo_url()


@pytest.fixture(scope="session")
def api_url() -> str:
    return config.get_api_url()


@pytest.fixture(scope="function")
def login_page(page: Page) -> "LoginPage":
    from pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(page: Page) -> "DashboardPage":
    from pages.dashboard_page import DashboardPage
    return DashboardPage(page)


@pytest.fixture(scope="function")
def screenshot_on_failure(request, page: Page):
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        page.screenshot(path=f"screenshots/failed_{request.node.name}.png", full_page=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    logs_dir = reports_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
