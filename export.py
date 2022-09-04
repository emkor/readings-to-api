#!/usr/bin/env python3

import sys
import typing as t
from http.client import HTTPConnection

DEVICE = "/dev/ttyUSB0"
API_URL = "/json.htm?type=command&param=udevice&idx={}&nvalue={}&svalue=TEMP"
DEVICE_READ_SEPARATOR = "SR;"
EXPECTED_VAL_COUNT = 8


def main(device: str, host: str, port: int, auth_b64: str):
    values_int = read_metrics_from_device(device=device, separator=DEVICE_READ_SEPARATOR)
    for value_series in values_int:
        if len(value_series) == EXPECTED_VAL_COUNT:
            http_client = HTTPConnection(host=host, port=port)
            for idx, value in enumerate(value_series):
                send_values_to_api(http_client=http_client, full_url=API_URL.format(idx, value), auth_b64=auth_b64)
        else:
            print(
                f"Line: {value_series} contains {len(value_series)} values but expected {EXPECTED_VAL_COUNT}: ignoring")


def send_values_to_api(http_client: HTTPConnection, full_url: str, auth_b64: str):
    http_client.request(method="POST", headers={"Authorization": f"Basic {auth_b64}"}, url=full_url)
    resp = http_client.getresponse()
    resp_payload = resp.read().decode()
    if not (200 <= resp.status < 300):
        print(f"Error on uploading values to {full_url} by POST: {resp.status} {resp_payload}")


def read_metrics_from_device(device: str, separator: str) -> t.List[t.List[int]]:
    reads = []
    with open(device, "r") as device_file:
        for line in device_file.readlines():
            value_series = line.strip().split(separator)
            for values_str in value_series:
                values = list(filter(lambda v: len(v.strip()), values_str.split(";")))  # filter empty strings
                values_int = list(filter(lambda v: v is not None, [safe_to_int(v) for v in values]))  # filter values not being INTs
                reads.append(values_int)
        return reads


def safe_to_int(val: str) -> t.Optional[int]:
    try:
        return int(val)
    except ValueError:
        return None


if __name__ == '__main__':
    main(device=DEVICE, host=sys.argv[1], port=int(sys.argv[2]), auth_b64=sys.argv[3])
    # main(device="example.csv", host="localhost", port=80, auth_b64="testpasswd=")
