from zope.i18nmessageid import MessageFactory

import logging

from inqbus.tagging import config


# Set up the i18n message factory for our package
MessageFactory = MessageFactory('inqbus.tagging')

logger = logging.getLogger(config.PROJECT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

