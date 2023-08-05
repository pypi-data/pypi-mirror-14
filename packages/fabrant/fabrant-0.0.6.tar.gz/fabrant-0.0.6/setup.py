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
    py_modules=['fabrant'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ]
)
