from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from inqbus.tagging import MessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice


class ILayer(Interface):
    pass

