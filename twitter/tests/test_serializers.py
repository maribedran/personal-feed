from django.test import TestCase

from twitter.models import TwitterUser
from twitter.serializers import TwitterUserCreateSerializer


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
