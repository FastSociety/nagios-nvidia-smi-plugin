#!/usr/bin/env python

import argparse, logging, nagiosplugin, subprocess, xml.etree.ElementTree

class Utilization(nagiosplugin.Resource):

    def __init__(self, args):
        self.args = args
        nvidia_smi_proc = subprocess.Popen(["/usr/bin/nvidia-smi", "-q", "-x", "-i", args.device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            
            temperature = gpu.find('temperature')
            gpuTemp = float(temperature.find('gpu_temp').text.strip(' C'))
            yield nagiosplugin.Metric('gpuTemp', gpuTemp, '')

            fan_speed = float(gpu.find('fan_speed').text.strip(' %'))
            yield nagiosplugin.Metric('fan_speed', fan_speed, '')

            link_widths = gpu.find('link_widths')
            current_link_width = float(link_widths.find('current_link_width').text.strip(''))
            yield nagiosplugin.Metric('current_link_width', current_link_width, '')

            single_bit = gpu.find('single_bit')
            ecc_single_bit = float(single_bit.find('total').text.strip(''))
            yield nagiosplugin.Metric('ecc_single_bit', ecc_single_bit, '')

            double_bit = gpu.find('double_bit')
            ecc_double_bit = float(double_bit.find('total').text.strip(''))
            yield nagiosplugin.Metric('ecc_double_bit', ecc_double_bit, '')

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description='Nagios plugin to check Nvidia GPU status using nvidia-smi')

    argp.add_argument('-g', '--gpu_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-G', '--gpu_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')
    
    argp.add_argument('-m', '--mem_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-M', '--mem_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')
 
    argp.add_argument('-t', '--gputemp_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-T', '--gputemp_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')

    argp.add_argument('-f', '--fan_speed_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-F', '--fan_speed_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')

    argp.add_argument('-l', '--link_widths_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-L', '--link_widths_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')

    argp.add_argument('-sb', '--ecc_single_bit_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-SB', '--ecc_single_bit_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')

    argp.add_argument('-db', '--ecc_double_bit_warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-DB', '--ecc_double_bit_critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')

    argp.add_argument('-d', '--device', default="0",
                      help='Device ID (starting from 0)')
  
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase verbosity (use up to 3 times)')

    args=argp.parse_args()

    check = nagiosplugin.Check(
            Utilization(args),
            nagiosplugin.ScalarContext('gpuutil', args.gpu_warning, args.gpu_critical),
            nagiosplugin.ScalarContext('memutil', args.mem_warning, args.mem_critical),
            nagiosplugin.ScalarContext('gpuTemp', args.gputemp_warning, args.gputemp_critical),
            nagiosplugin.ScalarContext('fan_speed', args.fan_speed_warning, args.fan_speed_critical),
            nagiosplugin.ScalarContext('current_link_width', args.link_width_warning, args.link_width_critical),
            nagiosplugin.ScalarContext('ecc_single_bit', args.ecc_single_bit_warning, args.ecc_single_bit_critical),
            nagiosplugin.ScalarContext('ecc_double_bit', args.ecc_double_warning, args.ecc_double_critical)
            )
    check.main(verbose=args.verbose)

if __name__ == "__main__":
    main()
