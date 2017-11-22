from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from twitter.models import Tweet, TwitterUser
from twitter.serializers import TweetCreateSerializer, TwitterUserCreateSerializer


class TwitterUserCreateSerializerTest(TestCase):

    def test_serializer_creates_instance(self):
        user = mommy.make('users.User')
        data = {
            'twitter_id': 1234567890,
            'screen_name': 'twitter_username',
            'name': 'Twitter Name',
            'description': 'Account Description',
            'owner': user.id
        }
        serializer = TwitterUserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, TwitterUser)
        self.assertEqual(user, serializer.instance.owners.first())


class TweetCreateSerializerTest(TestCase):

    def test_serializer_creates_instance(self):
        now = timezone.now()
        user = mommy.make(TwitterUser)
        data = {
            'twitter_id': 1234567890,
            'user': user.id,
            'text': 'My awesome tweet',
            'created_at': now.isoformat()
        }
        serializer = TweetCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertIsInstance(serializer.instance, Tweet)
