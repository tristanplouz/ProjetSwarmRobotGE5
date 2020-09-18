from dronekit import connect

def init():
	slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
	master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)
	return (master, slave)
