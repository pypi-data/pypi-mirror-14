# coding: utf-8


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='skymonitor',

    version='0.0.3',

    description='skyline monitor',
    long_description=long_description,

    url='https://github.com/xiachufang/skyline',

    # Author details
    author='liuweibo',
    author_email='liuweibo@xiachufang.com',
    packages=find_packages(exclude=['tmp', 'test']),

    entry_points={
        "console_scripts": ["skyline = skyline_client:main", "skymonitor = skyline_client:main",
                            "skygather = skyline_client:gather_main"]
    },

    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['gevent', 'simplejson', 'pyzmq', 'requests', 'jsonschema',
                      'pyinotify', 'six', 'ply', 'functools32'],
    keywords='skyline monitor',
    include_package_data=True
)
