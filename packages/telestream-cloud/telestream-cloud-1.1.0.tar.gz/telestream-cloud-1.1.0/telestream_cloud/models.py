from .request import TelestreamCloudRequest, TelestreamCloudException
from .upload_session import UploadSession


class ModelAPI(object):

    def __init__(self, credentials, model_type, path_prefix=None):
        self.credentials = credentials
        self.model_type = model_type
        self.path = model_type.model_path
        self.path_prefix = path_prefix

    def __str__(self):
        return 'ModelAPI: {}'.format(self.model_type.__name__)

    def all(self, **kwargs):
        request_path = '{}.json'.format(self.model_type.model_path)
        if self.path_prefix is not None:
            request_path = self.path_prefix + request_path
        response = TelestreamCloudRequest('GET', request_path,
                                          self.credentials, data=kwargs).send()
        return [self.model_type(self.credentials, x) for x in response.json()]

    def find(self, object_id):
        request_path = '{}/{}.json'.format(self.model_type.model_path,
                                           object_id)
        response = TelestreamCloudRequest('GET', request_path,
                                          self.credentials, data={}).send()
        return self.model_type(self.credentials, response.json())

    def create(self, **kwargs):
        request_path = '{}.json'.format(self.model_type.model_path)
        response = TelestreamCloudRequest('POST', request_path,
                                          self.credentials, data=kwargs).send()
        return self.model_type(self.credentials, response.json())

    def delete(self, object_id=None):
        object_id = object_id or self.id
        request_path = '{}/{}.json'.format(self.model_type.model_path, object_id)
        resp = TelestreamCloudRequest('DELETE', request_path,
                                      self.credentials, data={}).send()
        return resp.json()


class UpdatableMixin(object):

    def __setattr__(self, *args, **kwargs):
        return object.__setattr__(self, *args, **kwargs)

    def save(self):
        updated_values = {}

        for key in self.details:
            if self.details[key] != getattr(self, key):
                updated_values[key] = getattr(self, key)

        path = '{}/{}.json'.format(self.model_path, self.id)
        response = TelestreamCloudRequest('PUT', path, self.credentials,
                                          data=updated_values).send()
        return response.json()


class TelestreamCloudModel(object):

    def __init__(self, credentials, object_dict={}):
        object.__setattr__(self, 'details', object_dict)
        object.__setattr__(self, 'credentials', credentials.copy())
        self._set_object_attributes(self.details)

    def __str__(self):
        return '{} {}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, *args, **kwargs):
        n = self.__class__.__name__
        raise TelestreamCloudException('{} objects are immutable'.format(n))

    def _set_object_attributes(self, attr_dict):
        for key, value in attr_dict.items():
            object.__setattr__(self, key, value)

    def reload(self):
        obj = ModelAPI(self.credentials, self.__class__).find(self.id)
        object.__setattr__(self, 'details', obj.details)
        self._set_object_attributes(obj.details)


class Factory(UpdatableMixin, TelestreamCloudModel):
    model_path = '/factories'

    def __init__(self, credentials, object_dict):
        super(Factory, self).__init__(credentials, object_dict)
        if self.details and 'id' in self.details.keys():
            self.credentials['factory_id'] = self.id

        self.videos = ModelAPI(self.credentials, Video)
        self.encodings = ModelAPI(self.credentials, Encoding)
        self.profiles = ModelAPI(self.credentials, Profile)

    def get_notifications(self):
        response = TelestreamCloudRequest('GET', '/notifications.json',
                                          self.credentials, data={}).send()
        return response.json()

    def update_notifications(self, conf=None):
        if 'send_video_payload' in conf:
            conf['send_video_payload'] = str(conf['send_video_payload']).lower()
        if 'events' in conf:
            for event in conf['events']:
                conf['events'][event] = str(conf['events'][event]).lower()
        response = TelestreamCloudRequest('PUT', '/notifications.json',
                                          self.credentials, data=conf).send()
        return response.json()

    def upload_session(self, path, **kwargs):
        return UploadSession(self.credentials, path, **kwargs)


class Video(TelestreamCloudModel):
    model_path = '/videos'

    def __init__(self, credentials, object_dict):
        super(Video, self).__init__(credentials, object_dict)
        path_prefix = '{}/{}'.format(self.model_path, self.id)
        object.__setattr__(self, 'encodings',
                           ModelAPI(self.credentials,
                                    Encoding, path_prefix=path_prefix))

    def metadata(self):
        path = '{}/{}/metadata.json'.format(self.model_path, self.id)
        resp = TelestreamCloudRequest('GET', path,
                                      self.credentials, data={}).send()
        return resp.json()

    def delete_source_file(self):
        path = '{}/{}/source.json'.format(self.model_path, self.id)
        resp = TelestreamCloudRequest('DELETE', path,
                                      self.credentials, data={}).send()
        return resp.json()


class Encoding(TelestreamCloudModel):
    model_path = '/encodings'

    def video(self):
        return ModelAPI(self.credentials, Video).find(self.video_id)

    def profile(self):
        key = self.details.get('profile_id', self.details['profile_name'])
        return ModelAPI(self.credentials, Profile).find(key)

    def retry(self):
        path = '{}/{}/retry.json'.format(self.model_path, self.id)
        resp = TelestreamCloudRequest('POST', path,
                                      self.credentials, data={}).send()
        return resp.json()

    def cancel(self):
        path = '{}/{}/cancel.json'.format(self.model_path, self.id)
        resp = TelestreamCloudRequest('POST', path,
                                      self.credentials, data={}).send()
        return resp.json()


class Profile(UpdatableMixin, TelestreamCloudModel):
    model_path = '/profiles'
