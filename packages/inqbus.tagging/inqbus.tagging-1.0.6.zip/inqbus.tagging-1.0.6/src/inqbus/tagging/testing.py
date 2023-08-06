# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

# local imports
from inqbus.tagging import config


class InqbusTaggingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import inqbus.tagging
        xmlconfig.file(
            'testing.zcml',
            inqbus.tagging,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        # Insert some test data.
        applyProfile(portal, config.TEST_DATA_PROFILE)


INQBUS_TAGGING_FIXTURE = InqbusTaggingLayer()


INQBUS_TAGGING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INQBUS_TAGGING_FIXTURE,),
    name='InqbusTaggingLayer:IntegrationTesting'
)


JLU_UBLIBRARYDB_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INQBUS_TAGGING_FIXTURE,),
    name='InqbusTaggingLayer:FunctionalTesting'
)


INQBUS_TAGGING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        INQBUS_TAGGING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='InqbusTaggingLayer:AcceptanceTesting'
)
