# See https://github.com/NHSDigital/rap-community-of-practice/blob/main/docs/implementing_RAP/example-pipeline.md

from setuptools import find_packages, setup

setup(
    name='smoking-drinking-and-drug-use-rap',
    packages=find_packages(),
    version='0.1.0',
    description='To create publication ...',
    author='NHS_England',
    license='',
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
)
