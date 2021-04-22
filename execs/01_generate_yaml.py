import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from utilities import excel

# TODO: Delete temporary files.

print("{filename}: Start downloading testbed excel sheet.".format(filename=__file__))
excel.download_testbed_excel_file()

print("{filename}: Open excel file.".format(filename=__file__))
print(
    "{filename}: The following warning can be safely ignored".format(filename=__file__)
)
ws = excel.open_excel_worksheet()

print("{filename}: Construct yaml dict.".format(filename=__file__))
yaml_dict = excel.construct_testbed_yaml_dict_from_excel_ws(ws)

print("{filename}: Write yaml dict to yaml file.".format(filename=__file__))
excel.write_yaml_dict_to_yaml_file(yaml_dict, "yaml/testbed.yaml")

print("SUCCESS !!!")