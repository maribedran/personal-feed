from unittest.mock import patch

from model_mommy import mommy

from common.utils.tests import TestCaseUtils
from twitter.models import Tweet, TwitterUser
from twitter.use_cases import NotFoundError, UnexpectedError
from twitter.serializers import TweetSerializer, TwitterUserSerializer


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
        super().setUp()
        self.twitter_user = mommy.make('twitter.TwitterUser')
        self.twitter_user.owners.add(self.user)
        self.list_url = self.reverse('twitter:users-list')
        self.detail_url = self.reverse('twitter:users-detail', self.twitter_user.id)

    def test_list_returns_status_code_200(self):
        response = self.auth_client.get(self.list_url)
        self.assertResponse200(response)

    def test_list_returns_correct_data(self):
        data = TwitterUserSerializer(self.twitter_user).data
        response = self.auth_client.get(self.list_url)
        self.assertEqual(1, response.json()['count'])
        self.assertEqual([data], response.json()['results'])

    def test_list_filters_by_logged_user(self):
        twitter_user = mommy.make('twitter.TwitterUser')

        response = self.auth_client.get(self.list_url)
        count = TwitterUser.objects.filter(owners=self.user).count()
        self.assertEqual(count, response.json()['count'])

        twitter_user.owners.add(self.user)

        response = self.auth_client.get(self.list_url)
        self.assertEqual(count + 1, response.json()['count'])

    def test_detail_returns_status_code_200(self):
        response = self.auth_client.get(self.detail_url)
        self.assertResponse200(response)

    def test_detail_returns_correct_data(self):
        data = TwitterUserSerializer(self.twitter_user).data
        response = self.auth_client.get(self.detail_url)
        self.assertEqual(data, response.json())

    def test_detail_returns_404_if_user_is_not_owner(self):
        twitter_user = mommy.make('twitter.TwitterUser')
        detail_url = self.reverse('twitter:users-detail', twitter_user.id)
        response = self.auth_client.get(detail_url)
        self.assertResponse404(response)


class TweetViewSetTest(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.twitter_user = mommy.make('twitter.TwitterUser')
        self.twitter_user.owners.add(self.user)
        self.tweet = mommy.make('twitter.Tweet', user=self.twitter_user)
        self.list_url = self.reverse('twitter:tweets-list')
        self.detail_url = self.reverse('twitter:tweets-detail', self.tweet.id)

    def test_list_returns_status_code_200(self):
        response = self.auth_client.get(self.list_url)
        self.assertResponse200(response)

    def test_list_returns_correct_data(self):
        data = TweetSerializer(self.tweet).data
        response = self.auth_client.get(self.list_url)
        self.assertEqual(1, response.json()['count'])
        self.assertEqual([data], response.json()['results'])

    def test_list_filters_by_logged_user(self):
        tweet = mommy.make('twitter.Tweet')

        response = self.auth_client.get(self.list_url)
        count = Tweet.objects.filter(user__owners=self.user).count()
        self.assertEqual(count, response.json()['count'])

        tweet.user.owners.add(self.user)

        response = self.auth_client.get(self.list_url)
        self.assertEqual(count + 1, response.json()['count'])

    def test_detail_returns_status_code_200(self):
        response = self.auth_client.get(self.detail_url)
        self.assertResponse200(response)

    def test_detail_returns_correct_data(self):
        data = TweetSerializer(self.tweet).data
        response = self.auth_client.get(self.detail_url)
        self.assertEqual(data, response.json())

    def test_detail_returns_404_if_user_is_not_owner(self):
        tweet = mommy.make('twitter.Tweet')
        detail_url = self.reverse('twitter:tweets-detail', tweet.id)
        response = self.auth_client.get(detail_url)
        self.assertResponse404(response)
