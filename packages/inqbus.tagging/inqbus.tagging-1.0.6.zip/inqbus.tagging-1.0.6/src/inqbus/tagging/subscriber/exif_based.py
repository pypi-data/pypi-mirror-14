import re
from StringIO import StringIO

import PIL
import exifread

from inqbus.tagging.config import ORIENTATIONS, HORIZONTAL_MIRROR, \
    VERTICAL_MIRROR
from inqbus.tagging.functions import image_to_meta, add_tags, get_tagging_config


def get_tags(image_tags, tag_config):
    tags = []
    available_fields = []
    field_value = {}
    for key in image_tags.keys():
        available_fields.append(str(key))
        field_value[str(key)] = image_tags[key]
    allowed_fields = []
    field_info = {}
    for dict in tag_config:
        allowed_fields.append(dict['field'])
        field_info[dict['field']] = dict
    available_fields = set(available_fields)
    allowed_fields = set(allowed_fields)
    fields = available_fields.intersection(allowed_fields)

    for field in fields:
        regex = field_info[field]['regex']
        str_format = field_info[field]['format']
        value = field_value[field]

        if isinstance(value, list):
            for subvalue in value:
                tag = get_tag(subvalue, regex, str_format)
                if tag:
                    tags.append(tag)
        else:
            tag = get_tag(value, regex, str_format)
            if tag:
                tags.append(tag)

    return tags


def get_tag(value, regex, str_format):
    if hasattr(value, 'printable'):
        value = value.printable
    if regex:
        match = re.search(regex, value)
        if match and str_format:
            return str_format.format(*match.groups())
        elif match:
            return match.group(0)
        else:
            return

    if str_format:
        return str_format.format(value)
    else:
        return value


def meta_to_tag(context, event):

    tagging_config = get_tagging_config()

    meta = image_to_meta(context,
                         use_exif=tagging_config.use_exif,
                         use_iptc=tagging_config.use_iptc,
                         use_xmp=tagging_config.use_xmp)

    allowed_exif = tagging_config.exif_fields
    allowed_iptc = tagging_config.iptc_fields
    allowed_xmp = tagging_config.xmp_fields

    if hasattr(meta['iptc'], 'data'):
        iptc = meta['iptc'].data
    else:
        iptc = meta['iptc']
    exif = meta['exif']
    xmp = meta['xmp']

    tags = list(context.Subject())

    if tagging_config.use_iptc:
        tags = tags + get_tags(iptc, allowed_iptc)

    if tagging_config.use_exif:
        tags = tags + get_tags(exif, allowed_exif)

    if tagging_config.use_xmp:
        tags = tags + get_tags(xmp, allowed_xmp)

    add_tags(context, tags_to_add=tags)


def exif_to_orientation(context, event):

    if not (hasattr(context, 'image') and context.image):
        return

    try:
        from jpegtran import JPEGImage
    except ImportError:
        rotate_with_pillow(context)
    else:
        # use jpegtran to rotate
        rotate_with_jpegtran(context)


def rotate_with_jpegtran(context):
    image = context.image
    data = image.data

    from jpegtran import JPEGImage

    jpeg_image = JPEGImage(blob=data)

    try:
        image.data = jpeg_image.exif_autotransform().as_blob()
    except Exception as e:
        if 'Could not find EXIF orientation' in e.args:
            pass
        else:
            raise
    else:
        context.reindexObject()


def rotate_with_pillow(context):
    # use Pillow to rotate
    image = context.image
    data = image.data

    io = StringIO(data)
    io.seek(0)

    exif_tags = exifread.process_file(io)
    orientation = get_orientation(exif_tags)

    io.seek(0)

    pil_image = PIL.Image.open(io)
    converted_img_io = StringIO()

    if orientation:
        rotation = ORIENTATIONS[orientation][1]
        if rotation:
            mirror = ORIENTATIONS[orientation][2]

            rotated_image = pil_image.rotate(360-rotation,
                                             resample=PIL.Image.BICUBIC,
                                             expand=True)
            if mirror == HORIZONTAL_MIRROR:
                rotated_image = rotated_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            elif mirror == VERTICAL_MIRROR:
                rotated_image = rotated_image.transpose(PIL.Image.FLIP_TOP_BOTTOM)

            rotated_image.save(converted_img_io, 'JPEG', quality=100)

            image.data = converted_img_io.getvalue()

            context.reindexObject()

    converted_img_io.close()
    io.close()


def get_orientation(tags):
    if 'Image Orientation' in tags:
        rot_index = tags['Image Orientation'].values[0]
        return rot_index
    else:
        return None