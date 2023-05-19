import os

from playwright.sync_api import Playwright, sync_playwright, expect
import pytest
from pages.login_page import Login

user_name = os.environ["USER_NAME"]
password = os.environ["PASSWORD"]


@pytest.fixture(scope="session")
def setup(playwright: Playwright):
    browser = playwright.chromium.launch(slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_load_state("networkidle")
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.goto("https://demo-01.wge.dev.weave.works/sign_in")
    page.set_default_timeout(5000)

    yield page
    context.tracing.stop(path="../test-results/execution-tracing.zip")
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="class")
def login(setup):
    page = setup
    login_page = Login(page)
    login_page.get_user_name_textbox().fill(user_name)
    login_page.get_password_textbox().fill(password)
    login_page.get_continue_button().click()
    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/clusters/list")
    yield page
    login_page.get_account_settings_menu().click()
    login_page.get_logout_button().click()
