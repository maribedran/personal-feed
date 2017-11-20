from twitter.clients import UsersLookupClient
from twitter.serializers import TwitterUserCreateSerializer


class FetchUserUseCase(object):

    def execute(self, twitter_username):
        message = 'Something went wrong and the user could not be added. Please try againg later or contact our support team.'
        params = {'params': {'screen_name': twitter_username}}
        client = UsersLookupClient()
        response = client(params)
        status = response['status']
        data = response['data']
        if status == 200:
            serializer = TwitterUserCreateSerializer(data=data[0])
            if serializer.is_valid():
                serializer.save()
                message = 'Success! User added to feed.'
        elif status == 404:
            message = 'There is no Twitter user with the given username.'
        return message
