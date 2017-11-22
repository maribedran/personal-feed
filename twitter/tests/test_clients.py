import json

from django.test import TestCase

import responses
from dateutil.parser import parse
from tapioca_twitter import Twitter

from twitter.clients import StatusesUserTimelineClient, UsersLookupClient
from twitter.tests.specs import dog_rates_response, dog_rates_tweet


class UsersLookupClientTest(TestCase):

    def setUp(self):
        twitter_api = Twitter()
        self.api_url = twitter_api.users_lookup().data

    @responses.activate
    def test_success(self):
        responses.add(
            responses.GET,
            self.api_url,
            body=json.dumps(dog_rates_response),
            content_type="application/json"
        )
        params = {'params': {'screen_name': 'dog_rates'}}
        response = UsersLookupClient()(params)
        user = dog_rates_response[0].copy()
        user.update({'twitter_id': user.pop('id')})
        self.assertEqual({'status': 200, 'data': user}, response)

    @responses.activate
    def test_not_found(self):
        not_found = {'error': [
            {'code': 17, 'message': 'No user matches for specified terms.'}]}
        responses.add(
            responses.GET,
            self.api_url,
            status=404,
            body=json.dumps(not_found),
            content_type="application/json"
        )
        params = {'params': {'screen_name': 'not_ratting_dog'}}
        response = UsersLookupClient()(params)
        expected = {'status': 404, 'data': not_found}
        self.assertEqual(expected, response)

    @responses.activate
    def test_server_error(self):
        responses.add(
            responses.GET,
            self.api_url,
            status=500,
            content_type="application/json"
        )
        response = UsersLookupClient()()
        expected = {'status': 500, 'data': None}
        self.assertEqual(expected, response)


class StatusesUserTimelineClientTest(TestCase):

    def setUp(self):
        twitter_api = Twitter()
        self.api_url = twitter_api.statuses_user_timeline().data

    @responses.activate
    def test_success(self):
        responses.add(
            responses.GET,
            self.api_url,
            body=json.dumps([dog_rates_tweet]),
            content_type="application/json"
        )
        params = {'params': {'screen_name': 'dog_rates', 'count': 1}}
        response = StatusesUserTimelineClient()(params)
        tweet = dog_rates_tweet.copy()
        tweet.update({'created_at': parse(tweet['created_at']), 'twitter_id': tweet.pop('id')})
        expected = {'status': 200, 'data': [tweet]}
        self.assertEqual(expected, response)

    @responses.activate
    def test_not_found(self):
        not_found = {'errors': [{
            'code': 34,
            'message': 'Sorry, that page does not exist.'}
        ]}
        responses.add(
            responses.GET,
            self.api_url,
            status=404,
            body=json.dumps(not_found),
            content_type="application/json"
        )
        params = {'params': {'screen_name': 'not_ratting_dog', 'count': 1}}
        response = StatusesUserTimelineClient()(params)
        expected = {'status': 404, 'data': not_found}
        self.assertEqual(expected, response)

    @responses.activate
    def test_server_error(self):
        responses.add(
            responses.GET,
            self.api_url,
            status=500,
            content_type="application/json"
        )
        response = StatusesUserTimelineClient()()
        expected = {'status': 500, 'data': None}
        self.assertEqual(expected, response)
