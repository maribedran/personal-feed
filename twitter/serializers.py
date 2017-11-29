from rest_framework import serializers

from twitter.models import Tweet, TwitterUser


class TwitterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TwitterUser
        fields = ('twitter_id', 'screen_name', 'name', 'description',)


class TweetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('twitter_id', 'user', 'text', 'created_at', 'tags',)


class TweetGetSerializer(serializers.ModelSerializer):
    user = TwitterUserSerializer()

    class Meta:
        model = Tweet
        fields = ('twitter_id', 'user', 'text', 'created_at', 'tags',)


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
