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
    print("Haversine distance: "+str(d))
    
    #theta = atan2(cos(lat2)*sin(dlon),cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(dlon)
    #theta *= 180/pi
    return d
    
def controllerVit(dact,dobj,vmast):
    "Loopback system to control the system"
    rap = (dact-dobj)/dobj
    vmax=4

    if(rap<0 and rap>-0.05):
        beta = 4*abs(rap)+1
    elif(rap >= 0 and rap < 0.05):
        beta = 1
    elif(rap >= 0.05 and rap < 2.5):
        beta = 0.2/2.45*rap+(244/245)
    else:
        beta = 0 #si on est trop loin ou trop proche on arrete le buggy
    
    vit=beta*vmast
    
    if(vit>vmax):
        print("Saturation!")
        vit = vmax
        
    print("Corrected speed: "+vit)
    
    return vit
    
def controllerDis(dact,dobj):
    rap = (dact-dobj)/dobj
    
    if(rap<0 and rap>-0.05):
        beta = 5*abs(rap)+1
    elif(rap >= 0 and rap < 0.05):
        beta = 1
    elif(rap >= 0.05 and rap < 2.5):
        beta = 0.5/2.45*rap-(244/245)
    else:
        beta = 1 #Si on est trop loin ou trop proche le buggy est arrété par le controleur en vitesse
        
    d=beta*dobj
    
    print("Corrected distance: "+d)
    
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

print("Swarm started, d="+d+", theta="+theta+", h="+h)

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
    if True:
        if veloc > 0.5 :
            first_stop = False
            slave.mode = dronekit.VehicleMode("GUIDED") #Changement de Mode
            slaveSpeed=controllerVit(dact,d,velocMean)
            slave.groundspeed=slaveSpeed #Definition de la vitesse
            slave.airspeed=slaveSpeed #Definition de la vitesse
            
            targPos = controllerDis(dact,d)#Calcul de la distance corrigée
            print("\r Velocity inst : " + str(veloc)+"m/s (moyenne:"+velocMean+"m/s) ||"
                +str(dact)+"m actuellement, target "+targPos+"m || SlaveSpeed: "+slaveSpeed+"m/s",sep='', end='', flush=True)
            
            slave.simple_goto(destinationPoint(latM,lonM,altM,targPos,theta+bearing,h))#C'est parti
        else :
            print("\r Velocity inst : " + str(veloc)+"(moyenne:"+velocMean+")",sep='', end='', flush=True)
            if not first_stop :
                print("Arrêt du master detecté")
                first_stop = True
         #       print("Let's go")
                slave.groundspeed=controllerVit(dact,d,velocMean) #Definition de la vitesse
                slave.airspeed=controllerVit(dact,d,velocMean) #Definition de la vitesse
                targPos = controllerDis(dact,d)#Calcul de la distance corrigée
                slave.simple_goto(destinationPoint(latM,lonM,altM,targPos,theta+bearing,h))#C'est parti
            else :
          #      print("HOLD")
                time.sleep(ts)
                slave.mode = dronekit.VehicleMode("HOLD")
    else:
        if statistics.mean(masterSpeed) > 0.5 :
            slave.mode = dronekit.VehicleMode("GUIDED") #Changement de Mode
            slave.groundspeed=controllerVit(dact,d,statistics.mean(masterSpeed)) #Definition de la vitesse
            slave.airspeed=controllerVit(dact,d,statistics.mean(masterSpeed)) #Definition de la vitesse
            
            targPos = controllerDis(dact,d)#Calcul de la distance corrigée
            print("\r Velocity inst : " + str(veloc)+"(moyenne:"+statistics.mean(masterSpeed)+") "+str(dact)+"m actuellement, target "+targPos+"m",sep='', end='', flush=True)            
            slave.simple_goto(destinationPoint(latM,lonM,altM,targPos,theta+bearing,h))#C'est parti
        else :
            print("\r Arrêt du à un arrêt du master",sep='', end='', flush=True)
            slave.mode = dronekit.VehicleMode("HOLD")
    time.sleep(ts)
