import django_filters

from twitter.models import Tweet, TwitterUser


class TweetFilter(django_filters.FilterSet):
    user_name = django_filters.CharFilter(name='user__screen_name')
    date = django_filters.DateFilter(name='created_at', lookup_expr='date')

    class Meta:
        model = Tweet
        fields = ['id', 'twitter_id', 'user', 'user_name', 'date']


class TwitterUserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = TwitterUser
        fields = ['id', 'twitter_id', 'screen_name', 'name']
