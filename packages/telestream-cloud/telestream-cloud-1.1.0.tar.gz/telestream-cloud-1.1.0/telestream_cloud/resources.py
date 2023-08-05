from .models import ModelAPI, Factory


class Flip(object):

    def __init__(self, credentials):
        self.credentials = credentials
        self.factories = ModelAPI(self.credentials, Factory)
