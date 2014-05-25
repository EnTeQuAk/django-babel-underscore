#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'pytest-flakes',
    'pytest-pep8',
    'python-coveralls',
]


install_requires = [
    'Django>=1.4,<1.8',
    'Babel>=1.3',
    'django-babel>=0.3.4',
    'markey>=0.4',
]


dev_requires = [
    'flake8>=2.0',
    'invoke',
    'twine'
]


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)



setup(
    name='django-babel-underscore',
    version='0.1.0',
    description='Implements a underscore extractor for django-babel.',
    long_description=read('README.rst') + u'\n\n' + read('HISTORY.rst'),
    author='Christopher Grebs',
    author_email='cg@webshox.org',
    url='https://github.com/EnTeQuAk/django-babel-underscore',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    tests_require=test_requires,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    extras_require={
        'docs': ['sphinx'],
        'tests': test_requires,
        'dev': dev_requires,
    },
    zip_safe=False,
    license='BSD',
    keywords='django-babel-underscore',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
