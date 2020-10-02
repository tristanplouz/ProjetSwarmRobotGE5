#!/usr/bin/python3.7

import sys
from dronekit import connect

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

def main():
	master_lat = str(master.location.global_frame.lat)
	master_lon = str(master.location.global_frame.lon)
	master_alt = str(master.location.global_frame.alt)

	slave_lat = str(slave.location.global_frame.lat)
	slave_lon = str(slave.location.global_frame.lon)
	slave_alt = str(slave.location.global_frame.alt)

	sys.stdout.write('{"mla":' + master_lat + ',"mlo":' + master_lon + ',"mal":' + master_alt
	   	       + ',"sla":' + slave_lat  + ',"slo":' + slave_lon  + ',"sal":' + slave_alt + '}')

	sys.stdout.flush()
	sys.exit(0)
main()
