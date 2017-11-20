import json

from tapioca.exceptions import ClientError, ServerError


class PackingImproperlyConfigured(Exception):
    pass


class TapiocaPacking(object):
    tapioca_wrapper = None
    auth_params = None
    logging_class = None
    resource = None
    action = None

    def __init__(self, resource_params=None, action_params=None):
        self._check_config()
        self.api = self.tapioca_wrapper(**self.auth_params)
        self.resource_params = resource_params or {}
        self.action_params = action_params or {}

    def __call__(self):
        resource = getattr(self.api, self.resource)(**self.resource_params)
        action = getattr(resource, self.action)
        try:
            return {'status': 200, 'data': action(**self.action_params)._data}
        except (ClientError, ServerError) as e:
            return self.handle_error(e)

    def handle_error(self, error):
        status = error.status_code
        message = error.client._data
        if self.logging_class:
            self.logging_class.objects.create(
                status=status,
                error=json.dumps(message),
                resource=self.resource,
                action=self.action,
                resouce_params=json.dumps(self.resource_params),
                action_params=json.dumps(self.action_params)
            )
        return {'status': status, 'data': message}

    def _check_config(self):
        if not all([self.tapioca_wrapper, self.auth_params,
                    self.resource, self.action]):
            raise PackingImproperlyConfigured(
                '''
                   A packing must define:
                   tapioca_wrapper => a TapiocaClient class
                    ex.: tapioca_twitter.Twitter
                   auth_params => api's authentication parameters
                    ex.: {'api_key': 'my key', 'api_secret': 'my secret'}
                   resource => name of the api's resource
                    ex.: 'search_tweets'
                   action => http verb to be called
                    ex.: 'get'
                '''
            )
