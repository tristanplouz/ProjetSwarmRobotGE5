from dronekit import connect
import time

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

while True:
        print("Master : " +str(master.attitude.pitch))
        print("Slave : " + str(slave.attitude.pitch))
        time.sleep(2)
