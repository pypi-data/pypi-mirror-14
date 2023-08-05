import os
import sys

from collections import OrderedDict
from sh import uname


def find_cpuinfo(markers):
    # no support for non-linux systems
    if os.path.exists('/proc/cpuinfo'):
        content = open('/proc/cpuinfo', 'rb').read()
        for marker, return_value in list(markers.items()):
            if marker in content:
                return return_value


def get_device_meta():
    return {
        'distro': get_distro(),
        'model': get_model(),
        'system': get_system(),
    }


def get_distro():
    """
    Returns the device distribution

    :return string: device distribution
    """
    distro = None

    if os.path.exists('/etc/linino'):
        return 'linino'

    result = uname('-a')
    if 'Darwin Kernel Version' in result:
        return 'osx'

    issue_path = '/etc/issue'
    if os.path.exists(issue_path):
        with open(issue_path, 'rb') as fh:
            content = fh.read().lower()
            for _distro in ('raspbian', 'arch'):
                if _distro in content:
                    distro = _distro
                    break

    return distro


def get_model():
    systems = OrderedDict((
        ('Arduino Yun', 'yun'),
        ('BCM2708', '1'),
        ('BCM2709', '2'),
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform


def get_system():
    systems = OrderedDict((
        ('Arduino Yun', 'arduino'),
        ('BCM270', 'raspberrypi'),  # note this will match BCM2708 (rpi) and BCM2709 (rpi2)
    ))
    cpuinfo = find_cpuinfo(systems)
    if cpuinfo:
        return cpuinfo

    if sys.platform == 'darwin':
        return sys.platform

    if 'linux' in sys.platform:
        return 'linux'
