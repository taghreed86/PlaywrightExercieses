from playwright.sync_api import Playwright, sync_playwright, expect
from pages.policies_page import Policies
from pages.application_page import Applications
from pages.login_page import Login


def test_run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    login_page = Login(page)

    page.wait_for_load_state("networkidle")
    page.set_default_timeout(10000)
    # page.pause()
    page.goto("https://demo-01.wge.dev.weave.works/sign_in")
    # page.get_by_placeholder("Username").click()
    # page.get_by_placeholder("Username").fill("wego-admin")
    # playwright.selectors.set_test_id_attribute("id")
    # page.get_by_test_id("email").click()

    login_page.get_user_name_textbox().fill("wego-admin")

    login_page.get_password_textbox().fill(">ch2yU5@]F8U6IZkX?Q#")
    login_page.get_continue_button().click()
    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/clusters/list")

    policies_page = Policies(page)
    applications_page = Applications(page)

    def test_open_policies_page():
        policies_page.open_policies_page()
        expect(page).to_have_url("https://demo-01.wge.dev.weave.works/policies")

    def test_open_policy_details_page():
        policies_page.open_policy_details_page()
        expect(page).to_have_url("https://demo-01.wge.dev.weave.works/policies/details?clusterName=management&id=weave.policies.containers-minimum-replica-count")

    def test_open_applications_page():
        applications_page.open_application_page()
        expect(page).to_have_url("https://demo-01.wge.dev.weave.works/applications")

    def test_open_application_details_page():
        applications_page.open_application_details_page()
        expect(page).to_have_url("https://demo-01.wge.dev.weave.works/kustomization/details?clusterName=management&name=canaries&namespace=flux-system")

    def test_open_application_yaml():
        applications_page.open_application_yaml_tab()
        expect(page.get_by_text("kubectl get kustomization canaries -n flux-system -o yaml")).to_be_visible()

    # page.pause()
    def test_open_application_violations_page():
        applications_page.open_application_violations_tab()
        expect(page).to_have_url("https://demo-01.wge.dev.weave.works/kustomization/violations?clusterName=management&name=canaries&namespace=flux-system")

    def test_open_application_violations_details():
        applications_page.open_application_violations_details()
        assert "https://demo-01.wge.dev.weave.works/violations/details?clusterName=management&id=" in page.url
        expect(page.locator("text=Containers Minimum Replica Count in deployment podinfo (1 occurrences)")).to_be_visible()

    def test_open_policy_details_from_app_violations_details_page():
        applications_page.open_policy_details_from_application_violations_details_page()
        expect(page.locator("text=weave.policies.containers-minimum-replica-count")).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
