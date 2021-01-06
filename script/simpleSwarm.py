import dronekit
import time
import sys
import atexit
from math import *


def failsafe():
    "Methode permettant de mettre en securité les buggys"
    print("Deconnection")
    slave.groundspeed = 0
    master.groundspeed = 0
    print("Groundspeed = 0")
    slave.mode = dronekit.VehicleMode("HOLD")
    master.mode = dronekit.VehicleMode("HOLD")
    print("HOLD")
#    slave.disarm()
#    master.disarm()
#    print("Disarm")
    slave.close()
    master.close()
    print("Goodbye")
    

def destinationPoint(lat_org,lon_org,d=2,teta=180):
    "Methode permettant de calculer une position gps a partir d'une position GPS d'une distance et d'un cap"
    R=6371009
    teta*=pi/180
    lat_org*=pi/180
    lon_org*=pi/180
    lat = asin(sin(lat_org)*cos(d/R)+cos(lat_org)*sin(d/R)*cos(teta))
    lon = lon_org+atan2(sin(teta)*sin(d/R)*cos(lat_org),cos(d/R)-sin(lat_org)*sin(lat))
    lat*=180/pi
    lon=((lon+540)%360-180)*180/pi
    print("targeted: "+str(lat)+"  "+str(lon))
    return dronekit.LocationGlobal(lat,lon,0) #return a Location Object
    
def haversineDistance(lat1,lon1,lat2,lon2):
    "Haversine formula to calculate a distance"
    R=6371009
    lat1 *= pi/180
    lon1 *= pi/180
    lat2 *= pi/180
    lon2 *= pi/180
    
    dlon = lon2-lon1
    dlat = lat2-lat1
    
    a = sin(dlat/2)**2+cos(lat1)*cos(lat2)*(sin(dlon/2))**2
    d = 2 * R *asin(sqrt(a))
    print("Haversine Distance Calculated: "+str(d))
    
    #theta = atan2(cos(lat2)*sin(dlon),cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(dlon)
    #theta *= 180/pi
    return d

atexit.register(failsafe)

print("Connection au slave....")
slave = dronekit.connect("/dev/ttyUSB0",baud=56700) #Le master est relié en utilisant une télémétrie sur un Port USB
time.sleep(3)
if slave is not null:
    print("Slave connecté: "+str(slave.version))
else:
    print("Slave non connecté, quit.")
    sys.exit()

print("Connection au master....")
master = dronekit.connect("/dev/ttyACM0",baud=56700) #Le master est relié directement en USB
time.sleep(3)
if master is not null:
    print("Master connecté: "+str(master.version))
else:
    print("Master non connecté, quit.")
    sys.exit()

print("On attend un peu pour tout récupérer.")
time.sleep(2)

rep = input("Armer le slave (Yes/No)")
if(rep=="Y" or rep=="y"):
    slave.arm()
    slave.mode = dronekit.VehicleMode("HOLD")
    print("Slave armé et en mode HOLD")
    
rep = input("Armer le master (Yes/No)")
if(rep=="Y" or rep=="y"):
    master.arm()
    master.mode = dronekit.VehicleMode("MANUAL")
    print("Master armé et en mode HOLD")
    
#print("Slave: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")
#print("Master: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")

#Paramètre de controle de la position relative
d=2
theta=180

#Paramètre de l'automatique
ts=0.2
vmax=1.5

#Variable de fonctionnement
veloc = 0
first_stop = False

#Sécurité sur la précision du GPS, on attend au moins 17 satellites par drone avant de lancer le swarm
while master.gps_0.satellites_visible < 17 or slave.gps_0.satellites_visible < 17 :
    print("Number of satellites unsatisfied : Master " 
        + str(master.gps_0.satellites_visible) + " - Slave "
        + str(slave.gps_0.satellites_visible))
    time.sleep(2)

#Question bloquante avant de lancer le swarm
input("Good satellites. Let's go ?")

master.mode = dronekit.VehicleMode("MANUAL")

while 1:
    #print("Get info")
    latM=master.location.global_frame.lat
    lonM=master.location.global_frame.lon
    
    latS = slave.location.global_frame.lat
    lonS = slave.location.global_frame.lon
    
    dact = haversineDistance(latM,lonM,latS,lonS)

    bearing = master.heading

    if veloc > 0.5 :
        first_stop = False
       # print("Let's go")
        slave.mode = dronekit.VehicleMode("GUIDED")
        slave.simple_goto(destinationPoint(latM,lonM,d,theta+bearing),groundspeed=vmax)
    else :
        print("SAFE STOP")
        if not first_stop :
            first_stop = True
     #       print("Let's go")
            slave.simple_goto(destinationPoint(latM,lonM,d,theta+bearing),groundspeed=vmax)
        else :
      #      print("HOLD")
            time.sleep(ts)
            slave.mode = dronekit.VehicleMode("HOLD")
    time.sleep(ts)
