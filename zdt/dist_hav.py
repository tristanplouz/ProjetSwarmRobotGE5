from dronekit import connect
import time
from haversine import haversine, Unit

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

while True:
	coord_master = (master.location.global_frame.lat, 
			master.location.global_frame.lon)
	coord_slave = (slave.location.global_frame.lat,
			slave.location.global_frame.lon)
	dist = haversine(coord_master, coord_slave, unit='m')
	print("Distance : " + str(dist))
	time.sleep(1)
