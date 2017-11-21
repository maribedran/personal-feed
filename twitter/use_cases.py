from datetime import date

from dateutil.relativedelta import relativedelta

from twitter.clients import StatusesUserTimelineClient, UsersLookupClient
from twitter.serializers import TweetCreateSerializer, TwitterUserCreateSerializer


class NotFoundError(Exception):
    pass


class UnexpectedError(Exception):
    pass


class FetchUserUseCase(object):

    def execute(self, twitter_username):
        params = {'params': {'screen_name': twitter_username}}
        client = UsersLookupClient()
        response = client(params)
        status = response['status']
        data = response['data']
        if status == 200:
            serializer = TwitterUserCreateSerializer(data=data[0])
            if serializer.is_valid():
                return serializer.save()
        elif status == 404:
            raise NotFoundError('There is no Twitter user with the given username.')
        raise UnexpectedError('Something went wrong and the user could not be added. Please try againg later or contact our support team.')


class FetchUsersLastMonthsTweetsUseCase(object):

    def execute(self, twitter_user):
        message = 'Something went wrong and the timeline could not be retrieved. Please try againg later or contact our support team.'
        client = StatusesUserTimelineClient()
        params = {'params': {'user_id': twitter_user.twitter_id, 'count': 200}}
        tweets = {}
        should_fetch_tweets = True
        last_month = date.today() + relativedelta(months=-1)
        in_month_range = lambda t: t['created_at'].date() >= last_month
        while should_fetch_tweets:
            response = client(params)
            status = response['status']
            data = response['data']
            if status == 200:
                for tweet in data:
                    if in_month_range(tweet):
                        tweet['user'] = twitter_user.id
                        tweets[tweet['id']] = tweet
                earlyest_tweet = data[-1]
                should_fetch_tweets = (
                    len(data) == 200 and in_month_range(earlyest_tweet))
                params['params']['max_id'] = earlyest_tweet['id']
            else:
                should_fetch_tweets = False
        serializer = TweetCreateSerializer(data=list(tweets.values()), many=True)
        if serializer.is_valid() and tweets:
            serializer.save()
            message = "Success! User's timeline saved to database."
        return message
