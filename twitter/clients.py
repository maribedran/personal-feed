from django.conf import settings

from dateutil.parser import parse
from tapioca_twitter import Twitter

from common.utils.tapioca_packing import TapiocaPacking


AUTH_PARAMS = {
    'api_key': settings.TWITTER_KEY,
    'api_secret': settings.TWITTER_SECRET_KEY,
    'access_token': settings.TWITTER_TOKEN,
    'access_token_secret': settings.TWITTER_SECRET_TOKEN
}


class UsersLookupClient(TapiocaPacking):
    tapioca_wrapper = Twitter
    auth_params = AUTH_PARAMS
    resource = 'users_lookup'
    action = 'get'

    def serialize_data(self, data):
        user = data[0]
        user['twitter_id'] = user.pop('id')
        return user


class StatusesUserTimelineClient(TapiocaPacking):
    tapioca_wrapper = Twitter
    auth_params = AUTH_PARAMS
    resource = 'statuses_user_timeline'
    action = 'get'

    def serialize_data(self, data):
        for tweet in data:
            tweet['created_at'] = parse(tweet['created_at'])
            tweet['twitter_id'] = tweet.pop('id')
        return data
