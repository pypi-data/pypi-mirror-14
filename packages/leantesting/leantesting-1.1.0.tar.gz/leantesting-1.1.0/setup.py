from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='leantesting',

    version='1.1.0',

    description='Lean Testing Python SDK',
    long_description=long_description,

    url='https://github.com/crowdsourcedtesting/leantesting-python',

    author='Lean Testing',
    author_email='support@crowdsourcedtesting.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: Other/Proprietary License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='development api bug tracker',

    # packages = find_packages(exclude = ['tests']),
    packages=find_packages(),

    install_requires=['pycurl'],

    extras_require={
        'test': ['unittest2']
    },

    include_package_data=True
)
