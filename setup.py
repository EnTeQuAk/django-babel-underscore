#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.5.1'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


test_requires = [
    'coverage',
    'pytest',
    'pytest-cov>=1.4',
    'pytest-flakes',
    'pytest-pep8',
    'python-coveralls',
]


install_requires = [
    'django>=1.8,<2.0',
    'babel>=1.3',
    'django-babel>=0.5.1',
    'markey>=0.8,<0.9',
]


dev_requires = [
    'flake8>=2.0',
]


setup(
    name='django-babel-underscore',
    version=version,
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
    extras_require={
        'docs': ['sphinx'],
        'tests': test_requires,
        'dev': dev_requires,
    },
    entry_points="""
    [babel.extractors]
    underscore = django_babel_underscore:extract
    """,
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
