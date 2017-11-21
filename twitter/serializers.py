from rest_framework import serializers

from twitter.models import Tweet, TwitterUser


class TwitterUserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TwitterUser
        fields = ('id', 'twitter_id', 'screen_name', 'name',)
        read_only_fields = ('twitter_id',)

    def validate(self, data):
        data['twitter_id'] = data.pop('id')
        return data


class TweetCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'twitter_id', 'user', 'text', 'created_at',)
        read_only_fields = ('twitter_id',)

    def validate(self, data):
        data['twitter_id'] = data.pop('id')
        return data


class TwitterUserSerializer(serializers.Serializer):
    twitter_user = serializers.CharField()
