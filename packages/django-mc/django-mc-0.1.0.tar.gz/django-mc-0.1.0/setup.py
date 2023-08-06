# -*- coding: utf-8 -*-
import codecs
import re
from os import path
from distutils.core import setup
from setuptools import find_packages


def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding='utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-mc',
    version=find_version('django_mc', '__init__.py'),
    author=u'David Danier',
    author_email='david.danier@team23.de',
    packages=find_packages(
        exclude=['tests', 'tests.*']),
    include_package_data=True,
    url='https://git.team23.de/team23/django_mc',
    license='BSD licence, see LICENSE file',
    description=(
        "A foundational structure for CMS systems. Helps you to create "
        "page models, components (individual content blocks to build up "
        "pages) and to attach components to pages."
    ),
    long_description=u'\n\n'.join((
        read('README.rst'),
        read('CHANGES.rst'))),
    install_requires=[
        'django_deferred_polymorph',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
)
