from django.contrib.auth import forms as auth_forms
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    User creation, aka registration form
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text=password_validators_help_text_html)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        # Validate password using default validators defined in settings
        validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('register', 'Register'))


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. This has all the data
    needed for django-admin
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
          )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserChangeSelfForm(forms.ModelForm):
    """
    A form for regular uses to edit their own details.
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
          )

    def __init__(self, *args, **kwargs):
        super(UserChangeSelfForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('save', 'Save'))


class EmailChangeForm(forms.ModelForm):
    """
    A form for changing one's email address
    """
    class Meta:
        model = User
        fields = {
            'requested_email',
        }

    def clean_requested_email(self):
        requested_email = self.cleaned_data.get('requested_email')
        if User.objects.filter(email=requested_email).exists():
            raise forms.ValidationError('That email is already taken')
        return requested_email

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('save', 'Save'))


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('change', 'Change'))


class PasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('reset', 'Reset'))


class SetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('save', 'Save'))


class AuthenticationForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', 'Login'))
