from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from twitter.models import Tweet, TwitterUser
from twitter.serializers import TweetCreateSerializer, TweetGetSerializer, TwitterUserSerializer


class TwitterUserCreateSerializerTest(TestCase):

    def test_serializer_creates_instance(self):
        data = {
            'twitter_id': 1234567890,
            'screen_name': 'twitter_username',
            'name': 'Twitter Name',
            'description': 'Account Description',
        }
        serializer = TwitterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, TwitterUser)

    def test_serializer_returns_correct_data(self):
        data = {
            'twitter_id': 1234567890,
            'screen_name': 'twitter_username',
            'name': 'Twitter Name',
            'description': 'Account Description',
        }
        twitter_user = mommy.make('twitter.TwitterUser', **data)
        serializer = TwitterUserSerializer(instance=twitter_user)
        self.assertEqual(data, serializer.data)


class TweetCreateSerializerTest(TestCase):

    def setUp(self):
        self.serializer = TweetCreateSerializer

    def test_serializer_creates_instance(self):
        now = timezone.now()
        user = mommy.make(TwitterUser)
        data = {
            'twitter_id': 1234567890,
            'user': user.id,
            'text': 'My awesome tweet',
            'created_at': now.isoformat(),
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, Tweet)

    def test_serializer_returns_correct_data(self):
        now = timezone.now()
        user = mommy.make(TwitterUser)
        data = {
            'twitter_id': 1234567890,
            'user': user,
            'text': 'My awesome tweet',
            'created_at': now.isoformat(),
            'tags': ['tag', 'tag2'],
        }
        tweet = mommy.make('twitter.Tweet', **data)
        serializer = self.serializer(instance=tweet)
        data.update({'user': user.id})
        self.assertEqual(data, serializer.data)


class TweetGetSerializerTest(TestCase):

    def setUp(self):
        self.serializer = TweetGetSerializer

    def test_serializer_returns_correct_data(self):
        now = timezone.now()
        user = mommy.make(TwitterUser)
        data = {
            'twitter_id': 1234567890,
            'user': user,
            'text': 'My awesome tweet',
            'created_at': now.isoformat(),
            'tags': ['tag', 'tag2'],
        }
        tweet = mommy.make('twitter.Tweet', **data)
        serializer = self.serializer(instance=tweet)
        data.update({'user': TwitterUserSerializer(instance=user).data})
        self.assertEqual(data, serializer.data)
