"""
# ########################################
# Step 3: Process and dump the collected information.
#
# Created with love by Akshay Mittal.
# ########################################
"""

#!/usr/local/bin/python3.8

from genie.testbed import load

import sys
import pathlib
import time

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities.generate_topology import build_topology_json_dict, write_topology_file
from utilities import misc

t0 = time.time()

yaml_file_location = "tmp/testbed.yaml"

print("Loading the yaml file")
testbed = load(yaml_file_location)

with open("./tmp/topology.list", "r") as filehandler:
    topo_list = filehandler.read()
topo_list = eval(topo_list)
with open("./tmp/no_link.dict", "r") as filehandler:
    no_link_dict = filehandler.read()
no_link_dict = eval(no_link_dict)
topology_json = build_topology_json_dict(topology_list=topo_list,
                                         no_link_dict=no_link_dict,
                                         devices=testbed.devices)
misc.create_dir("./static/generated")
write_topology_file(topology_json)
print("Topology.js file created.")

t1 = time.time()
t = t1 - t0
ty_res = time.gmtime(t)
res = time.strftime("%M:%S", ty_res)
print("SUCCESS !!! (Time taken = {min} min and {sec} seconds)".format(
    min=res.split(":")[0], sec=res.split(":")[1]))
