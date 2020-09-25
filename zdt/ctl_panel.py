from dronekit import connect
import time

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

print('|                            Master                          ||                             Slave                         |')
print('|  Pitch  |   Yaw   |   Roll   |   Lat   |   Lon   |   Alt   ||  Pitch  |   Yaw   |   Roll   |   Lat  |   Lon   |   Alt   |')

while True:
	print('\r|'+str(round(master.attitude.pitch,6)).center(9)+'|'+str(round(master.attitude.yaw,6)).center(9)+'|'+str(round(0,6)).center(9)+' |'+str(round(master.location.global_frame.lat,6)).center(9)+'|'+str(round(master.location.global_frame.lon,6)).center(9)+'|'+str(round(master.location.global_frame.alt,6)).center(9)+'||'+
		    str(round(slave.attitude.pitch,6)).center(9)+'|'+str(round(slave.attitude.yaw,6)).center(9)+'|'+str(round(slave.attitude.roll,6)).center(9)+' |'+str(round(0,6)).center(9)+'|'+str(round(0,6)).center(9)+'|'+str(round(0,6)).center(9)+'|',sep='', end='', flush=True)
#        print("Master : " +str(master.attitude.pitch))
#        print("Slave : " + str(slave.attitude.pitch))
        time.sleep(0.5)
