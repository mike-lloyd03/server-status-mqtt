# Server Status

This Python script sends machine status messages to an MQTT broker.

Currently, this script supports sending the following machine status information:
- Processor use (in percentage)
- Processor temperature
- RAM use (in megabytes)
- Disk use (in percentage, multiple disk paths can be specified)
- Last boot time

### Requirements
- Python 3
- `make`

### Installation
Clone this repo somewhere on the host machine and run the following in that directory.

```bash
make
```

This will create the Python virtual environment and install the required dependencies.

You can then install a systemd service and enable it on your system. This will run the script and set it to persist through reboots.

```bash
make deploy
systemctl enable --now server-status-mqtt.service
```

### Usage
Messages will be published with the following topics:

`server-status/<hostname_of_machine>/processor_use`
`server-status/<hostname_of_machine>/processor_temperature`
`server-status/<hostname_of_machine>/memory_use`
`server-status/<hostname_of_machine>/disk_use_percent_disk<number>`
`server-status/<hostname_of_machine>/last_boot`

(`disk_use_percent_disk<number>` will be numbered in the order in which the paths are specified in `config.py`.)

### Configuration
You will need to create a `.env` file in the root directory of the repo with three values set:

```bash
MQTT_USERNAME=<username>
MQTT_PASSWORD=<password>
MQTT_BROKER=<broker_host>
```

These are the connection details for your MQTT broker.

Boolean values can be set in `config.py` to determine which messages you would like to be sent.

Additionally, you can specify which disk paths are to be used for calculating disk use percent with the tuple `DISK_PATHS`. The default is `/`, the root directory of the system. Specifying a subdirectory of `/` which is on the same disk partition will return the same value as `/`.

To find the paths to available partitions on your system, run `df` and look at the "Mounted on" column:

```
Filesystem     1K-blocks      Used Available Use% Mounted on
dev             32847328         0  32847328   0% /dev
run             32857084      1992  32855092   1% /run
/dev/nvme0n1p2 888837712 661256828 182356664  79% /
tmpfs           32857084    428040  32429044   2% /dev/shm
tmpfs           32857088     64836  32792252   1% /tmp
/dev/nvme0n1p1    306572       296    306276   1% /boot/efi
tmpfs            6571416       360   6571056   1% /run/user/1000
```

### Home Assistant Integration
These MQTT messages can be used to create custom sensors in Home Assistant.

The following template can be added to you `configuration.yaml` file.

```yaml
  - platform: mqtt
    name: "Server1 disk use percent"
    state_topic: "server_status/server1/disk_use_percent_disk1"
    unit_of_measurement: "%"
    icon: mdi:harddisk
```

