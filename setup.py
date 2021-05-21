#!/usr/bin/env python

from distutils.core import setup

setup(name='nagios-nvidia-smi-plugin',
        version='0.1.0',
        author='Marco Cicala',
        author_email='marco.cicala@e4company.com',
        license="MIT",
        keywords="nagios nvidia smi gpu plugin",
        url='https://github.com/ilciko/nagios-nvidia-smi-plugin',
        description='Nagios plugin to check Nvidia GPU status using nvidia-smi',
        long_description=open('README.txt').read(),
        install_requires=["argparse","nagiosplugin"],
        scripts=["check_nvidiasmi.py"]
)
