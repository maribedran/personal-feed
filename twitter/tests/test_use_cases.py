from datetime import datetime
from unittest.mock import call, patch

from django.test import TestCase

from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from twitter.clients import StatusesUserTimelineClient
from twitter.models import Tweet, TwitterUser
from twitter.tests.specs import dog_rates_response, dog_rates_tweet
from twitter.use_cases import (
    AddTwitterUserUseCase, AddUsersLastMonthsTweetsUseCase, NotFoundError, UnexpectedError
)


class AddTwitterUserUseCaseTest(TestCase):

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_success_saves_user(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        response = dog_rates_response.copy()[0]
        response['twitter_id'] = response.pop('id')
        mocked_client_call.return_value = {'status': 200, 'data': response}

        users_count = TwitterUser.objects.count()

        use_case = AddTwitterUserUseCase()
        result = use_case.execute('dog_rates')

        params = {'params': {'screen_name': 'dog_rates'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
        self.assertEqual(users_count + 1, TwitterUser.objects.count())
        self.assertIsInstance(result, TwitterUser)

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_user_not_found_returns_expected_message(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 404, 'data': {}}

        use_case = AddTwitterUserUseCase()

        self.assertRaises(NotFoundError, use_case.execute, 'not_ratting_dogs')

        params = {'params': {'screen_name': 'not_ratting_dogs'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)

    @patch('twitter.use_cases.UsersLookupClient.__call__')
    @patch('twitter.use_cases.UsersLookupClient.__init__')
    def test_any_other_error_returns_unexpected_error_message(self, *args):
        mocked_client, mocked_client_call = args
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 500, 'data': {}}

        use_case = AddTwitterUserUseCase()

        self.assertRaises(UnexpectedError, use_case.execute, 'dog_rates')
        params = {'params': {'screen_name': 'dog_rates'}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)


class AddUsersLastMonthsTweetsUseCaseTest(TestCase):

    def setUp(self):
        self.user = mommy.make(TwitterUser)
        tweet = dog_rates_tweet.copy()
        self.tweet = StatusesUserTimelineClient().serialize_data([tweet])[0]

    @patch('twitter.use_cases.StatusesUserTimelineClient.__call__')
    @patch('twitter.use_cases.StatusesUserTimelineClient.__init__')
    def test_success_saves_tweets(self, mocked_client, mocked_client_call):
        mocked_client.return_value = None
        mocked_client_call.return_value = {'status': 200, 'data': [self.tweet]}
        tweets_count = Tweet.objects.filter(user=self.user).count()

        use_case = AddUsersLastMonthsTweetsUseCase()
        result = use_case.execute(self.user)

        # The actual call doesn't have the max_id key, but the original param
        # is updated so the assert fails withou the key
        # Any thoughts?
        params = {'params': {'user_id': self.user.twitter_id, 'count': 200, 'max_id': self.tweet['twitter_id']}}
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
            {'twitter_id': i, 'text': 'Text', 'created_at': now}
            for i in range(1, 201)
        ]}
        # Last tweet from previous request is always the first
        second_response = {'status': 200, 'data': [
            {'twitter_id': 200, 'text': 'Text', 'created_at': now},
            {'twitter_id': 201, 'text': 'Text', 'created_at': two_months_before}
        ]}
        mocked_client.return_value = None
        mocked_client_call.side_effect = [first_response, second_response]
        tweets_count = Tweet.objects.filter(user=self.user).count()

        use_case = AddUsersLastMonthsTweetsUseCase()
        result = use_case.execute(self.user)

        params = {'params': {'user_id': self.user.twitter_id, 'count': 200, 'max_id': 201}}
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_has_calls([call(params), call(params)])
        self.assertEqual(tweets_count + 200, Tweet.objects.filter(user=self.user).count())
        self.assertEqual("Success! User's timeline saved to database.", result)

    @patch('twitter.use_cases.StatusesUserTimelineClient.__call__')
    @patch('twitter.use_cases.StatusesUserTimelineClient.__init__')
    def test_error_raises_unexpected_error_exception(self, *args):
        mocked_client, mocked_client_call = args
        mocked_client.return_value = None
        mocked_client_call.return_value = {
            'status': 500, 'data': {}}

        use_case = AddUsersLastMonthsTweetsUseCase()

        params = {'params': {'user_id': self.user.twitter_id, 'count': 200}}
        self.assertRaises(UnexpectedError, use_case.execute, self.user)
        mocked_client.assert_called_once_with()
        mocked_client_call.assert_called_once_with(params)
