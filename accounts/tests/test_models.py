from django.test import TestCase

from ..models import *


class AccountsUserModelTests(TestCase):
    user = User(email='test@test.com', first_name='John', last_name='Doe')

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'John')
