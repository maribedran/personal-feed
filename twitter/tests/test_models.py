from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from twitter.models import Tweet, TwitterUser


class TwitterUserModelTest(TestCase):

    def test_create_instance(self):
        twitter_user = TwitterUser.objects.create(
            twitter_id=1234567890987654321,
            screen_name='coolUser_name',
            name='Even Cooler Name'
        )
        self.assertEqual(1234567890987654321, twitter_user.twitter_id)
        self.assertEqual('coolUser_name', twitter_user.screen_name)
        self.assertEqual('Even Cooler Name', twitter_user.name)

    def test_add_owner(self):
        user = mommy.make('users.User')
        twitter_user = mommy.make('twitter.TwitterUser')
        twitter_user.owners.add(user)
        self.assertEqual(user, twitter_user.owners.first())

    def test_str_returns_screen_name(self):
        twitter_user = mommy.make('twitter.TwitterUser', screen_name='some_name')
        self.assertEqual('some_name', str(twitter_user))


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

    def test_str_returns_truncated_text(self):
        tweet = mommy.make('twitter.Tweet', text='A' * 100)
        self.assertEqual('%s...' % ('A' * 67), str(tweet))
