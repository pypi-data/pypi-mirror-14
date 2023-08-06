# -*- coding: utf-8 -*-
"""Test Setup of inqbus.tagging."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedBlobImage

# local imports
from inqbus.tagging.functions import image_to_meta, get_ignored_tags_form, \
    get_tagging_config
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.configuration.utilities import TaggingConfig


def image_by_path(path):
    dirname, filename = os.path.split(path)
    return NamedBlobImage(
        data=open(path, 'r').read(),
        filename=unicode(filename)
    )


class TestFunctions(unittest.TestCase):
    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Folder', 'test-folder')

        self.folder = self.portal['test-folder']

    def test_image_to_meta_no_image(self):
        result = image_to_meta(None)

        self.assertTrue(result)
        self.assertTrue('iptc' in result)
        self.assertTrue('exif' in result)
        self.assertTrue('xmp' in result)

    def test_get_config(self):
        config = get_tagging_config()

        self.assertIsInstance(config, TaggingConfig)

    def test_get_ignored_tags_for_form(self):
        config = get_tagging_config()

        config._ignored_tags = ['test', 'hallo']

        tags = get_ignored_tags_form()

        self.assertTrue(len(tags) == 2)
        self.assertTrue(tags[0] == {'tag': 'test'})
        self.assertTrue(tags[1] == {'tag': 'hallo'})

    def test_image_to_meta(self):
        self.folder.invokeFactory('Image', 'testimage')

        img = self.folder['testimage']

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")

        img.image = image_by_path(path)
        img.reindexObject()

        meta = image_to_meta(img)

        self.assertTrue(meta['iptc'])
        self.assertTrue(meta['exif'])

        meta = image_to_meta(img, use_exif=False)
        self.assertTrue(meta['iptc'])
        self.assertFalse(meta['exif'])

        meta = image_to_meta(img, use_iptc=False)
        self.assertTrue(meta['exif'])
        self.assertFalse(meta['iptc'])

