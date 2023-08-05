# -*- coding: utf-8 -*-

import os
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requires = [
    'Flask==0.10.1',
    'PyYAML==3.11',
    'matterhook==0.1',
    'py-trello==0.4.3',
    'python-slugify==1.2.0',
]

tests_require = []

setup(
    name='matterllo',
    version='0.1',
    author='Lujeni',
    author_email='julien@thebault.co',
    description='Simple integration between Trello and Mattermost',
    long_description=read('README.rst'),
    url='https://github.com/lujeni/matterllo',
    download_url='https://github.com/lujeni/matterllo/tags',
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    extra_requires={},
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
