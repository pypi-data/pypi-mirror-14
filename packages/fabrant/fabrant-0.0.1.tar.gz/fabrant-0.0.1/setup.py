from setuptools import setup

import fabrant


setup(
    name='fabrant',
    version=fabrant.__version__,
    description="Easy handling of vagrant hosts within fabric",
    long_description=open("README.rst").read(),
    author='Fabian Schindler',
    author_email='fabian.schindler@eox.at',
    url='https://github.com/constantinius/fabrant',
    py_modules=['fabrant'],
)
