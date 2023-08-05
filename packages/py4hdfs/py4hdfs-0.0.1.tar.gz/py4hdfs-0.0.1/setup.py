from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='py4hdfs',

    version='0.0.1',

    description='Fast Queries to HDFS',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/vishalkuo/py4hdfs',
    download_url='https://github.com/vishalkuo/py4hdfs/tarball/v0.0.1',
    # Author details
    author='Vishal Kuo',
    author_email='me@vishalkuo.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7'
    ],

    keywords='hadoop hdfs webhdfs',


    packages=find_packages(),

    install_requires=['requests', 'cement'],

   
    package_data={
        'config': ['config.ini'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pydfs=pydfs.py',
        ],
    },
)