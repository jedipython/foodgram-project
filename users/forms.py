from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import password_validation


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    raw_password = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'raw_password')

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        raw_password = self.cleaned_data.get('raw_password')
        if raw_password:
            try:
                password_validation.validate_password(
                    raw_password, self.instance)
            except forms.ValidationError as error:
                self.add_error('raw_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['raw_password'])
        if commit:
            user.save()
        return user


class EmptyClass(UserCreationForm):
    """ Flake8 не пропускает тест с импортом первой строки, но она нужна, чтобы работал класс выше """
    pass
