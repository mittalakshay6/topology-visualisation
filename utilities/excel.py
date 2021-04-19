from configparser import SafeConfigParser

import requests
import yaml
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.http.request_options import RequestOptions
from openpyxl import load_workbook

TESTBED_FILE_LOCAL_NAME = "testbed_tracker_downloaded.xlsx"


def download_testbed_excel_file():
    parser = SafeConfigParser(interpolation=None)
    parser.read("settings.cfg")

    username = parser.get("user_credentials", "username")
    password = parser.get("user_credentials", "password")
    testbed_file_url = parser.get("default", "testbed_file_url")

    ctx_auth = AuthenticationContext(testbed_file_url)
    ctx_auth.acquire_token_for_user(username, password)

    options = RequestOptions(testbed_file_url)
    ctx_auth.authenticate_request(options)

    req = requests.get(
        testbed_file_url, headers=options.headers, verify=True, allow_redirects=True
    )
    output = open(TESTBED_FILE_LOCAL_NAME, "wb")
    output.write(req.content)
    output.close()


def open_excel_worksheet():
    wb = load_workbook(filename=TESTBED_FILE_LOCAL_NAME)
    ws = wb.active
    return ws


def construct_testbed_yaml_dict_from_excel_ws(ws):
    yaml_dict = {"devices": {}}
    col = 1
    for row in range(2, 1000):
        device = ws.cell(row=row, column=col).value
        if device is None:
            break
        port = ws.cell(row=row, column=col + 1).value
        if port is None:
            continue
        device_name = device + "_" + str(port)
        port2 = None
        if ws.cell(row=row, column=col + 2).value is not None:
            port2 = ws.cell(row=row, column=col + 2).value
        ip = ws.cell(row=row, column=col + 3).value
        if port2 is None:
            device_dict = {
                device_name: {
                    "connections": {
                        "default": {"class": "unicon.Unicon"},
                        "a": {"ip": ip, "port": port, "protocol": "telnet"},
                    },
                    "credentials": {
                        "default": {"password": "lab123", "username": "lab"},
                        "enable": {"password": "lab123"},
                    },
                    "os": "iosxr",
                    "type": "router",
                    "custom": {
                        "execute_timeout": 80,
                        "configure_timeout": 65,
                        "abstraction": {"order": ["os"]},
                    },
                }
            }
        else:
            device_dict = {
                device_name: {
                    "connections": {
                        "default": {"class": "unicon.Unicon"},
                        "a": {"ip": ip, "port": port, "protocol": "telnet"},
                        "a": {"ip": ip, "port": port2, "protocol": "telnet"},
                    },
                    "credentials": {
                        "default": {"password": "lab123", "username": "lab"},
                        "enable": {"password": "lab123"},
                    },
                    "os": "iosxr",
                    "type": "router",
                    "custom": {
                        "execute_timeout": 80,
                        "configure_timeout": 65,
                        "abstraction": {"order": ["os"]},
                    },
                }
            }
        yaml_dict["devices"][device_name] = device_dict[device_name]
    return yaml_dict


def write_yaml_dict_to_yaml_file(source_yaml_dict, dest_filename):
    with open(dest_filename, "w") as outfile:
        yaml.dump(source_yaml_dict, outfile, default_flow_style=False)


def add_tgen_info_to_device_objects_from_ws(ws, devices):
    col = 1
    for row in range(2, 1000):
        device = ws.cell(row=row, column=col).value
        if device is None:
            break
        port = ws.cell(row=row, column=col + 1).value
        if port is None:
            continue
        device_name = device + "_" + str(port)
        tgen = ws.cell(row=row, column=col + 4).value
        devices[device_name].tgen = str(tgen)