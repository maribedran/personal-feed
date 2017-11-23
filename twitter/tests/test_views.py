from unittest.mock import patch

from model_mommy import mommy

from common.utils.tests import TestCaseUtils
from twitter.use_cases import NotFoundError, UnexpectedError


class AddUserViewTest(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.url = self.reverse('twitter:add_user')

    def test_invalid_post_returns_400(self):
        response = self.auth_client.post(self.url, {'a': 'b'})
        self.assertResponse400(response)

    @patch('twitter.use_cases.AddUsersLastMonthsTweetsUseCase.execute')
    @patch('twitter.use_cases.AddTwitterUserUseCase.execute')
    def test_valid_post_calls_use_cases_correctly(self, *args):
        mocked_user_uc, mocked_tweets_uc = args
        twitter_user = mommy.make('twitter.TwitterUser')
        mocked_user_uc.return_value = twitter_user

        response = self.auth_client.post(self.url, {'username': 'user'})
        self.assertResponse200(response)
        mocked_user_uc.assert_called_once_with('user')
        mocked_tweets_uc.assert_called_once_with(twitter_user)
        twitter_user.refresh_from_db()
        self.assertEqual(twitter_user.owners.first(), self.user)
        self.assertResponseContentEqual(response, 'Success! User added to feed.')

    @patch('twitter.use_cases.AddTwitterUserUseCase.execute')
    def test_view_returns_error_message_for_not_found_exception(self, mocked_user_uc):
        mocked_user_uc.side_effect = NotFoundError('Error Message')

        response = self.auth_client.post(self.url, {'username': 'user'})
        self.assertResponse400(response)
        mocked_user_uc.assert_called_once_with('user')
        self.assertResponseContentEqual(response, 'Error Message')

    @patch('twitter.use_cases.AddTwitterUserUseCase.execute')
    def test_view_returns_error_message_for_unexpected_exception(self, mocked_user_uc):
        mocked_user_uc.side_effect = UnexpectedError('Error Message')

        response = self.auth_client.post(self.url, {'username': 'user'})
        self.assertResponse500(response)
        mocked_user_uc.assert_called_once_with('user')
        self.assertResponseContentEqual(response, 'Error Message')

    @patch('twitter.use_cases.AddUsersLastMonthsTweetsUseCase.execute')
    @patch('twitter.use_cases.AddTwitterUserUseCase.execute')
    def test_view_returns_error_message_for_unexpected_exception_on_second_uc(self, *args):
        mocked_user_uc, mocked_tweets_uc = args
        twitter_user = mommy.make('twitter.TwitterUser')
        mocked_user_uc.return_value = twitter_user
        mocked_tweets_uc.side_effect = UnexpectedError('Error Message')

        response = self.auth_client.post(self.url, {'username': 'user'})
        self.assertResponse500(response)
        mocked_user_uc.assert_called_once_with('user')
        self.assertResponseContentEqual(response, 'Error Message')
        mocked_tweets_uc.assert_called_once_with('User Created!')


class TwitterUserViewSetTest(TestCaseUtils):

    def setUp(self):
        self.twitter_user = mommy.make('twitter.TwitterUser')
        self.list_url = self.reverse('twitter:users-list')
        self.retrieve_url = self.reverse('twitter:users-list')
