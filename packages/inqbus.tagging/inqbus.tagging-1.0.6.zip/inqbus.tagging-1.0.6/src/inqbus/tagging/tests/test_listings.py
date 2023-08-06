try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.tests.test_functions import image_by_path


class TestContentListings(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Folder', 'test-folder')

        self.folder = self.portal['test-folder']


    def test_available_actions(self):
        view = getMultiAdapter(
            (self.folder, self.request),
            name="folder_contents"
        )
        view = view.__of__(self.folder)
        results = view()

        self.assertTrue('Retag' in results)

    def test_available_columns(self):
        view = getMultiAdapter(
            (self.folder, self.request),
            name='folder_contents'
        )
        view = view.__of__(self.folder)
        results = view()
        self.assertTrue('tags' in results)
        self.assertTrue('preview' in results)

    def test_get_image(self):
        view = view = getMultiAdapter(
            (self.folder, self.request),
            name='folder_contents'
        )

        result = view.image_html()
        self.assertFalse('img' in result)

        dirname, filename = os.path.split(os.path.abspath(__file__))

        path = os.path.join(dirname, "test_images", "small_IMG_5097.jpg")

        self.folder.invokeFactory('Image', 'testimage', image=image_by_path(path))

        image = self.folder['testimage']

        self.request.form.update({'uid': image.UID()})

        view = view = getMultiAdapter(
            (self.folder, self.request),
            name='folder_contents'
        )

        result = view.image_html()
        self.assertTrue('img' in result)