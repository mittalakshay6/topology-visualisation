#!/usr/local/bin/python3.8

from pprint import pprint
from genie.testbed import load

import sys
import json
import pathlib
import time

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities.build_topo_dict import *


def countdown(time_sec):

    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        time_sec -= 1


yaml_file_location = "yaml/testbed.yaml"

pprint("Loading the yaml file")
testbed = load(yaml_file_location)

devices = build_device_object_list(testbed)

pprint("Trying to connect to devices")
devices_success, devices_fail = connect_to_all_devices(devices)
pprint(
    "Total: {devices} Success: {success} Fail: {fail}".format(
        devices=len(devices), success=len(devices_success), fail=len(devices_fail)
    )
)
pprint("Success:")
pprint(devices_success)
pprint("Fail:")
pprint(devices_fail)

save_running_config_on_all_devices(devices_success)

commit_replace_hostname_config_all(devices_success)

apply_mh_config_all(devices_success)

pprint("Configuring lldp on all the devices")
configure_lldp_on_all_devices(devices_success)

pprint("Sleep for 30 sec for LLDP packets exchange")
countdown(30)

pprint("Building LLDP info dict")
lldp_info_dict = build_lldp_info_dict(devices_success)

restore_running_config_on_all_devices(devices_success)

pprint("Release all devices")
disconnect_from_all_devices(devices_success)

print("Build topology list")
topo_list = build_topology_list_from_lldp_info(lldp_info_dict)

print("Write topology list to file.")
# Write topology list to file.
with open("./tmp/topology.list", "w") as filehandler:
    json.dump(topo_list, filehandler)

print("SUCCESS !!!")