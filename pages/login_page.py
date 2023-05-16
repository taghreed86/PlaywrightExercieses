class Login:
    def __init__(self, page):
        self.page = page

    def get_user_name_textbox(self):
        return self.page.locator("id=email")

    def get_password_textbox(self):
        return self.page.get_by_placeholder("Password")

    def get_continue_button(self):
        return self.page.get_by_role("button", name="CONTINUE")