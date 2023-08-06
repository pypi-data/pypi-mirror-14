#!/usr/bin/env python

from distutils.core import setup

setup(name='swarmclient',
    version='1.2',
    description='swarmclient library',
    author='mindsensors.com',
    author_email='support@mindsensors.com',
    url='http://www.mindsensors.com',
    py_modules=['swarmclient'],
	data_files=[('/etc/init.d', ['SwarmServer.sh']),
	('/usr/local/bin', ['swarmserver'])],
    install_requires=['ws4py'],
    )
