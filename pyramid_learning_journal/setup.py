"""Setup for Pyramid Learning Journal."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'ipython',
    'pyramid_ipython',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'webtest',
    'psycopg2'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    'tox'
]

setup(
    name='pyramid_learning_journal',
    version='0.0',
    description='learning_journal',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = pyramid_learning_journal:main',
        ],
        'console_scripts': [
            'initializedb = pyramid_learning_journal.scripts.initializedb:main',
        ],
    },
)
