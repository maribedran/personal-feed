from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from twitter.models import Tweet, TwitterUser
from twitter.serializers import TweetSerializer, TwitterUserSerializer, UsernameSerializer
from twitter.use_cases import (
    AddTwitterUserUseCase, AddUsersLastMonthsTweetsUseCase, NotFoundError, UnexpectedError
)


class AddTwitterUserView(APIView):
    serializer_class = UsernameSerializer

    def associate_users(self, twitter_user, current_user):
        twitter_user.owners.add(current_user)

    def post(self, request, *args, **kwags):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            twitter_user = TwitterUser.objects.filter(screen_name=username).first()
            if not twitter_user:
                try:
                    twitter_user = AddTwitterUserUseCase().execute(username)
                    AddUsersLastMonthsTweetsUseCase().execute(twitter_user)
                except NotFoundError as e:
                    response = e.args[0]
                    status = 400
                except UnexpectedError as e:
                    response = e.args[0]
                    status = 500
            if twitter_user:
                status = 200
                response = 'Success! User added to feed.'
                self.associate_users(twitter_user, request.user)
        return Response(response, status=status)


class TwitterUserReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = TwitterUserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('twitter_id', 'screen_name',)
    ordering = ('twitter_id',)

    def get_queryset(self):
        return TwitterUser.objects.filter(owners=self.request.user)


class TweetReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = TweetSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('twitter_id',)
    ordering = ('twitter_id',)

    def get_queryset(self):
        return Tweet.objects.select_related('user').filter(user__owners=self.request.user)
