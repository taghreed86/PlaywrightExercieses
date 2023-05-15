class Applications:
    def __init__(self, page):
        self.page = page

    def open_application_page(self):
        self.page.get_by_role("link", name="Applications").click()

    def open_application_details_page(self):
        self.page.get_by_role("link", name="canaries").click()

    def open_application_yaml_tab(self):
        self.page.get_by_role("tab", name="Yaml").click()

    def open_application_violations_tab(self):
        self.page.get_by_role("tab", name="Violations").click()

    def open_application_violations_details(self):
        self.page.get_by_role("link", name="Containers Minimum Replica Count in deployment podinfo (1 occurrences)").nth(0).click()

    def open_policy_details_from_application_violations_details_page(self):
        self.page.get_by_role("link", name="Containers Minimum Replica Count").click()