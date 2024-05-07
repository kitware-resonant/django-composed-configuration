from allauth.account.forms import LoginForm


class LoginOverrideForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = None
