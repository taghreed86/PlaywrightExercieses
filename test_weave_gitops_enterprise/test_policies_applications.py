from playwright.sync_api import Playwright, sync_playwright, expect
from pages.policies_page import Policies
from pages.application_page import Applications
import pytest
import os


WGE_CNAME = os.environ["MANAGEMENT_CLUSTER_CNAME"] or "localhost"
NODEPORT = os.environ["UI_NODEPORT"] or "30080"

URL = f"https://{WGE_CNAME}:{NODEPORT}"


@pytest.mark.usefixtures("login")
class TestPolicies:
    @pytest.fixture(autouse=True)
    def _obj(self, login):
        self.page = login
        self.policies_page = Policies(self.page)

    def test_open_policies_page(self):
        self.policies_page.open_policies_page()
        expect(self.page).to_have_url("https://{URL}/policies")

    def test_open_policy_details_page(self):
        self.policies_page.open_policy_details_page()
        expect(self.page).to_have_url("https://{URL}/policy_details/details?clusterName=management&id=weave.policies.containers-minimum-replica-count&name=Containers%20Minimum%20Replica%20Count")


@pytest.mark.usefixtures("login")
class TestApplications:
    @pytest.fixture(autouse=True)
    def _create_obj(self, login):
        self.page = login
        self.applications_page = Applications(self.page)

    def test_open_applications_page(self):
        self.applications_page.open_application_page()
        expect(self.page).to_have_url("https://{URL}/applications")

    def test_open_application_details_page(self):
        self.applications_page.open_application_details_page()
        expect(self.page).to_have_url("https://{URL}/kustomization/details?clusterName=management&name=canaries&namespace=flux-system")

    def test_open_application_yaml(self):
        self.applications_page.open_application_yaml_tab()
        expect(self.page .get_by_text("kubectl get kustomization canaries -n flux-system -o yaml")).to_be_visible()

    # page.pause()
    def test_open_application_violations_page(self):
        self.applications_page.open_application_violations_tab()
        expect(self.page).to_have_url("https://{URL}/kustomization/violations?clusterName=management&name=canaries&namespace=flux-system")


    def test_open_application_violations_details(self):
        self.applications_page.open_application_violations_details()
        # assert "https://{URL}/violations/details?clusterName=management&id=" in self.page .url
        assert "https://{URL}/policy_violation?clusterName=management&id=" in self.page.url
        expect(self.page .locator("text=Containers Minimum Replica Count in deployment podinfo (1 occurrences)")).to_be_visible()

    def test_open_policy_details_from_app_violations_details_page(self):
        self.applications_page.open_policy_details_from_application_violations_details_page()
        expect(self.page .locator("text=weave.policies.containers-minimum-replica-count")).to_be_visible()
