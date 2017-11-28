import django_filters

from twitter.models import Tweet


class TweetFilter(django_filters.FilterSet):
    user_name = django_filters.CharFilter(name='user__screen_name')
    date = django_filters.DateFilter(name='created_at', lookup_expr='date')

    class Meta:
        model = Tweet
        fields = ['id', 'twitter_id', 'user', 'user_name', 'date']
