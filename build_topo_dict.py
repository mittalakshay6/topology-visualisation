#!/usr/local/bin/python3.8

# This script is responsible for preparing the topology dictionary of all the routers in our lab

import logging
from pprint import pprint
import time
import genie.libs.sdk.apis.iosxr.lldp.get as lldp_get
import genie.libs.sdk.apis.iosxr.running_config.get as run_get
from genie.libs.sdk.apis.iosxr.lldp import configure
from genie.testbed import load
from clear_line import clear_line

logger = logging.getLogger(__name__)

# TODO: Think about breakout interfaces. One possible solution is to not do commit replace, rather get the list of all the interfaces (v4, v6, vrf), and unshut them.
# TODO: Study and implement logger here and replace with all print statements.
# TODO: Document generation from doc strings.
# TODO: Implement concurrency for possible parallel operations on the routers.


def build_device_object_list(testbed):

    devices = []
    for device in testbed.devices.values():
        devices.append(device)
    return devices


def connect_to_all_devices(devices, force=True):

    success = []
    failed = []
    for device in devices:
        if(force):
            try:
                clear_line(str(device.connections.cli.ip),
                           device.connections.cli.port)
            except EOFError as err:
                print("Failed to clear line for {device} at {ip}:{port}, Reason: {reason}".format(
                    device=device.name, ip=device.connections.cli.ip, port=device.connections.cli.port, reason=str(err)))
                failed.append(device)
                continue
        try:
            device.connect(via="cli", learn_hostname=True,
                           prompt_recovery=True,
                           log_stdout=False
                           )
            success.append(device)
            continue
        except Exception as err:
            print("Failed to connect to {device} at {ip}:{port}, Reason: {reason}".format(
                device=device.name, ip=device.connections.cli.ip, port=device.connections.cli.port, reason=str(err)))
            failed.append(device)
            continue

    return success, failed


def disconnect_from_all_devices(devices):
    for device in devices:
        device.disconnect()


def build_running_config_dict(devices):

    device_to_run_conf = {}
    for device in devices:
        # Fetch running config
        running_conf = run_get.get_valid_config_from_running_config(
            device)
        # Add this to the dictionary
        device_to_run_conf[device.name] = running_conf
    return device_to_run_conf


def restore_running_config_on_all_devices(devices, running_conf_dict):

    for device in devices:
        run_conf = running_conf_dict[device.name]
        device.configure("commit replace")
        device.configure(run_conf)


def commit_replace_all_devices(devices):
    for device in devices:
        device.configure("commit replace")
        device.disconnect()
    connect_to_all_devices(devices)


def configure_hostname_on_all_devices(devices):

    for device in devices:
        device.configure("hostname {hostname}".format(hostname=device.name))
    return


def configure_lldp_on_all_devices(devices):

    for device in devices:
        configure.configure_lldp(device)


def build_lldp_info_dict(devices):
    lldp_info_dict = {}
    for device in devices:
        lldp_info_dict[device.name] = lldp_get.get_lldp_neighbors_info(device)
    return lldp_info_dict


def build_topology_list_from_lldp_info(lldp_info_dict):

    # (dev1, intf1) -> (dev2, intf2)
    topology_list = []
    for device_name in lldp_info_dict.keys():
        lldp_info = lldp_info_dict[device_name]
        if (not lldp_info["total_entries"]):
            continue
        for local_intf in lldp_info["interfaces"].keys():
            local = (device_name, local_intf)

            remote_intf = list(
                lldp_info["interfaces"][local_intf]["port_id"])[0]
            remote_device = list(
                lldp_info["interfaces"][local_intf]["port_id"][remote_intf]["neighbors"])[0]
            remote = (remote_device, remote_intf)

            # check if the link is already present in the list
            link_present = (local, remote) in topology_list or (
                remote, local) in topology_list

            if link_present:
                continue
            else:
                topology_list_obj = (local, remote)
                topology_list.append(topology_list_obj)

    return topology_list


def build_topology_list(yaml_file_location):

    pprint("Loading the yaml file")
    testbed = load(yaml_file_location)
    pprint("Building device object list")
    devices = build_device_object_list(testbed)
    pprint("Trying to connect to devices")
    devices_success, devices_fail = connect_to_all_devices(devices)
    pprint("Total: {devices} Success: {success} Fail: {fail}".format(
        devices=len(devices), success=len(devices_success), fail=len(devices_fail)))
    pprint("Success:")
    pprint(devices_success)
    pprint("Fail:")
    pprint(devices_fail)

    pprint("Building running config for all the devices")
    running_config_dict = build_running_config_dict(devices_success)

    pprint("Commit replace all devices")
    commit_replace_all_devices(devices_success)

    pprint("Configuring hostname on all devices")
    configure_hostname_on_all_devices(devices_success)

    pprint("Configuring lldp on all the devices")
    configure_lldp_on_all_devices(devices_success)

    pprint("Sleep for 30 sec for LLDP packets exchange")
    time.sleep(30)

    pprint("Building LLDP info dict")
    lldp_info_dict = build_lldp_info_dict(devices_success)

    pprint("Restoring running config")
    restore_running_config_on_all_devices(devices_success, running_config_dict)

    pprint("Release all devices")
    disconnect_from_all_devices(devices_success)

    topo_list = build_topology_list_from_lldp_info(lldp_info_dict)

    return topo_list
