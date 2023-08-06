# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

REQUIRES = ["cryptography==1.0", "google-api-python-client==1.4.2",
            "oauth2client==1.5.2", "pycrypto==2.6.1", "pyopenssl==0.15.1",
            "arrow==0.6.0"]

setup(
    name='gdrive-client',
    version='1.0.0',
    packages=[
        'gdrive',
    ],
    author='Suraj Arya',
    author_email='suraj@loanzen.in',
    description='An simpler lightweight  version of calling google drive apis if you only want to list/upload files',
    url='https://github.com/loanzen/gdrive-client',
    license='MIT',

    install_requires=REQUIRES,
)
