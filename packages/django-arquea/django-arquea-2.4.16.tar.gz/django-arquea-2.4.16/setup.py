# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages
import codecs, os

version = '2.4.16'
"""
zest.releaser available commands
prerelease: asks you for a version number (defaults to the current version minus a 'dev' or so) with this new version
number and offers to commit those changes to subversion
release: copies the the trunk or branch of the current checkout and creates a version control tag of it. Makes a
checkout of the tag in a temporary directory. Offers to register and upload a source dist of this package to
PyPI (Python Package Index).
postrelease: asks you for a version number (gives a sane default), adds a development marker to it, updates the
setup.py or version.txt and the CHANGES/HISTORY/CHANGELOG file with this and offers to commit those changes to
version control.
fullrelease: all of the above in order.

"""

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))

setup(
    name='django-arquea',
    version=version,
    description="Sistema administrativo do ANSP",
    long_description=long_description,
    keywords='',
    author='NARA',
    author_email='noc@ansp.br',
    url='http://www.ansp.br',
    license='',
    packages=find_packages(exclude=['ez_setup']),
    # namespace_packages = [''],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'django<1.10',
        'django-import-export',
        'django-tinymce',
        'django-ckeditor',
        'django-treemenus2',
        'django-weasyprint',
        'django-localflavor',
        'python-dateutil',
        'python-magic',
        'xhtml2pdf',
        'pyyaml',
        'ipaddress',
        'pillow',
        'pypdf',
        'reportlab',
    ]
)
