from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_load_state("networkidle")
    page.set_default_timeout(10000)
    # page.pause()
    page.goto("https://demo-01.wge.dev.weave.works/sign_in")
    # page.get_by_placeholder("Username").click()
    # page.get_by_placeholder("Username").fill("wego-admin")
    # playwright.selectors.set_test_id_attribute("id")
    # page.get_by_test_id("email").click()
    page.locator("id=email").click()
    page.locator("id=email").fill("wego-admin")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(">ch2yU5@]F8U6IZkX?Q#")
    page.get_by_role("button", name="CONTINUE").click()

    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/clusters/list")

    page.get_by_role("link", name="Policies").click()
    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/policies")
    page.get_by_role("link", name="Containers Minimum Replica Count").click()

    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/policies/details?clusterName=management&id=weave.policies.containers-minimum-replica-count")

    page.get_by_role("link", name="Applications").click()

    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/applications")

    page.get_by_role("link", name="canaries").click()

    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/kustomization/details?clusterName=management&name=canaries&namespace=flux-system")

    page.get_by_role("tab", name="Yaml").click()
    page.get_by_role("tab", name="Violations").click()
    # page.pause()
    page.get_by_role("link", name="Containers Minimum Replica Count in deployment podinfo (1 occurrences)").nth(0).click()
    expect(page).to_have_url("https://demo-01.wge.dev.weave.works/violations/details?clusterName=management&id=993b4386-b012-4b3f-8b93-0745484686d6&source=applications&sourcePath=kustomization")
    expect(page.locator("text=Containers Minimum Replica Count in deployment podinfo (1 occurrences)")).to_be_visible()

    page.get_by_role("link", name="Containers Minimum Replica Count").click()
    expect(page.locator("text=weave.policies.containers-minimum-replica-count")).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
