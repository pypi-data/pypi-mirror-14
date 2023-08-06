# coding=utf-8
import sys
from setuptools import setup, find_packages

NAME = 'django-generic-tagging'
VERSION = '0.0.2'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name=NAME,
    version=VERSION,
    description='A generic tagging plugin for Django',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django tagging tag',
    author='giginet',
    author_email='giginet.net@gmail.com',
    url='https://github.com/giginet/%s' % NAME,
    download_url='https://github.com/giginet/%s/tarball/master' % NAME,
    license='MIT',
    packages=find_packages(exclude=('tests', 'example')),
    include_package_data=True,
    package_data={
        '': ['README.rst',
             'requirements-test.txt'],
    },
    zip_safe=False,
    test_suite='runtests.run_tests',
    tests_require=readlist('requirements-test.txt'),
    **extra
)
