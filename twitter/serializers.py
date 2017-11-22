from rest_framework import serializers

from twitter.models import Tweet, TwitterUser
from users.models import User


class TwitterUserCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = TwitterUser
        fields = ('twitter_id', 'screen_name', 'name', 'description', 'owner',)

    def create(self, validated_data):
        user = validated_data.pop('owner')
        instance = super().create(validated_data)
        instance.owners.add(user)
        return instance


class TweetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('twitter_id', 'user', 'text', 'created_at',)


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
