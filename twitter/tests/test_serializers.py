from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from twitter.models import TwitterUser, Tweet
from twitter.serializers import TwitterUserCreateSerializer, TweetCreateSerializer


class TwitterUserCreateSerializerTest(TestCase):

    def test_serializer_creates_instance(self):
        data = {
            'id': 1234567890,
            'screen_name': 'twitter_username',
            'name': 'Twitter Name'
        }
        serializer = TwitterUserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, TwitterUser)


class TweetCreateSerializerTest(TestCase):

    def test_serializer_creates_instance(self):
        now = timezone.now()
        user = mommy.make(TwitterUser)
        data = {
            'id': 1234567890,
            'user': user.id,
            'text': 'My awesome tweet',
            'created_at': now.isoformat()
        }
        serializer = TweetCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, Tweet)
