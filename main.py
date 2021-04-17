#!/usr/local/bin/python3.8

from pprint import pprint
from utilities.build_topo_dict import *
from utilities.generate_topology import build_topology_json_dict
from utilities.generate_topology import write_topology_file

yaml_file_location = "yaml/all_devices.yaml"

"""
Step 1: Build device object list
Step 2: Connect to all devices.

"""

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

pprint("Configuring lldp on all the devices")
configure_lldp_on_all_devices(devices_success)

pprint("Sleep for 30 sec for LLDP packets exchange")
time.sleep(30)

pprint("Building LLDP info dict")
lldp_info_dict = build_lldp_info_dict(devices_success)

restore_running_config_on_all_devices(devices_success)

pprint("Release all devices")
disconnect_from_all_devices(devices_success)

topo_list = build_topology_list_from_lldp_info(lldp_info_dict)

topology_json = build_topology_json_dict(topo_list, testbed.devices)

write_topology_file(topology_json)

pprint("Topology file created, run the app in browser now.")
