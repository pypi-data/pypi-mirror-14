# coding=utf-8
import os

from setuptools import setup
from setuptools.command.test import test as TestCommand
import omnilog
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


with open(here + '/README.md') as r:
    readme_html = r.read()
    readme_plain = re.sub(r"<([0-9a-zA-Z/]*)>", "", readme_html)

with open(here + '/requirements.txt') as req:
    reqs = req.read().splitlines()

setup(
    name='omnilog',
    version=omnilog.__version__,
    download_url='https://github.com/sandboxwebs/omnilog/tarball/' + omnilog.__version__,
    url='https://github.com/sandboxwebs/omnilog',
    license='GPLV3',
    author='Eloy (sbw)',
    install_requires=reqs,
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    author_email='eloy@sandboxwebs.com',
    description='A remote log watcher daemon that uses ssh, and multithreaded design.',
    long_description=readme_plain,
    packages=['omnilog'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Freely Distributable',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring'
    ],
    include_package_data=True,
    platforms='any',
    scripts=['omnilog/omnilogd.py']
)
