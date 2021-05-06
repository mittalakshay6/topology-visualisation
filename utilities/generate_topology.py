#!/usr/local/bin/python3.8

import json

OUTPUT_TOPOLOGY_FILENAME = "topology.js"
TOPOLOGY_FILE_HEAD = "\n\nvar topologyData = "

# TODO: Add more info, telnet IP and port in topology.js


def build_topology_json_dict(topology_list, no_link_dict, devices):

    host_id = 0
    host_id_map = {}
    topology_dict = {"nodes": [], "links": []}

    # Generate topology JSON dict
    for device_name in no_link_dict.keys():
        if host_id_map.get(device_name) == None:
            host_id_map[device_name] = host_id
            try:
                localip = str(devices[device_name].connections.a.ip)
            except KeyError:
                localip = None
            try:
                localport = devices[device_name].connections.a.port
            except KeyError:
                localport = None
            tgen = devices[device_name].custom.tgen
            icon = "dead_node" if no_link_dict[
                device_name] == "dead" else "router"
            topology_dict["nodes"].append({
                "id": host_id,
                "name": device_name,
                "telnetIP": localip,
                "telnetPort": localport,
                "icon": icon,
                "tgen": tgen,
            })
            host_id += 1
    for tuple in topology_list:
        local_name = tuple[0][0]
        remote_name = tuple[1][0]
        if host_id_map.get(local_name) == None:
            host_id_map[local_name] = host_id
            try:
                localip = str(devices[local_name].connections.a.ip)
            except KeyError:
                localip = None
            try:
                localport = devices[local_name].connections.a.port
            except KeyError:
                localport = None
            tgen = devices[local_name].custom.tgen
            topology_dict["nodes"].append({
                "id": host_id,
                "name": local_name,
                "telnetIP": localip,
                "telnetPort": localport,
                "icon": "router",
                "tgen": tgen,
            })
            host_id += 1
        if host_id_map.get(remote_name) == None:
            host_id_map[remote_name] = host_id
            try:
                remoteip = str(devices[remote_name].connections.a.ip)
            except KeyError:
                remoteip = None
            try:
                remoteport = devices[remote_name].connections.a.port
            except KeyError:
                remoteport = None
            tgen = devices[remote_name].custom.tgen
            topology_dict["nodes"].append({
                "id": host_id,
                "name": remote_name,
                "telnetIP": remoteip,
                "telnetPort": remoteport,
                "icon": "router",
                "tgen": tgen,
            })
            host_id += 1

    link_id = 0
    for tuple in topology_list:
        local_name = tuple[0][0]
        local_intf = tuple[0][1]
        remote_name = tuple[1][0]
        remote_intf = tuple[1][1]
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
                        dst=OUTPUT_TOPOLOGY_FILENAME):

    with open(dst, "w") as topology_file:
        topology_file.write(header)
        topology_file.write(json.dumps(topology_json, indent=4,
                                       sort_keys=True))
        topology_file.write(";")
