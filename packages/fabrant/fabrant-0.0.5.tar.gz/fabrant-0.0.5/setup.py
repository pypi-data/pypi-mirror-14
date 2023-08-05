from setuptools import setup

import fabrant

version = fabrant.__version__


setup(
    name='fabrant',
    version=version,
    description="Easy handling of vagrant hosts within fabric",
    long_description=open("README.rst").read(),
    author='Fabian Schindler',
    author_email='fabian.schindler@eox.at',
    license='MIT',
    url='https://github.com/constantinius/fabrant',
    download_url=(
        'https://github.com/constantinius/fabrant/archive/v%star.gz' % version
    ),
    py_modules=['fabrant'],
)
