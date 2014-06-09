#!/usr/bin/env python

from setuptools import setup

setup(name='ipmitools',
      version='0.2.0',
      description='Run ipmitool commands on consoles',
      author='Raghu Udiyar',
      author_email='raghusiddarth@gmail.com',
      url='github.com/raags/ipmitool',
      install_requires=['pexpect', 'argparse'],
      packages=['ipmi'],
      entry_points = {
        'console_scripts': [
        'ipmitool.py=ipmi.ipmi_cli:main' 
        ],
      },
     )
