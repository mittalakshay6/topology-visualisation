#!/usr/local/bin/python3.8

# This script is responsible for preparing the topology dictionary of all the routers in our lab

from pprint import pprint
import genie.libs.sdk.apis.iosxr.lldp.get as lldp_get
import genie.libs.sdk.apis.iosxr.running_config.get as run_get
from genie.libs.sdk.apis.iosxr.lldp import configure
from genie.testbed import load
from utilities.clear_line import clear_line
from unicon.eal.dialogs import Statement, Dialog
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.iosxr.running_config.configure import restore_running_config

# TODO: Think about breakout interfaces. One possible solution is to not do commit replace, rather get the list of all the interfaces (v4, v6, vrf), and unshut them.
# TODO: Study and implement logger here and replace with all pprint statements.
# TODO: Document generation from doc strings.
# TODO: Implement concurrency for possible parallel operations on the routers.


login_creds = ["default", "alternate0", "alternate1", "alternate2", "alternate3"]


def build_device_object_list(testbed):

    pprint("Building the device object list")
    devices = []
    for device in testbed.devices.values():
        devices.append(device)
    return devices


def connect_to_all_devices(devices, force=True):

    success = []
    failed = []
    for device in devices:
        pprint("Clear line for device {device}".format(device=device.name))
        if force:
            try:
                clear_line(str(device.connections.a.ip), device.connections.a.port)
            except EOFError as err:
                pprint(
                    "Failed to clear line for {device} at {ip}:{port}, Reason: {reason}".format(
                        device=device.name,
                        ip=device.connections.a.ip,
                        port=device.connections.a.port,
                        reason=str(err),
                    )
                )
            try:
                clear_line(str(device.connections.b.ip), device.connections.b.port)
            except EOFError as err:
                pprint(
                    "Failed to clear line for {device} at {ip}:{port}, Reason: {reason}".format(
                        device=device.name,
                        ip=device.connections.b.ip,
                        port=device.connections.b.port,
                        reason=str(err),
                    )
                )
            except AttributeError as err:
                pass
        try:
            pprint("Try to connect to device {device}".format(device=device.name))
            device.connect(
                learn_hostname=True,
                prompt_recovery=True,
                log_stdout=False,
                login_creds=login_creds,
            )
            success.append(device)
            continue
        except Exception as err:
            pprint(
                "Failed to connect to {device} at {ip}:{port}, Reason: {reason}".format(
                    device=device.name,
                    ip=device.connections.a.ip,
                    port=device.connections.a.port,
                    reason=str(err),
                )
            )
            failed.append(device)
            continue

    return success, failed


def disconnect_from_all_devices(devices):
    for device in devices:
        pprint("Disconnecting from device {device}".format(device=device.name))
        try:
            device.destroy()
        except Exception as err:
            pprint(
                "Failed to disconnect from device {device} : {err}".format(
                    device=device, err=str(err)
                )
            )


def save_running_config(device):

    cmd = "show running-config | file harddisk:/show_topology_run_config.conf"
    yes_cmd = Statement(
        pattern=r"^.*The +destination +file +already +exists\. +Do +you +want +to +overwrite\? +\[no\]\:",
        action="sendline(y)",
        loop_continue=True,
        continue_timer=False,
    )
    # Begin timeout
    command_timeout = 300
    max_time = 120
    check_interval = 30
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.execute(
                cmd, timeout=command_timeout, reply=Dialog([yes_cmd])
            )
        except Exception as e:
            raise Exception("Cannot save running-config {}".format(str(e)))
        # Copy in progress...
        pprint(output)
        if "[OK]" in output or "Copy complete" in output:
            break
        if "system not ready" in output or "Building configuration..." in output:
            pprint(
                "Still building configuration. Re-attempting save config "
                "after '{}' seconds".format(check_interval)
            )
            timeout.sleep()
            continue
    else:
        # No break
        raise Exception("Failed to save running-config.")


