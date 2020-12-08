import dronekit
import time
import sys
from math import *

def getSlavePos(lat_org,lon_org,d=2,teta=180):
    R=6371009
    teta*=pi/180
    lat_org*=pi/180
    lon_org*=pi/180
    lat = asin(sin(lat_org)*cos(d/R)+cos(lat_org)*sin(d/R)*cos(teta))
    lon = lon_org+atan2(sin(teta)*sin(d/R)*cos(lat_org),cos(d/R)-sin(lat_org)*sin(lat))
    lat*=180/pi
    lon=((lon+540)%360-180)*180/pi
    print("targeted: "+str(lat)+"  "+str(lon))
    return dronekit.LocationGlobal(lat,lon,0)

print("Connection au slave....")
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
    master.mode = dronekit.VehicleMode("MANUAL")
    slave.mode = dronekit.VehicleMode("HOLD")
else:
    print("No 3D fix")
    slave.disarm()
    master.disarm()
    slave.close()
    master.close()
    sys.exit()

d=0.5
theta=180
ts=1
gs=2

while master.gps_0.satellites_visible < 17 or slave.gps_0.satellites_visible < 17 :
    print("Number of satellites unsatisfied : Master " 
        + str(master.gps_0.satellites_visible) + " - Slave "
        + str(slave.gps_0.satellites_visible))
    time.sleep(2)

input("Good satellites. Let's go ?")
while 1:
    lat=master.location.global_frame.lat
    lon=master.location.global_frame.lon
    bearing = master.heading
    vx,vy,vz = master.velocity
    veloc = sqrt(vx**2+vy**2+vz**2)
    print("Velocity : " + str(veloc))
    if veloc > 1 :
        first_stop = False
        slave.mode = dronekit.VehicleMode("GUIDED")
        slave.simple_goto(getSlavePos(lat,lon,d,theta+bearing),groundspeed=gs)
    else :
        if !first_stop :
            first_stop = True
            slave.simple_goto(getSlavePos(lat,lon,d,theta+bearing),groundspeed=gs)
        else :
            slave.mode = dronekit.VehicleMode("HOLD")
    time.sleep(ts)
