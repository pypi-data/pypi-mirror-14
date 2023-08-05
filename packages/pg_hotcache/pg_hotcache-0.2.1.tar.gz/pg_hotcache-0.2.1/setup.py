from setuptools import setup, find_packages

PACKAGE = "pg_hotcache"
NAME = "pg_hotcache"
DESCRIPTION = "Loading into cache from said PostgreSQL database the tables, which are most frequently scanned."
AUTHOR = "Timur Isanov"
AUTHOR_EMAIL = "tisanov@yahoo.com"
URL = "https://github.com/xtimon/pg_hotcache"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(),
    install_requires=[
        'argparse',
        'psycopg2'
    ],
    entry_points={
        'console_scripts':
            ['pg_hotcache = pg_hotcache.core:main']
        },
    classifiers=[
        'Environment :: Console',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)