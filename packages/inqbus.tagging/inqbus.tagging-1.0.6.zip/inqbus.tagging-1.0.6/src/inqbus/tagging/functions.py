from Products.CMFCore.utils import getToolByName
import exifread
from iptcinfo import IPTCInfo
from zope.component.hooks import getSite


from StringIO import StringIO

from zope.component import getUtility, queryUtility

from inqbus.tagging.configuration.utilities import ITaggingConfig
from inqbus.tagging.subscriber import xmp


def get_tagging_config():
    return queryUtility(ITaggingConfig,"TaggingConfig")

def get_ignored_tags():
    config_store = getUtility(ITaggingConfig,"TaggingConfig")
    return config_store.ignored_tags


def get_ignored_tags_form():
    tags = get_ignored_tags()
    tag_list = []
    for tag in tags:
        tag_list.append({'tag': tag})
    return tag_list


def get_test_image():
    config_store = get_tagging_config()
    return config_store.test_image


def image_to_meta(context, use_exif=True, use_iptc=True, use_xmp=True ):

    meta = {}
    if hasattr(context, 'image') and context.image:
        image = context.image
    else:
        return {'iptc': {}, 'exif': {}, 'xmp': {}}
    data = image.data

    io = StringIO(data)
    io.seek(0)
    if use_iptc :
        meta['iptc'] = IPTCInfo(io, force=True)
        io.seek(0)
    else:
        meta['iptc'] = {}

    if use_exif :
        meta['exif'] = exifread.process_file(io)
        io.seek(0)
    else:
        meta['exif'] = {}

    if use_xmp :
        meta['xmp'] = xmp.parse(image.data)
    else:
        meta['xmp'] = {}

    io.close()
    return meta


def add_tags(obj, tags_to_add=[]):
    if not hasattr(obj, 'Subject'):
        return

    tags = list(obj.Subject()) + tags_to_add
    tags = list(set(tags))

    clear_tags = []

    for tag in tags:

        try:
            int(tag)
        except ValueError:
            pass
        else:
            continue

        try:
            clear_tag = unicode(tag)
        except UnicodeDecodeError:
            continue

        ignored_tags = get_ignored_tags()

        if len(clear_tag) < 100 and tag not in ignored_tags:
            clear_tags.append(clear_tag)

    obj.setSubject(clear_tags)
    obj.reindexObject()


def get_all_keywords(context):
    """
    Get the list of current keywords. TODO: Caching, use sets or dict
    :param context:
    :return:
    """
    # does not work with context in test, but with site
    catalog = getToolByName(getSite(), 'portal_catalog')
    # catalog = getToolByName(context, 'portal_catalog')
    keywords = list(catalog.uniqueValuesFor('Subject'))
    keywords.sort(key=lambda x:x.lower())
    return keywords
