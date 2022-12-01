# HADR_Initiatorlog

This is meant to be used with the Silicon Labs HADR SOC initiator demo.

Clone this repo to:
gecko_sdk/app/bluetooth/example_host/

Usage:
python3 SerialtoExcel.py --serial /dev/tty.usbmodem0004402351551 --readcount 15

where --serial is the desired Serial port and --readcount is the desired number of distance samples

It will output the samples to the screen and also create "Distance.xlsx" file.