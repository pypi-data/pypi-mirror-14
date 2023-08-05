"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import codecs
import os
import re
import sys

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")    

setup(
    name='django-tastypie-simple-api-doc',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=find_version('tastypie_api_doc','__init__.py'),

    description='A Django app to generate a simple and automatic api documentation with Tastypie',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/matheuscas/django-tastypie-simple-api-doc',

    # Author details
    author='Matheus Cardoso',
    author_email='matheus.mcas@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',

        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    # What does your project relate to?
    keywords='django tastypie api documentation automatic',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    # packages=['tastypie_api_doc'],
    package_data={'tastypie_api_doc': ['templates/index.html', 
                                'static/tastypie_api_doc/bower_components/jquery/dist/*.js',
                                'static/tastypie_api_doc/bower_components/semantic/dist/*.js',
                                'static/tastypie_api_doc/bower_components/semantic/dist/*.css',
                                'static/tastypie_api_doc/bower_components/semantic/dist/components/*.js',
                                'static/tastypie_api_doc/bower_components/semantic/dist/components/*.css',
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.ttf',
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.woff',
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.svg',
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.eot'
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.otf'
                                'static/tastypie_api_doc/bower_components/semantic/dist/themes/default/assets/fonts/*.woff2']},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['django-tastypie>=0.12.1','django>=1.8.6'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    zip_safe=False
)