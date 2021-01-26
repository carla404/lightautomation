from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError

import uuid
import argparse
import json
import os

def getConfig():
    CONFIG_FILE = "config.json"
    fd = None

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--conf", dest="config_file", type=str, help="Path to config file"
    )
    args = parser.parse_args()

    if args.config_file is None:
        print("using config.json as configfile")
    else:
        CONFIG_FILE = args.config_file

    try:
        fd = open(os.path.join(os.path.dirname(__file__), CONFIG_FILE))
    except IOError as e:
        print("I/O error({}): {}".format(e.errno, e.strerror))

    js = json.load(fd)

    return js

def main():
    conf = getConfig()

    try:
        identity = conf["identity"]
        api_factory = APIFactory(host=conf["ip"], psk_id=identity, psk=conf["key"])
    except KeyError:
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=conf["ip"], psk_id=identity)

        try:
            psk = api_factory.generate_psk(conf["key"])
            print("Generated PSK: ", psk)

            conf["identity"] = identity
            conf["key"] = psk

        except AttributeError:
            raise PytradfriError(
                "Please provide the 'Security Code' on the "
                "back of your Tradfri gateway using the "
                "-K flag."
            )


    api = api_factory.request

    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    for device in devices:
        print(device)
    print("done...")




if __name__ == "__main__":
    main()