========================
Nagios Nvidia-Smi Plugin
========================

This plugin for checks Nvidia GPU stats via the nvidia-smi executable provided
by nvidia-current.

Setup
=====
1. pip install nagios-nvidia-smi-plugin
2. /usr/local/bin/check_nvidiasmi.py -h::

		usage: check_nvidiasmi.py [-h] [-w RANGE] [-c RANGE] [-W RANGE] [-C RANGE]
		                          [-v]
		
		Nagios plugin to check Nvidia GPU status using nvidia-smi
		
		optional arguments:
		  -h, --help            show this help message and exit
		  -w RANGE, --gpu_warning RANGE
		                        warning if threshold is outside RANGE
		  -c RANGE, --gpu_critical RANGE
		                        critical if threshold is outside RANGE
		  -W RANGE, --mem_warning RANGE
		                        warning if threshold is outside RANGE
		  -C RANGE, --mem_critical RANGE
		                        critical if threshold is outside RANGE
		  -v, --verbose         increase verbosity (use up to 3 times)

Releases
========
0.2.0 - Jan 16, 2013: Initial release

Develop
=======
Fork me on `Github <https://github.com/FastSociety/nagios-nvidia-smi-plugin>`_.