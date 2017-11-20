from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from twitter.models import Tweet, TwitterUser


class TwitterUserModelTest(TestCase):

    def test_create_instance(self):
        user = TwitterUser.objects.create(
            twitter_id=1234567890987654321,
            screen_name='coolUser_name',
            name='Even Cooler Name'
        )
        self.assertEqual(1234567890987654321, user.twitter_id)
        self.assertEqual('coolUser_name', user.screen_name)
        self.assertEqual('Even Cooler Name', user.name)


class TweetModelTest(TestCase):

    def test_create_instance(self):
        user = mommy.make(TwitterUser)
        now = timezone.now()
        tweet = Tweet.objects.create(
            twitter_id=1234567890,
            user=user,
            text='Awesome Tweet',
            created_at=now
        )
        self.assertEqual(1234567890, tweet.twitter_id)
        self.assertEqual(user, tweet.user)
        self.assertEqual('Awesome Tweet', tweet.text)
        self.assertEqual(now, tweet.created_at)

    def test_deleting_user_deletes_tweet(self):
        user = mommy.make(TwitterUser)
        tweet = mommy.make(Tweet, user=user)
        TwitterUser.objects.filter(id=user.id).delete()
        self.assertRaises(Tweet.DoesNotExist, Tweet.objects.get, id=tweet.id)
