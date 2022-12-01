#!/usr/bin/env python3
 ###############################################################################
 # # License
 # <b>Copyright 2022 Silicon Laboratories Inc. www.silabs.com</b>
 ###############################################################################
 #
 # SPDX-License-Identifier: Zlib
 #
 # The licensor of this software is Silicon Laboratories Inc.
 #
 # This software is provided 'as-is', without any express or implied
 # warranty. In no event will the authors be held liable for any damages
 # arising from the use of this software.
 #
 # Permission is granted to anyone to use this software for any purpose,
 # including commercial applications, and to alter it and redistribute it
 # freely, subject to the following restrictions:
 #
 # 1. The origin of this software must not be misrepresented; you must not
 #    claim that you wrote the original software. If you use this software
 #    in a product, an acknowledgment in the product documentation would be
 #    appreciated but is not required.
 # 2. Altered source versions must be plainly marked as such, and must not be
 #    misrepresented as being the original software.
 # 3. This notice may not be removed or altered from any source distribution.
 #
 ##############################################################################/

from matplotlib import pyplot
import datetime
import os
import argparse

# Run "python app.py --help" for help

DEFAULT_DISTANCE_FILE = os.path.join(os.path.dirname(__file__), '../bt_abr_host_initiator/exe/distance.txt')
DEFAULT_SERIAL_DEVICE = ""
DEFAULT_READ_COUNT = 100



def process_soc_init(init_serial_port = "", numberOfreadings=10):
    import serial
    import xlsxwriter
    import sys
    try:
        ser = serial.Serial(port=init_serial_port, baudrate=115200)
    except:
        print("Serial port could not be opened")
    else:
        last_new_distance_time = datetime.datetime.now()
        row = 0
        column = 0
        workbook = xlsxwriter.Workbook('Distance.xlsx')
        worksheet = workbook.add_worksheet()
        while(True):
            if ser.in_waiting > 0:
                new_dist = ser.read(ser.in_waiting)
                # Try reading distance
                try:
                    data_str = new_dist[2:-2].decode("ascii")
                    distance = str(int(data_str) / 1000.0)
                except:
                    distance = ''
                # Check if reading the distance was successful
                if (distance == ''):
                    time_delta = datetime.datetime.now() - last_new_distance_time
                    # if (time_delta.seconds > dplot_params.seconds_to_wait_for_exit):
                    #     break
                else:
                    last_new_distance_time = datetime.datetime.now()

                    if distance != 0:
                        date_time_str = last_new_distance_time.strftime("%Y-%m-%d %H:%M:%S")
                        worksheet.write(row, 0, date_time_str)
                        worksheet.write(row, 1, distance)
                        row += 1
                        print(distance)
                        if row == numberOfreadings:
                            workbook.close()
                            sys.exit()
        
def main(**args):
    #global dplot_params

    parser = argparse.ArgumentParser(description = "Connect the initiator to the computer and run this script.")
    parser.add_argument("--serial", default=DEFAULT_SERIAL_DEVICE, help='initiator serial port')
    parser.add_argument("--readcount", default=DEFAULT_READ_COUNT, help='Number of desired distance read count')
    args = parser.parse_args()
    
    process_soc_init(args.serial, int(args.readcount))

    input("Press Enter to exit...")

if __name__ == '__main__':
    main()