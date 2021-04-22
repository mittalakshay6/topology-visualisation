from genie.testbed import load

import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities import excel
from utilities.generate_topology import build_topology_json_dict, write_topology_file

yaml_file_location = "yaml/testbed.yaml"

print("Loading the yaml file")
testbed = load(yaml_file_location)

ws = excel.open_excel_worksheet()
excel.add_tgen_info_to_device_objects_from_ws(ws, testbed.devices)

with open("./tmp/topology.list", "r") as filehandler:
    topo_list = filehandler.read()
topo_list = eval(topo_list)
topology_json = build_topology_json_dict(topo_list, testbed.devices)

write_topology_file(topology_json)

print("Topology.js file created.")
print("SUCCESS !!!")