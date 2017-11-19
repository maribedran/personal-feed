from django.test import TestCase
from django.conf import settings

from twitter.use_cases import FetchTweetsUseCase


class FetchTweetsUseCaseTest(TestCase):

    def test_use_case_instantiates_tapioca_twitter_with_correct_parameters(self):
        api_params = {
            'api_key': settings.TWITTER_KEY,
            'api_secret': settings.TWITTER_SECRET_KEY,
            'access_token': settings.TWITTER_TOKEN,
            'access_token_secret': settings.TWITTER_SECRET_TOKEN,
        }

        use_case = FetchTweetsUseCase()

        self.assertEqual(use_case.twitter._api_params, api_params)
