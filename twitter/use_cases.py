from tapioca_twitter import Twitter
from django.conf import settings


class FetchTweetsUseCase(object):

    def __init__(self):
        self.twitter = Twitter(
            api_key=settings.TWITTER_KEY,
            api_secret=settings.TWITTER_SECRET_KEY,
            access_token=settings.TWITTER_TOKEN,
            access_token_secret=settings.TWITTER_SECRET_TOKEN,
        )
