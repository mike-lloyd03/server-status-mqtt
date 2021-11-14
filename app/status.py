"""Contains functions for getting the system statuses."""
import platform
from datetime import datetime

import psutil


def get_hostname():
    """Returns the hostname of the machine."""
    return platform.uname().node


def get_disk_use_percent(path):
    """Returns the disk usage of the host machine root directory in MB."""
    disk_use = psutil.disk_usage(path).percent
    return round(disk_use, 1)


def get_processor_use(interval):
    """Returns the cpu usage of the host machine over the given interval in seconds."""
    proc_use = psutil.cpu_percent(interval=interval)
    return round(proc_use, 1)


def get_processor_temperature():
    """Returns the package id temperature of the host machine in °C."""
    proc_temp = psutil.sensors_temperatures()["coretemp"][0].current
    return round(proc_temp, 1)


def get_memory_use():
    """Returns the memory usage of the host machine in MB."""
    virt_mem = psutil.virtual_memory()
    return round(virt_mem.used / 1024 ** 2, 1)


def get_last_boot():
    """Returns the boot time of the host machine."""
    boot_time = psutil.boot_time()
    last_boot = datetime.fromtimestamp(boot_time)
    return last_boot.strftime("%Y-%m-%dT%H:%M:%S")
