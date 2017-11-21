from datetime import datetime
from unittest.mock import call, patch

from django.test import TestCase

from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from twitter.models import Tweet, TwitterUser
from twitter.tests.specs import dog_rates_response, dog_rates_tweet
from twitter.use_cases import FetchUsersLastMonthsTweetsUseCase, FetchUserUseCase


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
    def test_any_other_error_returns_unexpected_error_message(self, *args):
        mocked_client, mocked_client_call = args
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


class FetchUsersLastMonthsTweetsUseCaseTest(TestCase):

    def setUp(self):
        self.user = mommy.make(TwitterUser)
        tweet = dog_rates_tweet.copy()
        tweet['created_at'] = datetime.now()
        self.tweet = tweet

    @patch('twitter.use_cases.StatusesUserTimelineClient.__call__')
    @patch('twitter.use_cases.StatusesUserTimelineClient.__init__')
    def test_success_saves_tweets(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 200, 'data': [self.tweet]}
        tweets_count = Tweet.objects.filter(user=self.user).count()

        use_case = FetchUsersLastMonthsTweetsUseCase()
        result = use_case.execute(self.user)

        # The actual call doesn't have the max_id key, but the original param
        # is updated so the assert fails withou the key
        # Any thoughts?
        params = {'params': {'user_id': self.user.twitter_id, 'count': 200, 'max_id': self.tweet['id']}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        self.assertEqual(tweets_count + 1, Tweet.objects.filter(user=self.user).count())
        self.assertEqual("Success! User's timeline saved to database.", result)

    @patch('twitter.use_cases.StatusesUserTimelineClient.__call__')
    @patch('twitter.use_cases.StatusesUserTimelineClient.__init__')
    def test_fetch_all_tweets_in_month_range_if_more_than_200(self, *args):
        mocked_client, mocked_client_call = args
        now = datetime.now()
        two_months_before = now + relativedelta(months=-2)
        first_response = {'status': 200, 'data': [
            {'id': i, 'text': 'Text', 'created_at': now}
            for i in range(1, 201)
        ]}
        # Last tweet from previous request is always the first
        second_response = {'status': 200, 'data': [
            {'id': 200, 'text': 'Text', 'created_at': now},
            {'id': 201, 'text': 'Text', 'created_at': two_months_before}
        ]}
        mocked_client.return_value = None
        mocked_client_call.side_effect = [first_response, second_response]
        tweets_count = Tweet.objects.filter(user=self.user).count()

        use_case = FetchUsersLastMonthsTweetsUseCase()
        result = use_case.execute(self.user)

        params = {'params': {'user_id': self.user.twitter_id, 'count': 200, 'max_id': 201}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_has_calls([call(params), call(params)])
        self.assertEqual(tweets_count + 200, Tweet.objects.filter(user=self.user).count())
        self.assertEqual("Success! User's timeline saved to database.", result)

    @patch('twitter.use_cases.StatusesUserTimelineClient.__call__')
    @patch('twitter.use_cases.StatusesUserTimelineClient.__init__')
    def test_error_returns_unexpected_error_message(self, *args):
        mocked_client, mocked_client_call = args
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 500, 'data': {}}

        use_case = FetchUsersLastMonthsTweetsUseCase()
        result = use_case.execute(self.user)

        params = {'params': {'user_id': self.user.twitter_id, 'count': 200}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        message = 'Something went wrong and the timeline could not be retrieved. Please try againg later or contact our support team.'
        self.assertEqual(message, result)
