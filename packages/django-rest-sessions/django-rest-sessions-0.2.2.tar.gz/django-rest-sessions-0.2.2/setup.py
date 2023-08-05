import os

from distutils.core import Command
import setuptools
from setuptools.command.test import test


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


def get_version():
    with open('VERSION', 'r') as f:
        return f.readline().rstrip().split('=')[1]


def get_tarball_filename():
    return 'django-rest-sessions-{}.tar.gz'.format(get_version())


class TestXMLOutput(test):
    @staticmethod
    def _resolve_as_ep(val):
        from xmlrunner import XMLTestRunner
        if val is None:
            return XMLTestRunner(output='test-reports')
        return test._resolve_as_ep(val)

packages = ['rest_sessions']

setup_kwargs = dict(
    name='django-rest-sessions',
    version=get_version(),
    description= "Rest Session Backend For Django",
    long_description=read("README.rst"),
    keywords='django, sessions,',
    author='Hodur Sigurdor Heidarsson',
    author_email='hodur@temposoftware.com',
    url='https://stash.temposoftware.com/projects/TMC/repos/django-rest-sessions/browse',
    license='MIT',
    packages=packages,
    zip_safe=False,
    install_requires=['Django >= 1.8', 'requests>=2.7.0'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    test_suite='tests',
    cmdclass={
        'xml_test': TestXMLOutput
    }
)

setuptools.setup(**setup_kwargs)
