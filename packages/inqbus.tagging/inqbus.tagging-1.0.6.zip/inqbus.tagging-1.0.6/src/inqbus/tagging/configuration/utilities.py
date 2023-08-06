from persistent import Persistent
from persistent.list import PersistentList
from plone.api import content
import re
from zope.interface import Attribute
from zope.interface import implements
from zope.interface.interface import Interface


class ITaggingConfig(Interface):
    use_exif = Attribute("Boolean describing if exif should be converted to tags")

    use_iptc = Attribute("Boolean describing if iptc should be converted to tags")

    use_xmp = Attribute("Boolean describing if XMP should be converted to tags")


    exif_fields = Attribute("List holding information for converting exif")

    iptc_fields = Attribute("List holding information for converting iptc")

    xmp_fields = Attribute("List holding information for converting XMP")

    scan_title = Attribute("Boolean describing if title words should tag the object if the tags are already used")

    _scan_title_regex = Attribute("String holding a regex to filter title words")

    scan_regex_compiled = Attribute("the compiled regex")

    new_tags_from_title = Attribute("Should tags in the title generate new tags ")

    _new_tags_from_title_regex = Attribute("String holding a regex to filter title words")

    new_tags_from_title_regex_compiled = Attribute("the compiled regex")



class TaggingConfig(Persistent):
    implements(ITaggingConfig)

    use_exif = True
    use_iptc = True
    use_xmp = True
    scan_title = False
    _scan_title_regex = u""
    new_tags_from_title = False
    _new_tags_from_title_regex = u""

    def __init__(self):
        self._exif_fields = []
        self._iptc_fields = []
        self._xmp_fields = []
        self._ignored_tags = []
        self._test_image = None
        self.scan_title_regex_compiled = None
        self.new_tags_from_title_regex_compiled = None

    @property
    def exif_fields(self):
        return self._exif_fields

    @exif_fields.setter
    def exif_fields(self, value):
        self._exif_fields = value
        self._p_changed = True

    @property
    def iptc_fields(self):
        return self._iptc_fields

    @iptc_fields.setter
    def iptc_fields(self, value):
        self._iptc_fields = value
        self._p_changed = True

    @property
    def xmp_fields(self):
        return self._xmp_fields

    @xmp_fields.setter
    def xmp_fields(self, value):
        self._xmp_fields = value
        self._p_changed = True

    @property
    def ignored_tags(self):
        return self._ignored_tags

    @ignored_tags.setter
    def ignored_tags(self, value):
        self._ignored_tags = []
        for dict in value:
            self._ignored_tags.append(dict['tag'])
        self._p_changed = True

    @property
    def test_image(self):
        try:
            result = content.get(UID=self._test_image)
        except Exception as e:
            return None
        return result

    @test_image.setter
    def test_image(self, value):
        if hasattr(value, 'UID'):
            self._test_image = value.UID()
        else:
            self._test_image = ''
        self._p_changed = True

    @property
    def test_image(self):
        try:
            result = content.get(UID=self._test_image)
        except Exception as e:
            return None
        return result

    @test_image.setter
    def test_image(self, value):
        if hasattr(value, 'UID'):
            self._test_image = value.UID()
        else:
            self._test_image = ''
        self._p_changed = True

    @property
    def scan_title_regex(self):
        return self._scan_title_regex

    @scan_title_regex.setter
    def scan_title_regex(self, value):
        self._scan_title_regex = value
        try:
            if value:
                self.scan_title_regex_compiled = re.compile(value)
        except re.error as e:
            raise e
        self._p_changed = True

    @property
    def new_tags_from_title_regex(self):
        return self._new_tags_from_title_regex

    @new_tags_from_title_regex.setter
    def new_tags_from_title_regex(self, value):
        self._new_tags_from_title_regex = value
        try:
            if value:
                self.new_tags_from_title_regex_compiled = re.compile(value)
        except re.error as e:
            raise e
        self._p_changed = True

    def add_exif_tag(self, tag):
        self.exif_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True

    def add_iptc_tag(self, tag):
        self.iptc_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True

    def add_xmp_tag(self, tag):
        self.xmp_fields.append({
            'regex': None,
            'field': unicode(tag),
            'format': None
        })
        self._p_changed = True
