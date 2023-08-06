from Products.Five.browser import BrowserView
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import field, button, form
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import getUtility

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from inqbus.tagging.configuration.utilities import ITaggingConfig
from inqbus.tagging.functions import get_ignored_tags_form, get_test_image, \
    image_to_meta, get_tagging_config

from inqbus.tagging import MessageFactory as _
from inqbus.tagging.subscriber import xmp

class ITableRowFieldSchema(model.Schema):
    field = schema.TextLine(title=_(u"Field"), required=True,
                            description=_(u'Add the name of the field.'))
    format = schema.TextLine(title=_(u"Format String"), required=False,
                             description=_(u'Add a format string to format the value or the cut out portion. Use unchanged value if nothing is set.'))
    regex = schema.TextLine(title=_(u"Regular Expression"), required=False,
                            description=_(u'Add Regular Expression to cut out a portion of the field value. Use all if nothing is set.'))


class ITableRowIgnoredSchema(model.Schema):
    tag = schema.TextLine(title=_(u"Tag"), required=True)


class FieldFactory(object):

    def __init__(self, field):
        self.field = field

    def __call__(self, *args, **kwargs):
        config_store = get_tagging_config()
        if config_store:
            return  getattr(config_store, self.field, None)
        return None


class ITaggingFormSchema(model.Schema):

    use_exif = schema.Bool(title = _(u"Use Exif"),
                           defaultFactory=FieldFactory('use_exif'),
                           description=_(u"Select if tags based on exif should be added."))




    exif_fields = schema.List(
            title=_(u"Exif Fields"),
            description=_(u"""List of the EXIF fields that are transformed into tags. You may specify a regular expression to cut out one or more portions of the EXIF value. Also you may specify a new style format string to shape the output of the exif value or the cut out portions.
Example: Value is "Newton, Issac", regex = "(\w+), (\w+)", format = "{1} {0}" -> Issac Newton"""),
            defaultFactory=FieldFactory('exif_fields'),
            value_type=DictRow(
                    title=_(u"EXIF Fields"),
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    use_iptc = schema.Bool(title = _(u"Use IPTC"),
                           defaultFactory=FieldFactory('use_iptc'),
                           description=_(u"Select if tags based on iptc should be added."))

    iptc_fields = schema.List(
            title=_(u"IPTC Fields"),
            description=_(u"""List of the IPTC fields that are transformed into tags. You may specify a regular expression to cut out a portion of the IPTC value. Also you may specify a format string to shape the output of the exif value or the cut out portion."""),
            defaultFactory=FieldFactory('iptc_fields'),
            value_type=DictRow(
                    title=_(u"IPTC Fields"),
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )

    use_xmp = schema.Bool(title = _(u"Use XMP"),
                           defaultFactory=FieldFactory('use_xmp'),
                           description=_(u"Select if tags based on xmp should be added."))

    xmp_fields = schema.List(
            title=_(u"XMP Fields"),
            description=_(u"""List of the XMP fields that are transformed into tags. You may specify a regular expression to cut out a portion of the XMP value. Also you may specify a format string to shape the output of the exif value or the cut out portion."""),
            defaultFactory=FieldFactory('xmp_fields'),
            value_type=DictRow(
                    title=_(u"XMP Fields"),
                    schema=ITableRowFieldSchema,
                ),
            required=False,
        )


    ignored_tags = schema.List(
            title=_(u"Ignored Title Tags"),
            description=_(u"List of Tags that are ignored, if importing the title to tags."),
            defaultFactory=get_ignored_tags_form,
            value_type=DictRow(
                    title=_(u"Tags"),
                    schema=ITableRowIgnoredSchema,
                ),
            required=False,
        )

    scan_title = schema.Bool(title = _(u"Match title tags"),
                           defaultFactory=FieldFactory('scan_title'),
                           description=_(u"If selected: The title will be scanned utilizing the regex below to find keywords. The keywords found will then be matched with the list of already existing keywords. If matched the content object will be tagged with the matching keywords."))

    scan_title_regex = schema.TextLine(title = _(u"Regular expression for matching title tags"),
                                defaultFactory=FieldFactory('scan_title_regex'),
                                description=_(u"Specify a regex to break the title into keywords. Each keyword then is produced further."),
                                required=False,
                                )

    new_tags_from_title = schema.Bool(title = _(u"New tags from title"),
                           defaultFactory=FieldFactory('new_tags_from_title'),
                           description=_(u"We recommended strongly to leave this choice disabled: If enabled each item found by the regex will produce a (new) keyword. This may flood your Plone with so many keywords that you may not get rid of them easily. But for a particular setup this choice may be handy."),
                           default= True)

    new_tags_from_title_regex = schema.TextLine(title = _(u"Regular expression for creating new tags from title"),
                                defaultFactory=FieldFactory('new_tags_from_title_regex'),
                                description=_(u"Specify a regex to break the title into keywords. Each keyword then is produced further."),
                                required=False,
                                )


class TaggingForm(AutoExtensibleForm, form.Form):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """
    schema = ITaggingFormSchema
    ignoreContext = True

    fields = field.Fields(ITaggingFormSchema)
    fields['exif_fields'].widgetFactory = DataGridFieldFactory
    fields['iptc_fields'].widgetFactory = DataGridFieldFactory
    fields['xmp_fields'].widgetFactory = DataGridFieldFactory
    fields['ignored_tags'].widgetFactory = DataGridFieldFactory

    label = _(u"Inqbus.tagging Configuration")
    description = _(u"Configure Filters for metadata tag generation here. ")

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        config_store = get_tagging_config()

        for field in data:
            setattr(config_store, field, data[field])

        self.status = "Data was saved"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """


class TagSettingsView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TaggingForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()

class ITagImportExif(model.Schema):
    test_image = RelationChoice(title=_(u"Select EXIF-Tags from Image"),
                               description=_(u"Here you can select an image to pick EXIF tags for the whitelists"),
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportExifEditForm(AutoExtensibleForm, form.EditForm):
    """
    Define form logic
    """
    ignoreContext = True
    schema = ITagImportExif
    label = _(u"Inqbus Tagging Settings - Import Tags")


    def __init__(self, context, request):
        super(TagImportExifEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = get_tagging_config()
        test_image = config_store.test_image

        if test_image and test_image.portal_type and test_image.portal_type == 'Image':
            exif = image_to_meta(test_image)['exif']
            exif_keys = exif.keys()
            exif_keys.sort()
            for exif_key in exif_keys:
                exif_field = exif[exif_key]
                if str(exif_field) and len(str(exif_field)) < 100 :
                    self.fields += field.Fields(schema.Bool(
                                            __name__=exif_key,
                                            title=unicode(exif_key),
                                            description=unicode("Example: " +str(exif_field)),
                                            default=False))

    def applyChanges(self, data):
        config_store = get_tagging_config()
        for field in data:
            if field == 'test_image' and data['test_image']:
                config_store.test_image = data['test_image']
                self.context.REQUEST.RESPONSE.redirect(self.request["ACTUAL_URL"])
            elif data[field]:
                config_store.add_exif_tag(field)

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        self.status = "Data was saved."

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""


class TagImportExifView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagImportExifEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()


class ITagImportIptc(model.Schema):
    test_image = RelationChoice(title=_(u"Select IPTC-Tags from Image"),
                               description=_(u"Here you can select an image to pick IPTC tags for the whitelists"),
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportIptcEditForm(TagImportExifEditForm):

    schema = ITagImportIptc
    label = _(u"Inqbus Tagging Settings - Import IPTC Tags")

    def __init__(self, context, request):
        super(TagImportIptcEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = get_tagging_config()
        test_image = config_store.test_image
        if test_image and test_image.portal_type and test_image.portal_type == 'Image':
            exif = image_to_meta(test_image)['iptc'].data
            exif_keys = exif.keys()
            exif_keys.sort()
            for exif_key in exif_keys:
                exif_field = exif[exif_key]
                if str(exif_field) and len(str(exif_field)) < 100 :
                    self.fields += field.Fields(schema.Bool(
                                            __name__=str(exif_key),
                                            title=unicode(exif_key),
                                            description=unicode("Example: " +str(exif_field)),
                                            default=False))

    def applyChanges(self, data):
        config_store = get_tagging_config()
        for field in data:
            if field == 'test_image' and data['test_image']:
                config_store.test_image = data['test_image']
                self.context.REQUEST.RESPONSE.redirect(self.request["ACTUAL_URL"])
            elif data[field]:
                config_store.add_iptc_tag(field)


class TagImportIptcView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagImportIptcEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()


class ITagImportXMP(model.Schema):
    test_image = RelationChoice(title=_(u"Select XMP-Tags from Image"),
                               description=_(u"Here you can select an image to pick XMPtags for the whitelists"),
                               vocabulary="plone.app.vocabularies.Catalog",
                               required=False,
                               defaultFactory=get_test_image
                               )


class TagImportXMPEditForm(TagImportExifEditForm):

    schema = ITagImportXMP
    label = _(u"Inqbus Tagging Settings - Import XMP Tags")

    def __init__(self, context, request):
        super(TagImportXMPEditForm, self).__init__(context, request)

    def updateFields(self):
        super(TagImportExifEditForm, self).updateFields()
        config_store = get_tagging_config()
        test_image = config_store.test_image

        if test_image and test_image.portal_type and test_image.portal_type == 'Image':

            xmp_data = image_to_meta(test_image)['xmp']

            xmp_keys = xmp_data.keys()
            xmp_keys.sort()
            for xmp_key in xmp_keys:
                xmp_field = xmp_data[xmp_key]
                if str(xmp_field) and len(str(xmp_field)) < 100 :
                    self.fields += field.Fields(schema.Bool(
                                            __name__=str(xmp_key),
                                            title=unicode(xmp_key),
                                            description=unicode("Example: " +str(xmp_field)),
                                            default=False))

    def applyChanges(self, data):
        config_store = get_tagging_config()
        for field in data:
            if field == 'test_image' and data['test_image']:
                config_store.test_image = data['test_image']
                self.context.REQUEST.RESPONSE.redirect(self.request["ACTUAL_URL"])
            elif data[field]:
                config_store.add_xmp_tag(field)


class TagImportXMPView(BrowserView):
    """
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    """

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(TagImportXMPEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()
