# -*- coding: utf-8 -*-

# windows: python setup.py install --boost-dir=../../lib/boost_1.58_win64 --event-engine-include=../../../ --event-engine-lib=../../lib/win64/
# mac: python setup.py install --boost-dir=../../lib/boost_1.58_mac --event-engine-include=../../../ --event-engine-lib=../../lib/mac/
from distutils.version import StrictVersion
from setuptools import (
    Extension,
    find_packages,
    setup,
)

module1 = {'./build/keystone/':['engine.so']}

# setup
setup (name = 'keystone_sdk',
		version = '0.7.14',
		description = 'keystone python SDK for backtesting',
		# package_dir = {'keystone': 'build/keystone'},
		# packages = ['keystone'],
        packages = find_packages('.'),
        package_data = {'keystone': ['engine.cpython-35m-darwin.so', 'engine.so', 'engine.cp35-win_amd64.pyd', 'engine.pyd']},
        install_requires = ['six', 'pandas', 'numpy', 'pyzmq', 'tables'])
        # data_files = [('keystone',['./test.cpp'])])
