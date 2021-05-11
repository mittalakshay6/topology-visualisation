"""
# ########################################
#
# Created with love by Akshay Mittal.
#
# ########################################
"""

#!/usr/local/bin/python3.8
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from utilities import excel
from utilities import generate_topology
from utilities import misc

# Download the excel sheet
print("{filename}: Start downloading testbed excel sheet.".format(
    filename=__file__))
misc.create_dir("./tmp")
excel.download_testbed_excel_file()
# Open the excel worksheet
ws = excel.open_excel_worksheet()
# Parse excel sheet and update node reservations js file
node_reservation_dict = generate_topology.build_node_reservation_dict(ws)
misc.create_dir("./static/generated")
generate_topology.write_node_reservation_file(
    node_reservation_dict=node_reservation_dict)
# return error code
print("Done")
sys.stdout.flush()
