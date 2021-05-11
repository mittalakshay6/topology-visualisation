#!/usr/local/bin/python3.8

import json
from datetime import datetime
from utilities import excel

OUTPUT_TOPOLOGY_FILENAME = "static/generated/topology.js"
OUTPUT_NODE_RESERVATION_FILENAME = "static/generated/node_reservation.js"
TOPOLOGY_FILE_TIME_VAR = "\n\ntopology_timestamp = "
TOPOLOGY_FILE_HEAD = "\n\nvar topologyData = "
NODE_RESERVATION_FILE_HEAD = "\n\nvar nodeReservationData = "
NODE_RESERVATION_FILE_TIME_VAR = "\n\nvar reservation_timestamp = "


def is_valid_device(device_name, devices):
    return device_name in devices.keys()


def build_topology_json_dict(topology_list, no_link_dict, devices):

    host_id = 0
    host_id_map = {}
    topology_dict = {"nodes": [], "links": []}

    # Generate topology JSON dict
    for device_name in no_link_dict.keys():
        if (not is_valid_device(device_name=device_name, devices=devices)):
            continue
        if host_id_map.get(device_name) == None:
            host_id_map[device_name] = host_id
            localip = str(devices[device_name].connections.a.ip)
            localport = devices[device_name].connections.a.port
            tgen = devices[device_name].custom.tgen
            project = devices[device_name].custom.project
            if no_link_dict[device_name] == "dead":
                icon = "dead_node"
            elif tgen is None:
                icon = "router"
            else:
                icon = "nexus5000"
            topology_dict["nodes"].append({
                "id": host_id,
                "name": device_name,
                "telnetIP": localip,
                "telnetPort": localport,
                "icon": icon,
                "tgen": str(tgen),
                "project": str(project)
            })
            host_id += 1
    for tuple in topology_list:
        local_name = tuple[0][0]
        remote_name = tuple[1][0]
        if (not is_valid_device(local_name, devices)
                or not is_valid_device(remote_name, devices)):
            continue
        if host_id_map.get(local_name) == None:
            host_id_map[local_name] = host_id
            localip = str(devices[local_name].connections.a.ip)
            localport = devices[local_name].connections.a.port
            tgen = devices[local_name].custom.tgen
            icon = "nexus5000" if tgen else "router"
            project = devices[local_name].custom.project
            topology_dict["nodes"].append({
                "id": host_id,
                "name": local_name,
                "telnetIP": localip,
                "telnetPort": localport,
                "icon": icon,
                "tgen": str(tgen),
                "project": str(project)
            })
            host_id += 1
        if host_id_map.get(remote_name) == None:
            host_id_map[remote_name] = host_id
            remoteip = str(devices[remote_name].connections.a.ip)
            tgen = devices[remote_name].custom.tgen
            icon = "nexus5000" if tgen else "router"
            project = devices[remote_name].custom.project
            remoteport = devices[remote_name].connections.a.port
            topology_dict["nodes"].append({
                "id": host_id,
                "name": remote_name,
                "telnetIP": remoteip,
                "telnetPort": remoteport,
                "icon": icon,
                "tgen": str(tgen),
                "project": str(project)
            })
            host_id += 1

    link_id = 0
    for tuple in topology_list:
        local_name = tuple[0][0]
        local_intf = tuple[0][1]
        remote_name = tuple[1][0]
        remote_intf = tuple[1][1]
        if (not is_valid_device(local_name, devices)
                or not is_valid_device(remote_name, devices)):
            continue
        topology_dict["links"].append({
            "id": link_id,
            "source": host_id_map[local_name],
            "target": host_id_map[remote_name],
            "srcIfName": local_intf,
            "srcDevice": local_name,
            "tgtIfName": remote_intf,
            "tgtDevice": remote_name,
        })
        link_id += 1

    return topology_dict


def write_topology_file(topology_json,
                        header=TOPOLOGY_FILE_HEAD,
                        dst=OUTPUT_TOPOLOGY_FILENAME,
                        timestamp_head=TOPOLOGY_FILE_TIME_VAR):

    now = datetime.now()
    dt_string = now.strftime("%d/%b/%Y %H:%M:%S")
    with open(dst, "w") as topology_file:
        topology_file.write(header)
        topology_file.write(json.dumps(topology_json, indent=4,
                                       sort_keys=True))
        topology_file.write(";")
        topology_file.write(timestamp_head)
        topology_file.write("\"" + dt_string + "\"")


def build_node_reservation_dict(ws):
    reservation_dict = {}
    for row in range(2, 9999):
        device_name, _, _ = excel.construct_device_name(ws, row)
        if device_name == "continue":
            continue
        elif device_name == "break":
            break
        status = excel.get_reservation_status(ws, row)
        reservation_dict[device_name] = str(status)
    return reservation_dict


def write_node_reservation_file(node_reservation_dict,
                                header=NODE_RESERVATION_FILE_HEAD,
                                dst=OUTPUT_NODE_RESERVATION_FILENAME,
                                timestamp_head=NODE_RESERVATION_FILE_TIME_VAR):

    now = datetime.now()
    dt_string = now.strftime("%d/%b/%Y %H:%M:%S")
    with open(dst, "w") as node_reservation_file:
        node_reservation_file.write(header)
        node_reservation_file.write(
            json.dumps(node_reservation_dict, indent=4, sort_keys=True))
        node_reservation_file.write(";")
        node_reservation_file.write(timestamp_head)
        node_reservation_file.write("\"" + dt_string + "\"")