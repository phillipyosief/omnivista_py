# omnivista_py - An API Client for the Alcatel-Lucent OmniVista 2500
> a Python library that simplifies interaction with the OmniVista API.

![PyPI - Version](https://img.shields.io/pypi/v/omnivista_py)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/omnivista_py)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/omnivista_py)
[![Upload Python Package](https://github.com/phillipyosief/omnivista_py/actions/workflows/python-publish.yml/badge.svg)](https://github.com/phillipyosief/omnivista_py/actions/workflows/python-publish.yml)

omnivista_py allows easy management of network devices, and querying of performance data. With integrated error handling and optional logging

## Installation

Using [PyPi](https://pypi.org/project/omnivista-py/)
```sh
pip install omnivista_py
```

## Usage example

With omnivista_py, it has never been easier to search for a device and retrieve information about it.

Here is an example of how to initialize the client, search for 3 devices using three different attributes, and then print out their software version, configured IP interfaces, and the current directory they are running in.
```python
from omnivista_py import OVClient, Device

client = OVClient(
    url="https://omnivista.com",
    username="your_username",
    password="your_password"
)
client.login

device1 = client.Device(client, ip_address="192.168.1.1")
device2 = client.Device(client, hostname="myalcateldevice")
device3 = client.Device(client, mac_address="3a:5f:1c:7e:2b:9d")

devices = [device1, device2, device3]

for device in devices:
    print(device.get_software_version())
    print(device.get_ip_interfaces())
    print(device.get_running_directory())
```

You can find more examples [here]()

## Future Plans
There are several features and improvements planned for future releases of omnivita_py.
Which you can find all under [Projects](https://github.com/phillipyosief/omnivista_py/projects)


## Meta

Phillip Jerome Yosief

Distributed under the MIT license. See [``LICENSE``](LICENSE) for more information.

[github.com/phillipyosief/](https://github.com/phillipyosief/)

## Contributing

1. Fork it (<https://github.com/phillipyosief/omnivista_py/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
