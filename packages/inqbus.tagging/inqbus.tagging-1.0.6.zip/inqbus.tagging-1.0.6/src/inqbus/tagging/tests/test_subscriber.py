try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
import transaction
# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.functions import get_tagging_config, image_to_meta
from inqbus.tagging.tests.test_functions import image_by_path


class TestSubscriber(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.config = get_tagging_config()

        self.config.scan_title = True
        self.config.new_tags_from_title = True

        self.config.scan_title_regex = '(\w+)'
        self.config.new_tags_from_title_regex = '(\w+)'

    def _get_token(self, context):
        authenticator = getMultiAdapter(
            (context, self.request), name='authenticator')

        return authenticator.token()

    def test_title(self):

        self.portal.invokeFactory('Image', 'test-image', title="Test Title")

        folder = self.portal['test-image']

        subjects = folder.Subject()

        self.assertTrue('Test' in subjects)
        self.assertTrue('Title' in subjects)

    def test_rotation_and_filename_tags(self):
        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "Landscape_5.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path),
                             title="Different Title")

        image = folder['testimage']

        self.assertTrue(image.image._height < image.image._width)
        subjects = image.Subject()

        self.assertTrue('Different' in subjects)
        self.assertTrue('Title' in subjects)
        self.assertFalse('Landscape_5' in subjects)

    def test_meta_tags(self):
        self.config.add_exif_tag('Image Copyright')
        self.config.add_iptc_tag('5')
        self.config.add_iptc_tag('25')

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        meta = image_to_meta(image)

        exif = meta['exif']
        iptc = meta['iptc'].data

        subjects = image.Subject()

        self.assertTrue(exif['Image Copyright'].printable in subjects)

        self.assertFalse(exif['EXIF FlashPixVersion'].printable in subjects)

        self.assertTrue(iptc[5] in subjects)
        # iptc[25 is a list
        self.assertTrue(iptc[25][0] in subjects)

    def test_meta_tags_with_only_regex(self):
        self.config.exif_fields = [{
            'regex': u'(\w+)',
            'field': u'Image Copyright',
            'format': None
        }]

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        meta = image_to_meta(image)

        exif = meta['exif']

        subjects = image.Subject()

        self.assertFalse(exif['Image Copyright'].printable in subjects)
        self.assertTrue('IPTC' in subjects)
        self.assertFalse('Core' in subjects)

    def test_meta_tags_with_only_format(self):
        self.config.exif_fields = [{
            'regex': None,
            'field': u'Image Copyright',
            'format': 'hello_{0}'
        }]

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        meta = image_to_meta(image)

        exif = meta['exif']

        subjects = image.Subject()

        self.assertFalse(exif['Image Copyright'].printable in subjects)
        self.assertTrue('hello_' + exif['Image Copyright'].printable in subjects)

    def test_meta_tags_with_regex_and_format(self):
        self.config.exif_fields = [{
            'regex': '(\w+) (\w+)',
            'field': u'Image Copyright',
            'format': 'hello_{1}_{0}'
        }]

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        meta = image_to_meta(image)

        exif = meta['exif']

        subjects = image.Subject()

        self.assertFalse(exif['Image Copyright'].printable in subjects)
        self.assertTrue('hello_Core_IPTC' in subjects)

    def test_regex_no_match(self):
        self.config.exif_fields = [{
            'regex': '(\w+) (\w+)',
            'field': u'Image Copyright',
            'format': 'hello_{1}_{0}'
        }]

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "small_IMG_5097.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        meta = image_to_meta(image)

        exif = meta['exif']

        subjects = image.Subject()

        self.assertFalse(exif['Image Copyright'].printable in subjects)
        self.assertTrue(subjects)

    def test_xmp_and_ignored_list(self):
        self.config.xmp_fields = [{
            'regex': '',
            'field': u'{http://purl.org/dc/elements/1.1/}subject',
            'format': ''
        }]
        self.config.ignored_tags = [{'tag': 'Garde'}]

        self.portal.invokeFactory('Folder', 'test-folder', title="Test Title")

        folder = self.portal['test-folder']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "small_IMG_5097.jpg")

        folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = folder['testimage']

        subjects = image.Subject()

        self.assertTrue('Inthronisation' in subjects)
        self.assertTrue('Hohenfurch' in subjects)
        self.assertFalse('Garde' in subjects)