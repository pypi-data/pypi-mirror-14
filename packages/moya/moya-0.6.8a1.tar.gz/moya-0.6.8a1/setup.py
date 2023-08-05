#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = "0.6.8a1"

# Don't forget to update version in moya/__init__.py

classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4"
]

long_desc = """Web development framework"""

setup(
    name='moya',
    version=VERSION,
    description="web development platform",
    long_description=long_desc,
    zip_safe=False,
    license="MIT",
    author="Will McGugan",
    author_email="will@willmcgugan.com",
    url="http://www.moyaproject.com",

    entry_points={
        "console_scripts": [
            'moya = moya.command.app:main',
            'moya-pm = moya.command.moyapi:main',
            'moya-srv = moya.command.moyasrv:main',
            'moya-doc = moya.command.moyadoc:main'
        ]
    },
    scripts=[
        'scripts/moya-workon',
    ],
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={'': ['_*', 'docs/*']},

    classifiers=classifiers,
    install_requires=[
        'pyparsing >= 2.0.7',
        'webob>=1.5,<2',
        'sqlalchemy',
        'pytz',
        'pygments',
        'fs >= 0.5.4',
        'iso8601',
        'babel==1.3',
        'postmarkup',
        'polib',
        'pillow >= 3.1.1',
        'pymysql',
        'passlib',
        'commonmark >= 0.6.3',
        'requests',
        'lxml',
        'colorama',
        'premailer',
        'watchdog',
        'bleach',
        'beautifulsoup4'
    ],
    extras_require={
        ':sys_platform=="linux2" or sys_platform=="linux3"': ["pyinotify"],
        'dev': ['notify2']
    },
    setup_requires=["setuptools_git >= 0.3"]
)
