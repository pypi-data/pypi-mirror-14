from codecs import open
from os import path

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class CoverageCommand(TestCommand):

    def initialize_options(self):
        super(CoverageCommand, self).initialize_options()
        self.coverage_output = None

    def run_tests(self):

        from coverage import Coverage
        cov = Coverage(branch=True)
        cov.start()

        try:
            super(CoverageCommand, self).run_tests()
        finally:
            cov.stop()
            cov.html_report(directory="covhtml")


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ubjsonstream',
    version='0.0.2',
    description='A library for serializing and async deserializing UBJSON',
    long_description=long_description,
    author='Tomasz Sieprawski',
    author_email='tomasz@sieprawski.eu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='ubjson',
    packages=['ubjsonstream'],
    package_dir={'': 'src'},
    test_suite="test",
    install_requires=[],
    extras_require={
        'test': ['coverage'],
    },
    cmdclass={
        'coverage': CoverageCommand}
)
