from django.test import TestCase

from ..forms import *


# Set up default, valid form data
form_data = {
    'email': 'test@test.com',
    'first_name': 'Test',
    'last_name': 'Account',
    'password1': ';alskdjf',
    'password2': ';alskdjf',
}


class AccountsUserCreationFormTests(TestCase):
    def test_valid_form_data(self):
        """
        Valid forms successfully validate
        """
        user_form = UserCreationForm(data=form_data)
        self.assertTrue(user_form.is_valid())

    def test_missing_form_data(self):
        """
        Form with no data does not validate
        """
        user_form = UserCreationForm(data={})
        self.assertFalse(user_form.is_valid())

    def test_email_without_tld(self):
        """
        Email without TLD correctly identified as invalid
        """
        invalid_form_data = form_data.copy()
        invalid_form_data['email'] = 'invalidemail@bad'
        form = UserCreationForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

    def test_email_with_bad_chars(self):
        """
        Email with invalid characters correctly identified as invalid
        """
        invalid_form_data = form_data.copy()
        invalid_form_data['email'] = '$&%()#@test.com'
        form = UserCreationForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

    def test_email_without_at_symbol(self):
        """
        Email without @ symbol correctly identified as invalid
        """
        invalid_form_data = form_data.copy()
        invalid_form_data['email'] = 'emailtest.com'
        form = UserCreationForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

    def test_mismatching_passwords(self):
        """
        Mismatching passwords correctly identified as invalid
        """
        invalid_form_data = form_data.copy()
        invalid_form_data['password1'] = 'dfwew323r23g'
        invalid_form_data['password2'] = 'fgsdfhgraqt4e5'
        form = UserCreationForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())


class AccountsEmailChangeFormTests(TestCase):
    def test_valid_email(self):
        valid_form_data = {
            'requested_email': 'newemail@valid.com'
        }
        form = EmailChangeForm(data=valid_form_data)
        self.assertTrue(form.is_valid())

    def test_same_email(self):
        user = User.objects.create(email="test@test.com", first_name="John", last_name="Doe")
        invalid_form_data = {
            'requested_email': 'test@test.com'
        }
        form = EmailChangeForm(instance=user, data=invalid_form_data)
        self.assertFalse(form.is_valid())

    def test_existing_email(self):
        user = User.objects.create(email="test1@test.com", first_name="John", last_name="Doe")
        User.objects.create(email="test2@test.com", first_name="John", last_name="Doe")
        invalid_form_data = {
            'requested_email': 'test2@test.com'
        }
        form = EmailChangeForm(instance=user, data=invalid_form_data)
        self.assertFalse(form.is_valid())
