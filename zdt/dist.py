from dronekit import connect
import time
import math

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

while True:
	dx = master.location.global_frame.lon - slave.location.global_frame.lon
	dy = master.location.global_frame.lat - slave.location.global_frame.lat
	dz = master.location.global_frame.alt - slave.location.global_frame.alt
	dist = math.sqrt(pow(dx,2)+pow(dy,2)+pow(dz,2))
	print("Distance : " + str(dist))
	time.sleep(1)
