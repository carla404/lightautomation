import tradfriObjects

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
        fd = open(CONFIG_FILE)
    except IOError as e:
        print("I/O error({}): {}".format(e.errno, e.strerror))
        exit()

    js = json.load(fd)

    return js

def main():
    conf = getConfig()

    gw = tradfriObjects.gw(conf["ip"],conf["key"])







    gw.turnLightsOff()
    time.sleep(1)

    gw.turnLightsOn(80)
    time.sleep(1)

    gw.turnLightsOff()
    time.sleep(1)






if __name__ == "__main__":
    main()