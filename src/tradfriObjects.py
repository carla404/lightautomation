from pytradfri import Gateway
from pytradfri import device
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError

import uuid
import argparse

class gw(object):
    '''

    '''
    def __init__(self, ip, key):

        self.devices = []
        self.lights = []

        identity = uuid.uuid4().hex
        api_factory = APIFactory(ip, psk_id=identity)
        psk = api_factory.generate_psk(key)
        print("Generated PSK: ", psk)

        self.api = api_factory.request
        self.gateway = Gateway()

        devices_command = self.gateway.get_devices()
        devices_commands = self.api(devices_command)
        devices = self.api(devices_commands)

        print("Found devices")
        for device in devices:
            print(device)
            if device.has_light_control:
                self.lights.append(device)

    def turnLightsOn(self, dimmer=10):
        for light in self.lights:
            self.api(light.light_control.set_dimmer(dimmer))

    def turnLightsOff(self):
        for light in self.lights:
            self.api(light.light_control.set_dimmer(0))
