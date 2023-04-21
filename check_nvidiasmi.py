#!/usr/bin/env python

import argparse
import subprocess
import xml.etree.ElementTree

import nagiosplugin


class Utilization(nagiosplugin.Resource):
    def __init__(self, args):
        self.args = args
        nvidia_smi_proc = subprocess.Popen(
            ["/usr/bin/nvidia-smi", "-q", "-x", "-i", args.device],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        nvidia_smi_proc_out, nvidia_smi_proc_err = nvidia_smi_proc.communicate()
        if nvidia_smi_proc.returncode > 0:
            raise Exception(nvidia_smi_proc_err)
        self.nvidia_smi_xml_root = xml.etree.ElementTree.fromstring(nvidia_smi_proc_out)

    def probe(self):
        if self.nvidia_smi_xml_root is None:
            raise Exception("Failed to decode nvidia-smi output")

        # Add suffic to GPU specific metrics to allow for proper multi-gpu support
        # Otherwise only the metrics of the last GPU will be reported 
        count = 0

        yield nagiosplugin.Metric(
            "gpucount", int(self.nvidia_smi_xml_root.find("attached_gpus").text), ""
        )

        for gpu in self.nvidia_smi_xml_root.iter("gpu"):
            utilization = gpu.find("utilization")
            gpuUtilization = float(utilization.find("gpu_util").text.strip(" %"))
            yield nagiosplugin.Metric(f"gpuutil{count}", gpuUtilization, "%")

            memUtilization = float(utilization.find("memory_util").text.strip(" %"))
            yield nagiosplugin.Metric(f"memutil{count}", memUtilization, "%")

            temperature = gpu.find("temperature")
            gpuTemp = float(temperature.find("gpu_temp").text.strip(" C"))
            yield nagiosplugin.Metric(f"gpuTemp{count}", gpuTemp, "")


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(
        description="Nagios plugin to check Nvidia GPU status using nvidia-smi"
    )

    argp.add_argument(
        "--count_warning",
        metavar="RANGE",
        default=0,
        help="warning if threshold is outside RANGE",
    )
    argp.add_argument(
        "--count_critical",
        metavar="RANGE",
        default=0,
        help="critical if threshold is outside RANGE",
    )

    argp.add_argument(
        "-w",
        "--gpu_warning",
        metavar="RANGE",
        default=0,
        help="warning if threshold is outside RANGE",
    )
    argp.add_argument(
        "-c",
        "--gpu_critical",
        metavar="RANGE",
        default=0,
        help="critical if threshold is outside RANGE",
    )

    argp.add_argument(
        "-W",
        "--mem_warning",
        metavar="RANGE",
        default=0,
        help="warning if threshold is outside RANGE",
    )
    argp.add_argument(
        "-C",
        "--mem_critical",
        metavar="RANGE",
        default=0,
        help="critical if threshold is outside RANGE",
    )

    argp.add_argument(
        "-t",
        "--gputemp_warning",
        metavar="RANGE",
        default=0,
        help="warning if threshold is outside RANGE",
    )
    argp.add_argument(
        "-T",
        "--gputemp_critical",
        metavar="RANGE",
        default=0,
        help="critical if threshold is outside RANGE",
    )

    argp.add_argument("-d", "--device", default="0", help="Device ID (starting from 0)")

    argp.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity (use up to 3 times)",
    )

    args = argp.parse_args()

    check = nagiosplugin.Check(
        Utilization(args),
        nagiosplugin.ScalarContext("gpucount", args.count_warning, args.count_critical),
        nagiosplugin.ScalarContext("gpuutil", args.gpu_warning, args.gpu_critical),
        nagiosplugin.ScalarContext("memutil", args.mem_warning, args.mem_critical),
        nagiosplugin.ScalarContext(
            "gpuTemp", args.gputemp_warning, args.gputemp_critical
        ),
    )
    check.main(verbose=args.verbose)


if __name__ == "__main__":
    main()
