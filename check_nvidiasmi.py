#!/usr/bin/env python

import argparse, logging, nagiosplugin, subprocess, xml.etree.ElementTree

class Utilization(nagiosplugin.Resource):

    def __init__(self):
        nvidia_smi_proc = subprocess.Popen(["/usr/bin/nvidia-smi", "-q", "-x"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nvidia_smi_proc_out, nvidia_smi_proc_err = nvidia_smi_proc.communicate()
        if nvidia_smi_proc.returncode > 0:
            raise Exception(nvidia_smi_proc_err)
        self.nvidia_smi_xml_root = xml.etree.ElementTree.fromstring(nvidia_smi_proc_out)

    def probe(self):
        for gpu in self.nvidia_smi_xml_root.iter('gpu'):
            utilization = gpu.find('utilization')
            gpuUtilization = float(utilization.find('gpu_util').text.strip(' %'))
            yield nagiosplugin.Metric('gpuutil', gpuUtilization, '%')
            
            memUtilization = float(utilization.find('memory_util').text.strip(' %'))
            yield nagiosplugin.Metric('memutil', memUtilization, '%')

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description='Nagios plugin to check Nvidia GPU status using nvidia-smi')

    argp.add_argument('-w', '--gpu_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-c', '--gpu_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')
    
    argp.add_argument('-W', '--mem_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-C', '--mem_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')
    
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase verbosity (use up to 3 times)')

    args=argp.parse_args()

    check = nagiosplugin.Check(
            Utilization(),
            nagiosplugin.ScalarContext('gpuutil', args.gpu_warning, args.gpu_critical),
            nagiosplugin.ScalarContext('memutil', args.mem_warning, args.mem_critical)
            )
    check.main(verbose=args.verbose)

if __name__ == "__main__":
    main()