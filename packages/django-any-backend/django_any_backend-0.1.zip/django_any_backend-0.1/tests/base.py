import pycountry
from django_any_backend.testcases import AnyBackendTestCase

class PickleDBTest(AnyBackendTestCase):
    fixtures = ["tracks.default.json", "tracks.pickle_db.json"]