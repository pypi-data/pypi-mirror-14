from ..base import PickleDBTest
from testapp.models import Artist, Track
from sql_testapp.models import Track as SQLTrack, Artist as SQLArtist

class PickleDBModelTest(PickleDBTest):

    def test_create_delete(self):
        params1 = {"album": "Live And Dangerous", "name": "The Boys Are Back In Town", "release_date": "1978-06-02"}
        params2 = params1.copy()
        artist_params = {"id": 10}
        artist1 = SQLArtist.objects.filter(**artist_params).get()
        artist2 = Artist.objects.filter(**artist_params).get()
        self.assertDeleteEqual(SQLTrack, Track, params1)
        params1['artist'] = artist1
        params2['artist'] = artist2
        self.assertSaveEqual(SQLTrack, Track, params1, params2)

    def test_update(self):
        filters = {"name": "Enter Sandman"}
        params = {"album": "Metallica"}
        qs1 = SQLTrack.objects.filter(**filters)
        qs2 = Track.objects.filter(**filters)
        self.assertSaveUpdateEqual(qs1, qs2, params)