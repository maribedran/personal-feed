from django.test import TestCase

from users.models import User


class UserTest(TestCase):

    def test_create_two_users_with_empty_email_adress(self):
        '''
            Social auth calls the create_user method with data from the users
            profile. The field comes as an empty string when no email is set.
        '''
        self.assertIsInstance(User.objects.create_user(
            username='username',
            email='',
            password='password'
        ), User)
        self.assertIsInstance(User.objects.create_user(
            username='username2',
            email='',
            password='password'
        ), User)
