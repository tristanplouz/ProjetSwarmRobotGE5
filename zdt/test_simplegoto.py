import dronekit
import time
import math
master=dronekit.connect("/dev/ttyACM0")
print("wait 2s")
time.sleep(2)
print(master.version)
master.mode = dronekit.VehicleMode("GUIDED")
chk1=dronekit.LocationGlobalRelative(48.5791376, 7.7657461, 30)
chk2=dronekit.LocationGlobalRelative(48.5790596, 7.7665722, 30)
print("wait 5s")
time.sleep(5)
master.simple_goto(chk1, groundspeed=2)
print("go at 2m/s to ",chk1)
for i in range(0,50):
	print(master.velocity)
	print(math.sqrt(math.pow(master.velocity[0],2)+math.pow(master.velocity[1],2)+math.pow(master.velocity[2],2)),str("m/s"))
	time.sleep(1)
print("gone")
master.simple_goto(chk2, groundspeed=4.0)
print("go at 4m/s to ",chk2)
time.sleep(50)
master.simple_goto(chk1,groundspeed=0.75)
print("go at 0.75m/s to ",chk1)
time.sleep(50)
print("fin de chantier")

