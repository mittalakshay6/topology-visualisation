#!/usr/local/bin/python3.8

import os
import time

t0 = time.time()

cmd = os.path.join(os.getcwd(), "execs/01_generate_yaml.py")
os.system("{} {}".format("python", cmd))
cmd = os.path.join(os.getcwd(), "execs/02_generate_topology_list.py")
os.system("{} {}".format("python", cmd))
cmd = os.path.join(os.getcwd(), "execs/03_generate_topology_js.py")
os.system("{} {}".format("python", cmd))
cmd = os.path.join(os.getcwd(), "execs/update_reservations.py")
os.system("{} {}".format("python", cmd))

t1 = time.time()
t = t1 - t0
ty_res = time.gmtime(t)
res = time.strftime("%M:%S", ty_res)
print()
print("Total time taken = {min} min and {sec} seconds)".format(
    min=res.split(":")[0], sec=res.split(":")[1]))