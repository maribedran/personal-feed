import json

from django.test import TestCase

import responses

from tapioca_twitter import Twitter

from twitter.clients import UsersLookupClient
from twitter.tests.specs import dog_rates_response


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
        response = UsersLookupClient(action_params=params)()
        expected = {'status': 200, 'data': dog_rates_response}
        self.assertEqual(expected, response)

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
        response = UsersLookupClient(action_params=params)()
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
