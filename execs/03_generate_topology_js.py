from genie.testbed import load

import sys
import pathlib
import time

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities.generate_topology import build_topology_json_dict, write_topology_file

t0 = time.time()

yaml_file_location = "yaml/testbed.yaml"

print("Loading the yaml file")
testbed = load(yaml_file_location)

with open("./tmp/topology.list", "r") as filehandler:
    topo_list = filehandler.read()
topo_list = eval(topo_list)
topology_json = build_topology_json_dict(topo_list, testbed.devices)

write_topology_file(topology_json)
print("Topology.js file created.")

t1 = time.time()
t = t1 - t0

print("SUCCESS !!! (Time taken = {time} sec".format(time=t))
