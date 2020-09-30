#!/usr/bin/env python

from setuptools import setup

setup(
    name='ipmitools',
    packages=['ipmi'],
    version='0.4',
    description='Run ipmitool commands on consoles',
    author='Raghu Udiyar',
    author_email='raghusiddarth@gmail.com',
    url='https://github.com/raags/ipmitool',
    download_url='https://github.com/raags/ipmitool/tarball/0.4',
    install_requires=['pexpect', 'argparse'],
    entry_points={
        'console_scripts': [
            'ipmitool.py=ipmi.ipmicli:main'
        ],
    },
)
