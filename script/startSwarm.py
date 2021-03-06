import dronekit
import time
import sys
import atexit
import statistics
from math import *


def failsafe():
    "Methode permettant de mettre en securité les buggys"
    print("Déconnection")
    slave.groundspeed = 0
    slave.airspeed=0
    master.groundspeed = 0
    print("Groundspeed = 0")
    slave.mode = dronekit.VehicleMode("HOLD")
    master.mode = dronekit.VehicleMode("HOLD")
    print("HOLD mode sur les deux drones")
    slave.close()
    master.close()
    print("Goodbye")
    
def destinationPoint(lat_org,lon_org,alt_org,d=2,teta=180,h=2):
    "Methode permettant de calculer une position gps a partir d'une position GPS d'une distance et d'un cap"
    
    R=6371009
    
    teta*=pi/180
    lat_org*=pi/180
    lon_org*=pi/180
    
    lat = asin(sin(lat_org)*cos(d/R)+cos(lat_org)*sin(d/R)*cos(teta))
    lon = lon_org+atan2(sin(teta)*sin(d/R)*cos(lat_org),cos(d/R)-sin(lat_org)*sin(lat))
    
    lat*=180/pi
    lon=((lon+540)%360-180)*180/pi
    alt = alt_org+h
    #print("Destination: "+str(lat)+"  "+str(lon) +" at "+str(alt)+"m")
    return dronekit.LocationGlobal(lat,lon,alt) #return a Location object
    
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
    
    #theta = atan2(cos(lat2)*sin(dlon),cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(dlon)
    #theta *= 180/pi
    return d
    
def controllerVit(dact,dobj,vmast):
    "Loopback system to control the system"
    rap = (dact-dobj)/dobj
    vmax=1.5

    if(rap<0 and rap>-0.05):
        beta = 4*abs(rap)+1
    elif(rap >= 0 and rap < 0.05):
        beta = 1
    elif(rap >= 0.05 and rap < 3.5):
        beta = 0.2/2.45*rap+(244/245)
    else:
        beta = 0 #si on est trop loin ou trop proche on arrete le buggy
    
    vit=beta*vmast
    
    if(vit>vmax):
        print("Saturation!")
        vit = vmax
    
    return vit
    
def controllerDis(dact,dobj):
    rap = (dact-dobj)/dobj
    
    if(rap<0 and rap>-0.05):
        beta = 5*abs(rap)+1
    elif(rap >= 0 and rap < 0.05):
        beta = 1
    elif(rap >= 0.05 and rap < 3.5):
        beta = -0.5/2.45*rap+(2.475/2.45)
    else:
        beta = 1 #Si on est trop loin ou trop proche le buggy est arrété par le controleur en vitesse
        
    d=beta*dobj
    
    return d
    
atexit.register(failsafe)

print("Connection au slave....")
slave = dronekit.connect("/dev/ttyUSB0",baud=56700) #Le master est relié en utilisant une télémétrie sur un Port USB
time.sleep(3)
print("Slave connecté: "+str(slave.version))


print("Connection au master....")
master = dronekit.connect("/dev/ttyACM0",baud=56700) #Le master est relié directement en USB
time.sleep(3)
print("Master connecté: "+str(master.version))


print("On attend un peu pour tout récupérer.")
time.sleep(2)

rep = input("Armer le slave (Yes/No)")
if(rep=="Y" or rep=="y"):
    slave.arm()
    slave.mode = dronekit.VehicleMode("HOLD")
    print("Slave armé et en mode HOLD")
    rep = input("SimpleTakeOff? (Alt or N)")
    if(rep=="N" or rep =="n"):
        pass
    else:
        slave.mode = dronekit.VehicleMode("GUIDED")
        slave.simple_takeoff(int(rep))
        time.sleep(5)
    
rep = input("Armer le master (Yes/No)")
if(rep=="Y" or rep=="y"):
    master.arm()
    master.mode = dronekit.VehicleMode("MANUAL")
    print("Master armé et en mode HOLD")
    rep = input("SimpleTakeOff? (Alt or N)")
    if(rep=="N" or rep =="n"):
        pass
    else:
        master.mode = dronekit.VehicleMode("GUIDED")
        master.simple_takeoff(int(rep))
        time.sleep(5)
    
print("Slave: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")
print("Master: "+str(master.location.global_frame.lat)+" "+str(master.location.global_frame.lon)+" ")

#Définition de la position relative
d=2
theta=180
h=2

#Définition des paramètres d'échantillonage
ts=0.2

#Initialisation des variables utilisées après.
veloc = 0 #vitesse instantannée du master
masterSpeed=[0,0,0] #moyenne glissante de la vitesse du master

#Sécurité sur la précision du GPS, on attend au moins 17 satellites par drone avant de lancer le swarm
while master.gps_0.satellites_visible < 17 or slave.gps_0.satellites_visible < 17 :
    print("Number of satellites unsatisfied : Master " 
        + str(master.gps_0.satellites_visible) + " - Slave "
        + str(slave.gps_0.satellites_visible))
    time.sleep(2)

#Question bloquante avant de lancer le swarm
input("Good satellites. Let's go ?")

master.mode = dronekit.VehicleMode("MANUAL")

print("Swarm started, d="+str(d)+", theta="+str(theta)+", h="+str(h))

while 1:
    #print("Get info")
    latM=master.location.global_frame.lat
    lonM=master.location.global_frame.lon
    altM=master.location.global_frame.alt
    
    latS = slave.location.global_frame.lat
    lonS = slave.location.global_frame.lon
    altS = slave.location.global_frame.alt
    
    dact = haversineDistance(latM,lonM,latS,lonS)
    
    #print("Controller")
    bearing = master.heading
    vx,vy,vz = master.velocity
    veloc = sqrt(vx**2+vy**2+vz**2)
    
    masterSpeed.pop()
    masterSpeed.insert(0,veloc)
    velocMean = statistics.mean(masterSpeed)
    
    if velocMean > 0.55 :
        slave.mode = dronekit.VehicleMode("GUIDED") #Changement de Mode
        slaveSpeed=controllerVit(dact,d,velocMean)
        slave.groundspeed = slaveSpeed #Definition de la vitesse
        slave.airspeed = slaveSpeed #Definition de la vitesse
        
        targPos = controllerDis(dact,d) #Calcul de la distance corrigée
        targetBearing = (bearing+theta)%360
        
        print("\r V_inst : " + str(round(veloc,2))+"m/s (mean:"+str(round(velocMean,2))+
            "m/s)|SlvSpd "+str(round(slaveSpeed,3))+"m/s|"
            +str(round(dact,4))+"m, tgt:"+str(round(targPos,4))+"m|"+str(targetBearing),sep='', end='', flush=True)
        try:
            slave.simple_goto(destinationPoint(latM,lonM,altM,targPos,targetBearing,h)) #C'est parti
        except:
            print("Not send!")
    else :
        print("\r Arrêt du à un arrêt du master\t\t\t\t\t",sep='', end='', flush=True)
        slave.mode = dronekit.VehicleMode("HOLD")
    time.sleep(ts)
