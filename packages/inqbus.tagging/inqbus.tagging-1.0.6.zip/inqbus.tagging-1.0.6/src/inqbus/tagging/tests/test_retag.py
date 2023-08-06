try:
    import unittest2 as unittest
except ImportError:
    import unittest

# zope imports
from inqbus.tagging import MessageFactory as _
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate
import transaction
# local imports
from inqbus.tagging.testing import INQBUS_TAGGING_INTEGRATION_TESTING
from inqbus.tagging.browser.actions import RetagAction
from inqbus.tagging.configuration.utilities import ITaggingConfig


class TestRetag(unittest.TestCase):

    layer = INQBUS_TAGGING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Image', 'test-image')

        self.image = self.portal['test-image']

    def _get_token(self, context):
        authenticator = getMultiAdapter(
            (context, self.request), name='authenticator')

        return authenticator.token()

    def test_action(self):

        options = RetagAction(self.image, self.request).get_options()

        self.assertTrue('title' in options)
        self.assertTrue(options['title'] == translate(_('Retag'),
                                                      context=self.request))
        self.assertTrue('id' in options)
        self.assertTrue(options['id'] == 'retag')
        self.assertTrue('icon' in options)
        self.assertTrue(options['icon'] == 'random')
        self.assertTrue('url' in options and 'fc-retag' in options['url'])
        self.assertTrue('form' in options)

    def test_view(self):
        config = queryUtility(ITaggingConfig, 'TaggingConfig')
        config.new_tags_from_title = False
        config.scan_title = False

        self.request["REQUEST_METHOD"] = "POST"
        self.request.form.update({'UID_test': self.image.UID(),
                                  '_authenticator': self._get_token(self.portal)})

        self.image.title = 'Test Image'

        subjects = self.image.Subject()

        self.assertTrue('Test' not in subjects)
        self.assertTrue('Image' not in subjects)

        config.new_tags_from_title = True
        config.scan_title = True

        view = getMultiAdapter(
            (self.portal, self.request),
            name='fc-retag'
        )
        _result = view()

        self.assertFalse(view.errors)

        subjects = self.image.Subject()

        # no regex was set and no tag will be generated without regex
        self.assertTrue('Test' not in subjects)
        self.assertTrue('Image' not in subjects)

        config.new_tags_from_title_regex = '(\w+)'

        _result = view()

        self.assertFalse(view.errors)

        subjects = self.image.Subject()

        self.assertTrue('Test' in subjects)
        self.assertTrue('Image' in subjects)