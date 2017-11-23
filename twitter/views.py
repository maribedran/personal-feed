from rest_framework.response import Response
from rest_framework.views import APIView

from twitter.models import Tweet, TwitterUser
from twitter.serializers import UsernameSerializer, TweetGetSerializer, TwitterUserGetSerializer
from twitter.use_cases import (
    AddUsersLastMonthsTweetsUseCase, AddTwitterUserUseCase,
    NotFoundError, UnexpectedError
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
