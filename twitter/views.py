from rest_framework.response import Response
from rest_framework.views import APIView

from twitter.serializers import TwitterUserSerializer
from twitter.use_cases import (
    FetchUsersLastMonthsTweetsUseCase, FetchUserUseCase,
    NotFoundError, UnexpectedError
)


class AddTwitterUserView(APIView):
    serializer_class = TwitterUserSerializer

    def post(self, request, *args, **kwags):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['twitter_user']
            try:
                twitter_user = FetchUserUseCase().execute(username)
                response = FetchUsersLastMonthsTweetsUseCase().execute(twitter_user)
                status = 200
            except NotFoundError as e:
                response = e.args[0]
                status = 400
            except UnexpectedError as e:
                response = e.args[0]
                status = 500
        return Response(response, status=status)
