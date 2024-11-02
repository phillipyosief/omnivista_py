import requests
import json
import logging
import datetime
from .exceptions import *

class OVClient:
    def __init__(self, url: str, username: str, password: str, verify: bool = True, log: bool = False):
        """
        Initialize the API client.

        Args:
            url (str): Base URL of the API, e.g. https://omnivista.company.de
            username (str): Username for API authentication
            password (str): Password for API authentication
            verify (bool): Whether to verify SSL certificates
            log (bool): Whether to enable logging
        """
        self.url = url
        self.username = username
        self.password = password
        self.verify = verify
        self.log = log
        self.session = requests.Session()

        # Configure logging if enabled
        if self.log:
            logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    def _log(self, message: str):
        """Log a message if logging is enabled."""
        if self.log:
            logging.info(message)

    def _get_headers(self):
        return {"content-type": "application/json"}

    def _get(self, endpoint: str, params=None):
        """Internal method to perform GET requests to a specified endpoint.

        Args:
            endpoint (str): The API endpoint to request data from.
            params (dict, optional): Query parameters to include in the request.

        Returns:
            dict: The JSON response from the API.
        """
        self._log(f"Getting data from endpoint: {endpoint}")
        response = self.session.get(f"{self.url}/{endpoint}", verify=self.verify, headers=self._get_headers(), params=params)
        
        try:
            response.raise_for_status()  # Raise an error for bad responses
            self._log(f"Data retrieved successfully from {endpoint}!")
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._log(f"Failed to retrieve data from {endpoint}: {e}")
            raise DeviceRetrievalError(f"Failed to retrieve data from {endpoint}: {e}")  # Verwende die benutzerdefinierte Ausnahme
        except json.decoder.JSONDecodeError:
            if str(response.text).__contains__('Not found'):
                self._log(response.text)
                raise requests.HTTPError('Page cannot be found')
        except requests.exceptions.HTTPError:
            self._log(f'Page cannot be found')
            raise requests.exceptions.HTTPError('Page cannot be found')
        except Exception as e:
            self._log(e)
            raise e

    def login(self):
        """Log in to the API and return the response."""
        rbody = {
            'userName': self.username,
            'password': self.password
        }
        self._log(f"Attempting to log in with username: {self.username}")
        response = self.session.post(f"{self.url}/api/login", data=json.dumps(rbody), verify=self.verify, headers=self._get_headers())
        
        try:
            response.raise_for_status()  # Raise an error for bad responses
            self._log("Login successful!")
            return response.json()
        except requests.exceptions.HTTPError as e:
            self._log(f"Login failed: {e}")
            raise LoginError(f"Login failed: {e}")  # Verwende die benutzerdefinierte Ausnahme

    def _get_all_devices(self):
        """Get the list of devices from the API."""
        self._log("Getting devices...")
        return self._get("api/devices")  # Verwende die neue _get-Methode
    
    def get_all_devices(self):
        """Get the list of devices from the API."""
        self._log("Getting devices...")
        return self._get_all_devices()["response"]  # Verwende die neue _get-Methode
    

    def get_all_information(self):
        """Get the list of devices from the API."""
        self._log("Getting information...")
        return self._get("api/devices") 


    class Device:
        def __init__(self, client: 'OVClient', ip_address: str = None, mac_address: str = None, hostname: str = None):
            if not (ip_address or mac_address or hostname):
                raise ValueError("At least one of ip_address, mac_address, or hostname must be provided.")

            self.client = client  # Store a reference to the OVClient instance
            self.ip_address = ip_address
            self.mac_address = mac_address
            self.hostname = hostname

        def _search(self):
            """
            Find a device based on IP address, MAC address, or hostname.
            You can also use more than one property to search for, but they all 
            need to match with the found device.
    
            Returns:
                dict: The details of the found device, or None if not found.
            """
            devices = self.client._get_all_devices()  # Use the client instance to get the full list of devices
            devices = devices['response']
            
            for device in devices:
                if (self.ip_address and device.get('ipAddress') == self.ip_address) or \
                   (self.mac_address and device.get('macAddress') == self.mac_address) or \
                   (self.hostname and device.get('name') == self.hostname):
                    return device
    
            # Return None if no device was found
            raise DeviceRetrievalError(f"Can't find Device {self.ip_address}, {self.mac_address}, {self.hostname}")
        
        def _get(self, keys):
            """
            Get a property of the response from the device using this method

            Returns:
                dict or any: Returns with the searched property

            Raises:
                DeviceRetrievalError: If no device is found.
                APIClientError: If the keys are invalid or not found in the response.
            """
            if not isinstance(keys, (list, str)):
                raise APIClientError("Keys must be a string or a list of strings.")

            device = self._search()
            if not device:
                raise DeviceRetrievalError("No device found.")

            response = device  # Assuming device_data contains the response

            if isinstance(keys, list):
                result = {}
                for key in keys:
                    if key not in response:
                        raise APIClientError(f"Key '{key}' not found in the device response.")
                    result[key] = response.get(key, None)
                return result
            else:
                if keys not in response:
                    raise APIClientError(f"Key '{keys}' not found in the device response.")
                return response.get(keys, None)
        
        def get_all_information(self):
            """
            Returns all information from the device as a JSON object.

            Returns:
                dict: JSON response from the device

            Raises:
                DeviceRetrievalError: If no device is found.
            """
            return self._search()

        def get_ip_address(self):
            """
            Returns with the ip-address of the device
            
            Returns:
                str: IP-address of the device
            """
            return self._get(['ipAddress'])['ipAddress']

        def get_running_directory(self):
            """
            Returns with current running directory of the device 
            
            Returns:
                str: name of the current running directory
            """
            return self._get(['runningFrom'])['runningFrom']
        
        def get_mac_address(self):
            """
            Returns with the mac-address of the device
            
            Returns:
                str: Mac-address of the device
            """
            return self._get(['macAddress'])['macAddress']
            
        def get_software_version_advanced(self):
            """
            Returns with every software version for every module
            
            Returns:
                dict or str: Softwareversion 
            """
            return self._get(['ModulesInfo'])['ModulesInfo']
        
        def get_software_version(self):
            """
            Returns with the running software version

            Returns:
                dict: Module Info
            """
            return self._get(['version'])['version']
        
        def get_ip_interfaces(self):
            """
            Returns with all created ip interfaces

            Returns:
                dict: IP Interfaces
            """
            return self._get(['IpAddressesInfo'])['IpAddressesInfo']
        
        def get_hostname(self):
            """
            Returns with the hostname of the device
            
            Returns:
                str: Configured hostname of the device
            """
            return self._get(['name'])['name']
        
        def get_location(self):
            """
            Returns with the location of the Device
            
            Returns:
                str: Configured location of the deivce
            """
            return self._get(['name'])['name']
        
        def get_description(self):
            """
            Returns with the description of the Device
            
            Returns:
                str: Configured description of the device
            """
            return self._get(['description'])['description']

        def get_model_name(self):
            """
            Returns with the model names of the device or 
            it returns with the model names of every device in a virtual chassis
            
            Returns:
                str or dict: Model name of the device
            """
            return self._get(['others'])
        
        
