from os.path import abspath, dirname, join
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
from sys import exit


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        exit(errno)


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-repositories',
    version='0.1.3',
    description='Functions for managing code repositories',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='http://invisibleroads.com',
    keywords='invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'invisibleroads-macros',
        'pytz',
        'requests',
        'tzlocal',
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest})
