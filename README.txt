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
		                          [-t RANGE] [-T RANGE] [-d DEVICE] [-v]

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
		  -t RANGE, --gputemp_warning RANGE
		                        warning if threshold is outside RANGE
		  -T RANGE, --gputemp_critical RANGE
		                        critical if threshold is outside RANGE
		  -d DEVICE, --device DEVICE
		                        Device ID (starting from 0)
		  -v, --verbose         increase verbosity (use up to 3 times)

Releases
========
0.4.0 - May 06, 2015: Specify device to check, and added check for temperature; thanks @gslongo!
0.2.0 - Jan 16, 2013: Initial release

Develop
=======
Fork me on `Github <https://github.com/FastSociety/nagios-nvidia-smi-plugin>`_.
