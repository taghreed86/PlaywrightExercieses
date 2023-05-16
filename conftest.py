from playwright.sync_api import Playwright, sync_playwright, expect
import pytest
from pages.login_page import Login


@pytest.fixture(scope="session")
def setup(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_load_state("networkidle")
    page.goto("https://demo-01.wge.dev.weave.works/sign_in")
    page.set_default_timeout(5000)

    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="class")
def login(setup):
    page = setup
    login_page = Login(page)
    login_page.get_user_name_textbox().fill("wego-admin")
    login_page.get_password_textbox().fill(">ch2yU5@]F8U6IZkX?Q#")
    login_page.get_continue_button().click()
    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/clusters/list")
    yield page
    login_page.get_account_settings_menu().click()
    login_page.get_logout_button().click()
