"""
# ########################################
# Step 1: Generate the YAML file
#
# Created with love by Akshay Mittal.
# ########################################
"""

#!/usr/local/bin/python3.8

import sys
import pathlib
import time

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities import excel
from utilities import misc

t0 = time.time()

misc.create_dir("./tmp")
print("{filename}: Start downloading testbed excel sheet.".format(
    filename=__file__))
excel.download_testbed_excel_file()

print("{filename}: Open excel file.".format(filename=__file__))
print("{filename}: The following warning can be safely ignored".format(
    filename=__file__))
ws = excel.open_excel_worksheet()

print("{filename}: Construct yaml dict.".format(filename=__file__))
yaml_dict = excel.construct_testbed_yaml_dict_from_excel_ws(ws)

print("{filename}: Write yaml dict to yaml file.".format(filename=__file__))
excel.write_yaml_dict_to_yaml_file(yaml_dict, "tmp/testbed.yaml")

t1 = time.time()
t = t1 - t0
ty_res = time.gmtime(t)
res = time.strftime("%M:%S", ty_res)
print("SUCCESS !!! (Time taken = {min} min and {sec} seconds)".format(
    min=res.split(":")[0], sec=res.split(":")[1]))
