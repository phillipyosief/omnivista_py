# OmniVista API Client

`omnivista_py` is a Python library that simplifies interaction with the OmniVista API. It allows easy authentication with a username and password, management of network devices, and querying of performance data. With integrated error handling and optional logging, the client provides developers with an effective tool for automating and monitoring network infrastructures.

## Installation

To install the library, use pip:

```sh
pip install omnivista_py
```

## Usage

### Initialization

First, initialize the `OVClient` with the base URL of the API, username, password, and optional parameters for SSL verification and logging.

```python
from omnivista_py import OVClient

client = OVClient(
    url="https://omnivista.company.de",
    username="your_username",
    password="your_password",
    verify=True,  # Optional, default is True
    log=True      # Optional, default is False
)
```

### Authentication

Log in to the API:

```python
client.login()
```

### Device Management

#### Get All Devices

Retrieve a list of all devices:

```python
devices = client.get_all_devices()
```

#### Device Information

Create a `Device` instance and retrieve various information:

```python
device = client.Device(client, ip_address="192.168.1.1")

# Get all information
info = device.get_all_information()

# Get specific details
hostname = device.get_hostname()
ip_address = device.get_ip_address()
mac_address = device.get_mac_address()
model_name = device.get_model_name()
running_directory = device.get_running_directory()
location = device.get_location()
description = device.get_description()
software_version = device.get_software_version()
software_version_advanced = device.get_software_version_advanced()
ip_interfaces = device.get_ip_interfaces()
```

## Error Handling

The library includes custom exceptions for error handling:

- `APIClientError`: Base class for exceptions in this module.
- `AuthenticationError`: Raised for authentication-related errors.
- `DeviceRetrievalError`: Raised when retrieving devices fails.
- `LoginError`: Raised when login fails.

Example:

```python
try:
    client.login()
except LoginError as e:
    print(f"Login failed: {e}")
```

## License

This project is licensed under the MIT License.