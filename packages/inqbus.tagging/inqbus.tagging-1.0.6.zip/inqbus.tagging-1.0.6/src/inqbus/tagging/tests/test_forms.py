try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

# zope imports
from plone.app.testing import TEST_USER_ID, setRoles, SITE_OWNER_NAME, \
    SITE_OWNER_PASSWORD, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
import transaction

# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.functions import get_tagging_config
from inqbus.tagging.tests.test_functions import image_by_path


class TestForms(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.browser = Browser(self.portal)

        # login as siteowner
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        self.browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        self.browser.getControl(name='submit').click()

        # create testdata
        dirname, filename = os.path.split(os.path.abspath(__file__))

        self.portal.invokeFactory('Folder', 'folder', title="Test Title")
        self.folder = self.portal['folder']

        # image with exif/iptc
        path = os.path.join(dirname, "test_images", "metadata-test-image-L.jpg")
        self.folder.invokeFactory('Image', 'testimage', image=image_by_path(path))
        self.exif_image = self.folder['testimage']

        # image with xmp
        path = os.path.join(dirname, "test_images", "small_IMG_5097.jpg")
        self.folder.invokeFactory('Image', 'testimage2', image=image_by_path(path))
        self.xmp_image = self.folder['testimage2']

        transaction.commit()

    def test_import_xmp_without_image(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-xmp-import')
        self.browser.getControl(name='form.widgets.test_image').value = ''
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertFalse('{http://ns.adobe.com/exif/1.0/}Flash' in self.browser.contents)
        self.assertFalse('{http://ns.adobe.com/exif/1.0/}ISOSpeedRatings' in self.browser.contents)
        self.assertFalse('{http://ns.adobe.com/exif/1.0/}UserComment' in self.browser.contents)
        self.assertFalse('Example' in self.browser.contents)
        self.assertFalse("['Inthronisation', 'Hohenfurch', 'Garde']" in self.browser.contents)

    def test_import_exif_without_image(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-exif-import')
        self.browser.getControl(name='form.widgets.test_image').value = ''
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertFalse('EXIF ApertureValue' in self.browser.contents)
        self.assertFalse('EXIF BodySerialNumber' in self.browser.contents)
        self.assertFalse('EXIF ExifVersion' in self.browser.contents)
        self.assertFalse('Example' in self.browser.contents)
        self.assertFalse("2015:01:10 21:29:40" in self.browser.contents)

    def test_import_iptc_without_image(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-iptc-import')
        self.browser.getControl(name='form.widgets.test_image').value = ''
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertFalse('Example' in self.browser.contents)
        self.assertFalse("['Inthronisation', 'Hohenfurch', 'Garde']" in self.browser.contents)

    def test_import_xmp(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-xmp-import')
        self.browser.getControl(name='form.widgets.test_image').value = self.xmp_image.UID()
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertTrue('{http://ns.adobe.com/exif/1.0/}Flash' in self.browser.contents)
        self.assertTrue('{http://ns.adobe.com/exif/1.0/}ISOSpeedRatings' in self.browser.contents)
        self.assertTrue('{http://ns.adobe.com/exif/1.0/}UserComment' in self.browser.contents)
        self.assertTrue('Example' in self.browser.contents)
        self.assertTrue("['Inthronisation', 'Hohenfurch', 'Garde']" in self.browser.contents)

    def test_import_exif(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-exif-import')
        self.browser.getControl(name='form.widgets.test_image').value = self.exif_image.UID()
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertTrue('EXIF ColorSpace' in self.browser.contents)
        self.assertTrue('EXIF ComponentsConfiguration' in self.browser.contents)
        self.assertTrue('EXIF FlashPixVersion' in self.browser.contents)
        self.assertTrue('Example' in self.browser.contents)
        self.assertTrue("Image Artist" in self.browser.contents)

    def test_import_iptc(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-iptc-import')
        self.browser.getControl(name='form.widgets.test_image').value = self.exif_image.UID()
        self.browser.getControl(name='form.buttons.ok').click()

        self.assertTrue('5' in self.browser.contents)
        self.assertTrue('IPTC Core Description' in self.browser.contents)
        self.assertTrue('IPTC Creator Job Title and IPTC' in self.browser.contents)
        self.assertTrue('Example' in self.browser.contents)
        self.assertTrue("IPTC Core Creator and IPTC Auth" in self.browser.contents)

    def test_main_config(self):
        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-settings')

        self.assertTrue('Use Exif' in self.browser.contents)
        self.assertTrue('Exif Fields' in self.browser.contents)
        self.assertTrue('Field' in self.browser.contents)
        self.assertTrue('Format String' in self.browser.contents)
        self.assertTrue('Regular Expression' in self.browser.contents)
        self.assertTrue('Use IPTC' in self.browser.contents)
        self.assertTrue('IPTC Fields' in self.browser.contents)
        self.assertTrue('Use XMP' in self.browser.contents)
        self.assertTrue('XMP Fields' in self.browser.contents)
        self.assertTrue('Ignored Title Tags' in self.browser.contents)

    def test_keyword_manager(self):
        # set some tags to make sure buttons are available in view
        self.exif_image.setSubject(['just', 'a', 'view', 'tags'])
        self.exif_image.reindexObject()
        transaction.commit()

        # just testing redirecting urls because nothing else was changed by inqbus.tagging
        self.browser.open(self.portal.absolute_url() + '/keyword_manager_view')

        self.browser.getControl(name='form.button.Merge').click()

        self.assertTrue('field' in self.browser.url)
        self.assertTrue('search' in self.browser.url)
        self.assertTrue('limit' in self.browser.url)
        self.assertTrue('keyword_manager_view' in self.browser.url)

    def test_view_permissions(self):
        # Site Owner
        self.browser.open(self.portal.absolute_url() + '/keyword_manager_view')
        self.assertFalse('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-xmp-import')
        self.assertFalse('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-settings')
        self.assertFalse('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-iptc-import')
        self.assertFalse('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-exif-import')
        self.assertFalse('Insufficient Privileges' in self.browser.contents)

        # Manager (other user)
        self.browser.open(self.portal.absolute_url() + '/logout')
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = TEST_USER_NAME
        self.browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        self.browser.getControl(name='submit').click()

        self.browser.open(self.portal.absolute_url() + '/keyword_manager_view')
        self.assertTrue('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-xmp-import')
        self.assertTrue('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-settings')
        self.assertTrue('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-iptc-import')
        self.assertTrue('Insufficient Privileges' in self.browser.contents)

        self.browser.open(self.portal.absolute_url() + '/@@inqbus-tagging-exif-import')
        self.assertTrue('Insufficient Privileges' in self.browser.contents)

    def tearDown(self):
        self.folder.manage_delObjects(["testimage", 'testimage2'])
        self.portal.manage_delObjects(['folder'])

        transaction.commit()

