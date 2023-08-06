try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from plone.app.testing import TEST_USER_ID, setRoles
# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.functions import get_tagging_config
from inqbus.tagging.tests.test_functions import image_by_path
from inqbus.tagging.subscriber.exif_based import rotate_with_jpegtran, rotate_with_pillow


class TestRotation(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.config = get_tagging_config()

        self.config.new_tags_from_title = True

        self.config.title_regex = '(\w+)'

    def test_rotation_jpegtran(self):
        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "Landscape_5.jpg")

        folder.invokeFactory('Image', 'testimage')

        image = folder['testimage']

        image.image = image_by_path(path)

        rotate_with_jpegtran(image)

        self.assertTrue(image.image._height < image.image._width)

    def test_rotation_pillow(self):
        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "Landscape_5.jpg")

        folder.invokeFactory('Image', 'testimage')

        image = folder['testimage']

        image.image = image_by_path(path)

        rotate_with_pillow(image)

        self.assertTrue(image.image._height < image.image._width)
