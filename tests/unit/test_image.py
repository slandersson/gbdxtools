'''
Authors: Donnie Marino, Kostas Stamatiou
Contact: dmarino@digitalglobe.com

Unit tests for the gbdxtools.Idaho class
'''

from gbdxtools import Interface
from gbdxtools.image import Image
from auth_mock import get_mock_gbdx_session
import vcr
from os.path import join, isfile, dirname, realpath
import tempfile
import unittest

# How to use the mock_gbdx_session and vcr to create unit tests:
# 1. Add a new test that is dependent upon actually hitting GBDX APIs.
# 2. Decorate the test with @vcr appropriately
# 3. Replace "dummytoken" with a real gbdx token
# 4. Run the tests (existing test shouldn't be affected by use of a real token).  This will record a "cassette".
# 5. Replace the real gbdx token with "dummytoken" again
# 6. Edit the cassette to remove any possibly sensitive information (s3 creds for example)


class IpeImageTest(unittest.TestCase):

    _temp_path = None

    @classmethod
    def setUpClass(cls):
        mock_gbdx_session = get_mock_gbdx_session(token='dymmytoken')
        cls.gbdx = Interface(gbdx_connection=mock_gbdx_session)
        #cls.gbdx = Interface()
        cls._temp_path = tempfile.mkdtemp()
        print("Created: {}".format(cls._temp_path))

    @vcr.use_cassette('tests/unit/cassettes/test_image_default.yaml', filter_headers=['authorization'])
    def test_basic_ipe_image(self):
        _id = '104001002838EC00'
        img = Image(_id)
        self.assertTrue(isinstance(img, Image))
        assert img._node_id == 'toa_reflectance'
        assert img.shape == (8, 78848, 11008)
        assert img._proj == 'EPSG:4326'

    @vcr.use_cassette('tests/unit/cassettes/test_image_default.yaml', filter_headers=['authorization'])
    def test_ipe_image_with_aoi(self):
        _id = '104001002838EC00'
        img = Image(_id, bbox=[-85.81455230712892,10.416235163695223,-85.77163696289064,10.457089934231618])
        assert img._node_id == 'toa_reflectance'
        assert img.shape == (8, 3013, 3190)
        assert img._proj == 'EPSG:4326'

    @vcr.use_cassette('tests/unit/cassettes/test_image_proj.yaml', filter_headers=['authorization'])
    def test_ipe_image_with_proj(self):
        _id = '104001002838EC00'
        img = Image(_id, bbox=[-85.81455230712892,10.416235163695223,-85.77163696289064,10.457089934231618], proj='EPSG:3857')
        assert img._node_id == 'toa_reflectance'
        assert img.shape == (8, 3064, 3190)
        assert img._proj == 'EPSG:3857' 

