# -*- coding: utf-8 -*-
import transaction
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from inqbus.tagging import MessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZODB.POSException import ConflictError
from plone.app.content.browser.contents import ContentsBaseAction
from plone.app.content.interfaces import IStructureAction
from zope.i18n import translate
from zope.interface import implementer
from inqbus.tagging.functions import get_tagging_config

from inqbus.tagging.subscriber.exif_based import meta_to_tag
from inqbus.tagging.subscriber.title_based import title_to_tag


@implementer(IStructureAction)
class RetagAction(object):

    template = ViewPageTemplateFile('templates/retag.pt')
    order = 5

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_options(self):
        return {
            'title': translate(_('Retag'), context=self.request),
            'id': 'retag',
            'icon': 'random',
            'url': self.context.absolute_url() + '/@@fc-retag',
            'form': {
                'template': self.template()
            }
        }


class RetagActionView(ContentsBaseAction):
    success_msg = _('Items retaged')
    failure_msg = _('Failed to retag all items')

    def __call__(self):
        self.errors = []
        self.protect()
        context = aq_inner(self.context)

        catalog = getToolByName(context, 'portal_catalog')
        mtool = getToolByName(context, 'portal_membership')
        config = get_tagging_config()

        missing = []
        for key in self.request.form.keys():
            if not key.startswith('UID_'):
                continue
            uid = self.request.form[key]
            brains = catalog(UID=uid)
            if len(brains) == 0:
                missing.append(uid)
                continue
            obj = brains[0].getObject()
            title = self.objectTitle(obj)
            if not mtool.checkPermission('Copy or Move', obj):
                self.errors(_(u'Permission denied to retag ${title}.',
                              mapping={u'title': title}))
                continue

            sp = transaction.savepoint(optimistic=True)

            try:
                meta_to_tag(obj, None)
                title_to_tag(obj, None)
            except ConflictError:
                raise
            except Exception:
                sp.rollback()
                self.errors.append(_('Error retagging ${title}', mapping={
                    'title': title}))

        return self.message(missing)