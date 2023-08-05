# -*- coding: utf-8 -*-
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import io
import os

from setuptools import setup


# To use a consistent encoding
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf-8')
    ) as fp:
        return fp.read().rstrip()


here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='msbackup',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=read(os.path.join(here, 'msbackup', 'VERSION')),

    description='Generic backup utility.',
    long_description=read(os.path.join(here, 'README.rst')),

    # The project's main home page.
    url='https://github.com/Aleksei-Badyaev/msbackup',

    # Author details
    author='Aleksei Badyaev',
    author_email='aleksei.badyaev@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Author's natural language.
        'Natural Language :: Russian',

        'Operating System :: POSIX :: Linux',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        # Topic to locate application.
        'Topic :: System :: Archiving :: Backup',
    ],

    # What does your project relate to?
    keywords='linux backup administration',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['msbackup'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['python-dateutil', 'six'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={'dev': ['check-manifest',
                            'coverage',
                            'ipdb',
                            'twine',
                            'unittest-xml-reporting']},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'msbackup': ['VERSION']},
    include_package_data=True,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('/etc/msbackup', ['conf/msbackup.config'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'msbackup=msbackup.msbackup:main',
        ],
    },
)
