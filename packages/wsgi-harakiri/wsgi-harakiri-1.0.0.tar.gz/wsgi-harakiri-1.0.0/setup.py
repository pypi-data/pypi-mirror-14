#!/usr/bin/env python
import os
import re
import sys

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('wsgi_harakiri')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("rm -rf .eggs/ build/ dist/")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a v%s -m 'Version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='wsgi-harakiri',
    version=version,
    author="Adam Johnson",
    author_email='me@adamj.eu',
    url='https://github.com/adamchainz/wsgi-harakiri',
    description="WSGI Middleware that implements a customizable 'harakiri' like  uWSGI",
    long_description=readme + '\n\n' + history,
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    install_requires=[
        'six',
    ],
    license='ISCL',
    include_package_data=True,
    keywords='WSGI, Harakiri',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
)
