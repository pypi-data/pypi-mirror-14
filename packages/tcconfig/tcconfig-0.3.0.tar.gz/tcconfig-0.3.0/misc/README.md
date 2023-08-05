# Traffic control
## Network
Traffic control can be specified network to apply to:

- Outgoing/Incoming packets
- Certain IP address/network and port

## Parameters
The following parameters can be set of network interfaces.

- Network bandwidth [G/M/K bps]
- Network latency [milliseconds]
- Packet loss rate [%]


# Installation
## Install via pip
tcconfig canbe installed via [pip](https://pip.pypa.io/en/stable/installing/) (Python package manager).

```console
sudo pip install tcconfig
```


# Basic usage
Outgoing packet traffic control settings are as follows

## Set traffic control (tcset)
tcset is a command to impose traffic control to a network interface (device).

### tcset help
```console
usage: tcset [-h] [--version] [--logging] [--stacktrace] [--debug | --quiet]
             --device DEVICE [--direction {outgoing,incoming}] [--rate RATE]
             [--delay DELAY] [--loss LOSS] [--network NETWORK] [--port PORT]
             [--overwrite]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               for debug print.
  --quiet               suppress output of execution log message.

Miscellaneous:
  --logging             output execution log to a file (tcset.log).
  --stacktrace          display stack trace when an error occurred.

Traffic Control:
  --device DEVICE       network device name (e.g. eth0)
  --direction {outgoing,incoming}
                        direction of network communication that impose traffic
                        control. default=outgoing
  --rate RATE           network bandwidth [K|M|G bps]
  --delay DELAY         round trip network delay [ms] (default=0)
  --loss LOSS           round trip packet loss rate [%] (default=0)
  --network NETWORK     destination network of traffic control
  --port PORT           destination port of traffic control
  --overwrite           overwrite existing settings
```

### e.g. Set a limit on bandwidth up to 100Kbps
```console
# tcset --device eth0 --rate 100k
```

### e.g. Set 100ms network delay
```console
# tcset --device eth0 --delay 100
```

### e.g. Set 0.1% packet loss
```console
# tcset --device eth0 --loss 0.1
```

### e.g. All of the above at onece
```console
# tcset --device eth0 --rate 100k --delay 100 --loss 0.1
```

### e.g. Specify the IP address of traffic control
```console
# tcset --device eth0 --delay 100 --network 192.168.0.10
```

### e.g. Specify the IP network and port of traffic control
```console
# tcset --device eth0 --delay 100 --network 192.168.0.0/24 --port 80
```


## Delete traffic control (tcdel)
tcdel is a command to delete traffic control from a network interface (device).

### tcdel help
```console
usage: tcdel [-h] [--version] [--logging] [--stacktrace] [--debug | --quiet]
             --device DEVICE

optional arguments:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
  --debug          for debug print.
  --quiet          suppress output of execution log message.

Miscellaneous:
  --logging        output execution log to a file (tcdel.log).
  --stacktrace     display stack trace when an error occurred.

Traffic Control:
  --device DEVICE  network device name (e.g. eth0)
```

### e.g.
```console
# tcdel --device eth0
```


# Advanced usage
## Traffic control of incoming packets
Execute `tcset` command with `--direction incoming` option to set incoming traffic control.
Other options are the same as in the case of the basic usage.

### e.g. Set traffic control both incoming and outgoing network
```console
tcset --device eth0 --direction outgoing --rate 200K --network 192.168.0.0/24
tcset --device eth0 --direction incoming --rate 1M --network 192.168.0.0/24
```

### Requirements
Incoming packet traffic control requires additional ifb module, 
Which need to the following conditions:

- Equal or greater than Linux kernel version 2.6.20
- Equal or newer than iproute2 package version 20070313


# Dependencies
## Linux package
- iproute2 (reqrequired for tc commandured)

## Python packagge
Dependency python packages are automatically installed during AAA installation via pip.

- [DataPropery](https://github.com/thombashi/DataProperty)
- [ipaddress](https://pypi.python.org/pypi/ipaddress)
- [six](https://pypi.python.org/pypi/six/)
- [thutils](https://github.com/thombashi/thutils)

### Test dependencies
- [pingparsing](https://github.com/thombashi/pingparsing)
- [pytest](https://pypi.python.org/pypi/pytest)
- [pytest-runner](https://pypi.python.org/pypi/pytest-runner)
- [tox](https://pypi.python.org/pypi/tox)
