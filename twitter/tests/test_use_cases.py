from unittest.mock import patch

from django.test import TestCase

from twitter.models import TwitterUser
from twitter.tests.specs import dog_rates_response
from twitter.use_cases import FetchUserUseCase


class FetchUserUseCaseTest(TestCase):

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_success_saves_user(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 200, 'data': dog_rates_response}
        users_count = TwitterUser.objects.count()

        use_case = FetchUserUseCase()
        result = use_case.execute('dog_rates')

        params = {'params': {'screen_name': 'dog_rates'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        self.assertEqual(users_count + 1, TwitterUser.objects.count())
        self.assertEqual('Success! User added to feed.', result)

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_user_not_found_returns_expected_message(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 404, 'data': {}}

        use_case = FetchUserUseCase()
        result = use_case.execute('not_ratting_dogs')

        params = {'params': {'screen_name': 'not_ratting_dogs'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        self.assertEqual(
            'There is no Twitter user with the given username.',
            result
        )

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_any_other_error_returns_unexpected_error_message(self,
            mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 500, 'data': {}}

        use_case = FetchUserUseCase()
        result = use_case.execute('dog_rates')

        params = {'params': {'screen_name': 'dog_rates'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        message = 'Something went wrong and the user could not be added. Please try againg later or contact our support team.'
        self.assertEqual(message, result)
        message = 'Something went wrong and the user could not be added. Please try againg later or contact our support team.'
        self.assertEqual(message, result)
