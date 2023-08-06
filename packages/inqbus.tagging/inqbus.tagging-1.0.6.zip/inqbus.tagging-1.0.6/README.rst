
Introduction
============

This module allows automatic keyword tagging of multimedia content with a strong focus on images.

Inqbus.tagging processes metadata of the following keyword sources: Filename/Title, EXIF, IPTC, XMP. Any Plone Object-Type can be processed.

Keywords from Filename
----------------------

The metadata is filtered by configurable filters. For each metadata source there is a filter which can be switched on/off independently.

The filename/title may be filtered by a regular expression you are free to craft. The regular expression enables you to filter, strip, split into words, what you like.
You can decide if you like to have new keywords to be extracted from the title or if you want use only keywords from the title that match existing ones, or both strategies with different regular expressions in parallel.

Keywords from EXIF, IPTC and XMP
--------------------------------

EXIF, IPTC and XMP are filtered firstly by a positive list of tags for each category.

For every tag in a filter can be defined a regular expression and a format string to cut and format the way you like. Lets assume you have metadata tags with the structure "Asimov, Isaac; Bradley, Alex" you can transform them into the Plone tags "Isaac Asimov" and "Alex Bradley" easily.

Since there are lots of possible tags available inqbus.tagging comes with tag import views for each metadata category. Each tag import view allows for opening an arbitrary file in Plone to inspect its metadata and to select and transfer metadata tag names into the tag configuration.

Improved manual tagging of images
---------------------------------

Inqbus.tagging supports manual tagging of images by providing a preview image column in the folder_contents-View. Also inqbus.tagging brings lossless EXIF image auto rotation back to Plone.

Retagging of already uploaded content
-------------------------------------

If you have changed your autotagging config you can use the "retag" Button in the folder_contents-View to rerun the auto tagging on certain objects.

Stabilty
========

This code is work in progress crafted in after hours. It may not be save for production sites, but runs fine in our setup.
We welcome anyone to improve the code.


Requirements
============

* Plone 5
* z3c.forms
* IPTCInfo
* exifread
* jpegtran-cffi (libjpeg8, cython, cffi) for fast and loss less auto rotation.

Note: If not using jpegtran the EXIF auto rotation falls back to PIL. The XMP-Metadata in auto rotated files then is lost since PIL does not respect XMP.
    Also the rotated images are larger and a bit blurred. So we strongly suggest to use jpegtran-cffi.

Installation of jpegtran-cffi
-----------------------------

Building jpegtran-cffi on debian jessie:

aptitude install build-essential python-dev libturbojpeg1-dev libjpeg62-turbo-dev libffi-dev
pip install cffi
pip install jpegtran-cffi

Installation
============

Add inqbus.tagging to your buildout eggs.::

    eggs=\
        ...
        inqbus.tagging


To use inqbus.tagging with `jpegtran-cffi` add inqbus.tagging[jpegtran] to your buildout eggs.::

    eggs=\
        ...
        inqbus.tagging[jpegtran]


`jpegtran-cffi` is used for the rotation of the images. If you do not use it images
will be rotated using `Pillow`. This leads to metadata loss especially xmp-data.

Deinstallation
==============

For removing all stored configurations run the profile `profile-inqbus.tagging:purge`.

Then go to Configuration -> Extensions. Select uninstall inqbus.tagging.


Using inqbus.tagging
====================


Configure Auto-Tagging
----------------------

Go to Configuration -> inqbus.tagging Configuration:

.. image:: https://github.com/collective/inqbus.tagging/raw/master/docs/img/tagging_config.png



Select Tags by Tag Import
-------------------------

To make selecting meta-information more easier, you can use `Inqbus Tagging - Tag Imports`
in Site Setup to select meta-fields.

Therefore select an image and press `ok`. A list of available fields will be displayed
including the value of the selected image as example.

.. image:: https://github.com/collective/inqbus.tagging/raw/master/docs/img/tag_import.png

Select your tags and press ok. All selected tags are added to the list in
`Inqbus Tagging Settings` and can be configured there.

Enable Auto-Tagging for other Contenttypes
------------------------------------------

Register a subscriber like::

    <subscriber
    for="plone.app.contenttypes.content.Image
         zope.lifecycleevent.IObjectCreatedEvent"
    handler="inqbus.tagging.subscriber.title_based.title_to_tag"
    />

for every contenttype you want to tag.

Manage existing Tags
--------------------

For managing existing tags you can use a modified version of `Products.PloneKeywordManager`.

.. image:: https://github.com/collective/inqbus.tagging/raw/master/docs/img/keywordmanager.png

Here you can join tags used for the same content or delete not wanted tags.


Extended Folder_contents-View
=============================

Image Preview
-------------

To make working with Images more easier a preview-column was
added to the `folder_contents`-View and can be selected like all other columns.

.. image:: https://github.com/collective/inqbus.tagging/raw/master/docs/img/folder_contents.png

Retag
-----

To migrate existing objects you can use the `Retag`-Action in the `folder_contents`-View.


Limitations
===========

Processing XMP is done by parsing the RDF:XML-Data structure directly utilizing LXML.
Usually XMP is parsed by tools based on Adobe's XMP-Toolkit which fiddles a lot with the tag values to make them appear
right. There seems to be no Python XMP-Lib out there which does not requires an image file name to process a file.
Even in the underlying C++ Code there appears no good entry point for processing image data from a ZODB-Blob. So we
decided to parse the XMP "by hand" and do without the Adobe corrections. So please be not disappointed if the XMP tags
you have applied to your image by Photoshop 10 years ago may come out a bit askew.

Background
==========

We take part in a small foto group in germany. Our site http://fotogruppe-altenstadt.de presents 20.000+ high
quality images tagged by 2000+ keywords under CC license. Using Plone for a long time we like to give back our knowledge
to the community.
