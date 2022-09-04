# readings-to-api
one-shot script for passing reading from USB device to domoticz server

should be run in cron (periodically)

## requirements
`python3` on PATH (python should be in version >=3.7)

## usage
How to use:
`export.py <DEVICE PATH> <DOMOTICZ HOST/IP> <DOMOTICZ PORT> <BASIC AUTH TOKEN IN BASE64>`

Example:
`export.py /dev/ttyUSB0 localhost 80 QWxhZGRpbjpvcGVuIHNlc2FtZQ==`

How to get auth_b64: [Authorization](https://domoticz.com/wiki/Domoticz_API/JSON_URL's#Authorization)
