from .request import TelestreamCloudRequest, TelestreamCloudException
from .resources import Flip


class TelestreamCloud():

    DEFAULT_API_HOST = 'api-gce.pandastream.com'
    DEFAULT_API_VERSION = '3.0'
    DEFAULT_API_PORT = 443
    RESOURCES = {
        'flip': Flip
    }

    def __init__(self, access_key, secret_key, factory_id=None,
                 api_host=None, api_port=None, api_version=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.factory_id = factory_id
        self.api_host = api_host or self.DEFAULT_API_HOST
        self.api_port = api_port or self.DEFAULT_API_PORT
        self.api_version = api_version or self.DEFAULT_API_VERSION

    def _credentials(self):
        required = ['access_key', 'secret_key', 'api_host',
                    'api_port', 'api_version']
        if self.factory_id is not None:
            required.append('factory_id')
        return {key: self.__dict__[key] for key in required}

    def get_resource(self, resource_name):
        if resource_name in self.RESOURCES:
            return self.RESOURCES[resource_name](self._credentials())
        raise TelestreamCloudException(
                            'Unknown resource: {}'.format(resource_name))

    def get(self, request_path, params={}):
        return TelestreamCloudRequest('GET', request_path,
                                      self._credentials(), params).send()

    def post(self, request_path, params={}):
        return TelestreamCloudRequest('POST', request_path,
                                      self._credentials(), params).send()

    def put(self, request_path, params={}):
        return TelestreamCloudRequest('PUT', request_path,
                                      self._credentials(), params).send()

    def delete(self, request_path, params={}):
        return TelestreamCloudRequest('DELETE', request_path,
                                      self._credentials(), params).send()

    def signed_params(self, verb, path, params={}, timestamp=None):
        return TelestreamCloudRequest(verb, path, self._credentials(),
                                      params, timestamp).signed_params()
