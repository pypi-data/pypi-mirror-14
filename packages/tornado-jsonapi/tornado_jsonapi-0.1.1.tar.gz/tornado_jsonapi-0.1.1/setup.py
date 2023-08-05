#!/usr/bin/env python3
# vim: set fileencoding=utf8 :

from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import sys

import tornado_jsonapi


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='tornado_jsonapi',
    version=tornado_jsonapi.__version__,
    url='http://github.com/lockie/tornado_jsonapi',
    license='MIT License',
    author='Andrew Kravchuk',
    author_email='awkravchuk@gmail.com',
    install_requires=[
        'accept==0.1.0',
        'jsl==0.2.2',
        'jsonpatch==1.12',
        'jsonpointer==1.10',
        'jsonschema==2.3.0',
        'python_jsonschema_objects==0.0.15',
        'python-status==1.0.1',
        'tornado>=4.2',
    ],
    extras_require={
        'sqlalchemy': ['SQLAlchemy==1.0.12', 'alchemyjsonschema==0.2.2'],
        'dbapi2': ['antiorm==1.2.0']
    },
    tests_require=['pytest==2.9.1', 'pytest-pep8==1.0.6',
        'WebTest==2.0.20', 'loremipsum==1.0.5'],
    cmdclass={'test': PyTest},
    description='Framework providing REST JSON API to Tornado web server',
    long_description=read('README.rst', 'Changelog.rst'),
    packages=['tornado_jsonapi'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    keywords='tornado JSON API REST SQLAlchemy DBAPI',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
)
