from setuptools import setup, find_packages
import os

version = '1.0.6'

setup(name='inqbus.tagging',
      version=version,
      description="Auto tagging for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python :: 2 :: Only",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Telecommunications Industry",
          "Topic :: Multimedia :: Graphics :: Presentation"
        ],
      keywords='Plone, tagging, keywords, autorotation, EXIF, IPTC, XMP, image, inqbus',
      author='Dr. Volker Jaenisch <volker.jaenisch@inqbus.de>, Sandra Rum <sandra.rum@inqbus.de>',
      author_email='volker.jaenisch@inqbus.de',
      url='https://github.com/collective/inqbus.tagging',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['inqbus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Pillow',
          # -*- Extra requirements: -*-
          'Products.PloneKeywordManager',
          'IPTCInfo',
          'exifread',
          'plone.autoform',
          'collective.z3cform.datagridfield'
      ],
      extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
        'jpegtran': [
            'cffi',
            'jpegtran-cffi',
        ]
        },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      )
