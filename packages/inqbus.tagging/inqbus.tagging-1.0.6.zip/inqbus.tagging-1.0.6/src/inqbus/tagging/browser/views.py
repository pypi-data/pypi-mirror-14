import json

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.PloneKeywordManager.browser.prefs_keywords_view import PrefsKeywordsView
from plone import api
from plone.app.content.browser.contents import FolderContentsView
from plone.app.content.browser.file import TUS_ENABLED
from plone.app.content.utils import json_dumps
from plone.autoform.form import AutoExtensibleForm
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite
from zope.i18n import translate
from inqbus.tagging import logger

from inqbus.tagging import MessageFactory as _

class InqbusTaggingFolderContentsView(FolderContentsView):

    def __call__(self):
        site = getSite()
        base_url = site.absolute_url()
        base_vocabulary = '%s/@@getVocabulary?name=' % base_url
        site_path = site.getPhysicalPath()
        context_path = self.context.getPhysicalPath()
        options = {
            'vocabularyUrl': '%splone.app.vocabularies.Catalog' % (
                base_vocabulary),
            'urlStructure': {
                'base': base_url,
                'appended': '/folder_contents'
            },
            'moveUrl': '%s{path}/fc-itemOrder' % base_url,
            'indexOptionsUrl': '%s/@@qsOptions' % base_url,
            'contextInfoUrl': '%s{path}/@@fc-contextInfo' % base_url,
            'setDefaultPageUrl': '%s{path}/@@fc-setDefaultPage' % base_url,
            'availableColumns': {
                'id': translate(_('ID'), context=self.request),
                'preview': translate(_('Preview'), context=self.request),
                'ModificationDate': translate(_('Last modified'), context=self.request),  # noqa
                'EffectiveDate': translate(_('Publication date'), context=self.request),  # noqa
                'CreationDate': translate(_('Created on'), context=self.request),  # noqa
                'review_state': translate(_('Review state'), context=self.request),  # noqa
                'Subject': translate(_('Tags'), context=self.request),
                'Type': translate(_('Type'), context=self.request),
                'is_folderish': translate(_('Folder'), context=self.request),
                'exclude_from_nav': translate(_('Excluded from navigation'), context=self.request),  # noqa
                'getObjSize': translate(_('Object Size'), context=self.request),  # noqa
                'last_comment_date': translate(_('Last comment date'), context=self.request),  # noqa
                'total_comments': translate(_('Total comments'), context=self.request),  # noqa
            },
            'buttons': self.get_actions(),
            'rearrange': {
                'properties': {
                    'id': translate(_('Id'), context=self.request),
                    'sortable_title': translate(_('Title'), context=self.request),  # noqa
                    'modified': translate(_('Last modified'), context=self.request),  # noqa
                    'created': translate(_('Created on'), context=self.request),  # noqa
                    'effective': translate(_('Publication date'), context=self.request),  # noqa
                    'Type': translate(_('Type'), context=self.request)
                },
                'url': '%s{path}/@@fc-rearrange' % base_url
            },
            'basePath': '/' + '/'.join(context_path[len(site_path):]),
            'upload': {
                'relativePath': 'fileUpload',
                'baseUrl': base_url,
                'initialFolder': IUUID(self.context, None),
                'useTus': TUS_ENABLED
            }
        }
        self.options = json_dumps(options)
        return super(FolderContentsView, self).__call__()

    def json_response(self, data):
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(data)

    def image_html(self):

        image_uid = self.request.get('uid')
        if image_uid:
            image = api.content.get(UID=image_uid)
        else:
            image = None
        if image:
            html = '<img src=%s />' % (
                image.absolute_url()+"/@@images/image/mini")
        else:
            html = ''

        return self.json_response({'html': html})


class KeywordManagerView(PrefsKeywordsView):

    template = ViewPageTemplateFile('templates/keyword_manager_view.pt')

    def doReturn(self, message='', msg_type='', field=''):
        """
        set the message and return
        """
        if message and msg_type:
            pu = getToolByName(self.context, "plone_utils")
            pu.addPortalMessage(message, type=msg_type)

        logger.info(self.context.translate(message))
        portal_url = self.context.portal_url()
        url = "%s/keyword_manager_view" % portal_url

        field = self.request.get('field', '')
        limit = self.request.get('limit', '')
        search = self.request.get('search', '')

        if field or limit or search:
            url = "%s?field=%s&search=%s&limit=%s" % (url, field, search,
                                                      limit)

        self.request.RESPONSE.redirect(url)

