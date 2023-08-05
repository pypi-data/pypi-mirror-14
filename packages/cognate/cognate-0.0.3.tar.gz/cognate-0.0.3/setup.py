"""The setuptools setup file."""
from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='cognate',
    version=version,
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='https://github.com/neoinsanity/cognate',
    license='Apache License 2.0',
    description='From the same Root.',
    long_description=long_description,
    packages=['cognate',],
    install_requires=[],
    include_package_data = True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
    ]
)
