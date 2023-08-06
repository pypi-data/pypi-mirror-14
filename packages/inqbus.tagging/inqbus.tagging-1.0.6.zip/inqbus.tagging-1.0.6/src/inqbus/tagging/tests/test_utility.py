# -*- coding: utf-8 -*-
"""Test Setup of inqbus.tagging."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import types

# zope imports
from zope.component import queryUtility

# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.configuration.utilities import ITaggingConfig, TaggingConfig


class TestConfiguration(unittest.TestCase):
    """Validate setup process for inqbus.tagging."""

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.portal = self.layer['portal']

    def test_get_utility(self):
        utility = queryUtility(ITaggingConfig, 'TaggingConfig')
        self.assertIsInstance(utility, TaggingConfig)

    def test_attributes(self):
        utility = queryUtility(ITaggingConfig, 'TaggingConfig')
        self.assertIsInstance(utility.use_exif, types.BooleanType)
        self.assertIsInstance(utility.use_iptc, types.BooleanType)
        self.assertIsInstance(utility.use_xmp, types.BooleanType)
        self.assertIsInstance(utility.scan_title, types.BooleanType)

        self.assertIsInstance(utility._scan_title_regex, types.StringTypes)
        self.assertIsInstance(utility._new_tags_from_title_regex, types.StringTypes)

        self.assertIsInstance(utility.exif_fields, types.ListType)
        self.assertIsInstance(utility.iptc_fields, types.ListType)
        self.assertIsInstance(utility.xmp_fields, types.ListType)
        self.assertIsInstance(utility.ignored_tags, types.ListType)

        self.assertTrue(hasattr(utility, 'test_image'))

    def test_default_values(self):
        utility = queryUtility(ITaggingConfig, 'TaggingConfig')
        self.assertTrue(utility.use_exif)
        self.assertTrue(utility.use_iptc)
        self.assertFalse(utility.scan_title)
        self.assertTrue(utility.use_xmp)

        self.assertEqual(utility.exif_fields, [])
        self.assertEqual(utility.ignored_tags, [])
        self.assertEqual(utility.iptc_fields, [])
        self.assertEqual(utility.xmp_fields, [])

        self.assertEqual(utility._scan_title_regex, u"")
        self.assertEqual(utility._new_tags_from_title_regex, u"")

    def test_add_methods(self):
        utility = queryUtility(ITaggingConfig, 'TaggingConfig')

        utility.add_exif_tag('test')
        utility.add_iptc_tag('test')
        utility.add_xmp_tag('test')

        self.assertEqual(utility.exif_fields, [{
            'regex': None,
            'field': u'test',
            'format': None
        }])
        self.assertEqual(utility.iptc_fields, [{
            'regex': None,
            'field': u'test',
            'format': None
        }])
        self.assertEqual(utility.xmp_fields, [{
            'regex': None,
            'field': u'test',
            'format': None
        }])

    def test_getter_and_setter(self):
        utility = queryUtility(ITaggingConfig, 'TaggingConfig')

        utility.exif_fields = ['test']

        self.assertEqual(utility.exif_fields, ['test'])
        self.assertEqual(utility._exif_fields, ['test'])

        utility.iptc_fields = ['test']

        self.assertEqual(utility.iptc_fields, ['test'])
        self.assertEqual(utility._iptc_fields, ['test'])

        utility.xmp_fields = ['test']

        self.assertEqual(utility.xmp_fields, ['test'])
        self.assertEqual(utility._xmp_fields, ['test'])

        utility.ignored_tags = [{'tag': 'test'}]
        self.assertEqual(utility.ignored_tags, ['test'])
        self.assertEqual(utility._ignored_tags, ['test'])

