from setuptools import setup, find_packages
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = 'Neronet is going to be a framework designed to facilitate the specification, submission, monitoring, control, analysis and management of many different computational experiments in collaboration with computing cluster resource managers and job schedulers such as Slurm'

setup(
    name='neronet',
    version=find_version('neronet', 'version.py'),
    url='http://github.com/smarisa/neronet',
    license='MIT',
    author='The neronet team',
    install_requires=['pyyaml>=3.11'],
    author_email='samuel.marisa@aalto.fi',
    description='A tool for managing multiple computational experiments.',
    long_description=long_description,
    scripts=['bin/nerocli', 'bin/nerogui'],
    packages=['neronet'],
    package_data={'neronet': ['nerokid', 'neromum']},
    platforms='unix',
    zip_safe=True,
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