def save_running_config_on_all_devices(devices):
    for device in devices:
        pprint("Saving running config on device {device}".format(device=device.name))
        try:
            device.old_hostname = run_get.get_running_config_hostname(device)
        except:
            device.old_hostname = "ios"
        try:
            save_running_config(device)
        except Exception as err:
            pprint(
                "Failed to save running config on device {device} : {err}".format(
                    device=device.name, err=str(err)
                )
            )
    pprint("Done saving running configs for devices")


def restore_running_config_on_all_devices(devices):
    for device in devices:
        pprint("Restoring running config on {device}".format(device=device.name))
        try:
            device.state_machine.hostname = device.old_hostname
            if device.old_hostname == "ios":
                device.configure("no hostname", prompt_recovery=True)
            else:
                device.configure(
                    "hostname {old_hostname}".format(old_hostname=device.old_hostname),
                    prompt_recovery=True,
                )
            restore_running_config(
                device, "harddisk:/", "show_topology_run_config.conf"
            )
        except Exception as err:
            pprint(
                "Failed to restore running config on device {device} : {err}".format(
                    device=device.name, err=str(err)
                )
            )
    pprint("Running config restored successfully on all the devices")


def commit_replace_hostame_config(device):
    # Note: The name under devices in testbed yaml file must always match the hostname.
    device.state_machine.hostname = "ios"
    device.configure("commit replace", prompt_recovery=True)
    device.state_machine.hostname = device.name
    device.configure(
        "hostname {device_name}".format(device_name=device.name), prompt_recovery=True
    )
    device.destroy()
    device.connect(prompt_recovery=True, learn_hostname=True, login_creds=login_creds)


def commit_replace_hostname_config_all(devices):
    for device in devices:
        try:
            pprint(
                "Try commit replace and hostname config for device {device}".format(
                    device=device.name
                )
            )
            commit_replace_hostame_config(device)
        except Exception as err:
            pprint(
                "Commit replace and hostname config failed for device {device} : {err}".format(
                    device=device.name, err=str(err)
                )
            )
    pprint("Commit replace and hostname config done on all devices")


def apply_mh_config(device):
    device.configure(device.custom.mh_config)


def apply_mh_config_all(devices):
    for device in devices:
        if not device.custom.mh_config:
            continue
        try:
            print("Applying MH Config on {device}".format(device=device.name))
            apply_mh_config(device)
        except Exception as err:
            print(
                "Failed to apply MH config on {device}: {err}".format(
                    device=device.name, err=str(err)
                )
            )


def configure_lldp_on_all_devices(devices):

    for device in devices:
        try:
            pprint("configure lldp on device {device}".format(device=device.name))
            configure.configure_lldp(device)
        except Exception as err:
            pprint(
                "LLDP configuration on device {device} failed : {err}".format(
                    device=device.name, err=str(err)
                )
            )
    pprint("LLDP configuration on devices done")


def build_lldp_info_dict(devices):
    lldp_info_dict = {}
    for device in devices:
        try:
            pprint(
                "Try to get lldp neighbour info from device {device}".format(
                    device=device.name
                )
            )
            lldp_info_dict[device.name] = lldp_get.get_lldp_neighbors_info(device)
        except Exception as err:
            pprint(
                "Failed to get lldp neighbour info from device {device} : {err}".format(
                    device=device.name, err=str(err)
                )
            )
    pprint("LLDP info collection done")
    return lldp_info_dict


def build_topology_list_from_lldp_info(lldp_info_dict):

    # (dev1, intf1) -> (dev2, intf2)
    topology_list = []
    for device_name in lldp_info_dict.keys():
        lldp_info = lldp_info_dict[device_name]
        if not lldp_info["total_entries"]:
            continue
        for local_intf in lldp_info["interfaces"].keys():
            local = (device_name, local_intf)

            remote_intf = list(lldp_info["interfaces"][local_intf]["port_id"])[0]
            remote_device = list(
                lldp_info["interfaces"][local_intf]["port_id"][remote_intf]["neighbors"]
            )[0]
            remote = (remote_device, remote_intf)

            # check if the link is already present in the list
            link_present = (local, remote) in topology_list or (
                remote,
                local,
            ) in topology_list

            if link_present:
                continue
            else:
                topology_list_obj = (local, remote)
                topology_list.append(topology_list_obj)

    return topology_list
