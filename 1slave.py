import dronekit
import time
import sys
from math import *

print("connection au slave....")
slave = dronekit.connect("/dev/ttyUSB0",baud=56700)
time.sleep(3)
print("Slave: "+str(slave.version))

print("Connection au master....")
master = dronekit.connect("/dev/ttyACM0",baud=56700)
time.sleep(5)
print("Master: "+str(master.version))

    
    
rep = input("Armer le slave (Yes/No)")
if(rep=="Y" or rep=="y"):
    slave.arm()
    
rep = input("Armer le master (Yes/No)")
if(rep=="Y" or rep=="y"):
    master.arm()
    
print("Slave: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")
print("Master: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")
if(slave.gps_0.fix_type>2):
    master.mode = dronekit.VehicleMode("GUIDED")
    slave.mode = dronekit.VehicleMode("GUIDED")
else:
    print("No 3D fix")
    slave.disarm()
    master.disarm()
    slave.close()
    master.close()
    sys.exit()

while 1:
    input("Run slave")
    lat=master.location.global_frame.lat
    lon=master.location.global_frame.lon
    bearing = master.heading
    slave.simple_goto(getSlavePos(lat,lon,2,180+bearing),groundspeed=0.5)
    time.sleep(5)

def getSlavePos(lat_org,lon_org,d,teta):
#implement other hemisphere work
    R=6371009
    teta*=pi/180
    lat_org*=pi/180
    lon_org*=pi/180
    lat = asin(sin(lat_org)*cos(d/R)+cos(lat_org)*sin(d/R)*cos(teta))
    lon = lon_org+atan2(sin(teta)*sin(d/R)*cos(lat_org),cos(d/R)-sin(lat_org)*sin(lat))
    lat*=180/pi
    lon=((lon+540)%360-180)*180/pi
    print("targeted: "+lat+"  "+lon)
    return dronekit.LocationGlobal(lat,lon,0)
