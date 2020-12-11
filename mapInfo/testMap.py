import asyncio
import websockets
import time
import dronekit

print("Connection au slave....")
slave = dronekit.connect("/dev/ttyUSB0",baud=56700)
time.sleep(3)
print("Slave: "+str(slave.version))

print("Connection au master....")
master = dronekit.connect("/dev/ttyACM0",baud=56700)
time.sleep(5)
print("Master: "+str(master.version))

async def processus(websocket, path):
    message = await websocket.recv()
    print(message)
    latM,lonM,headM =master.location.global_frame.lat,master.location.global_frame.lon,master.heading
    latS,lonS,headS = slave.location.global_frame.lat,slave.location.global_frame.lon,slave.heading
    while True:
        await websocket.send('{"type":"masterP","lat":'+str(lat)+',"lon":'+str(lon)+',"head":'+str(head)+'}')
        await websocket.send(
        time.sleep(5)

start_server = websockets.serve(processus, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



'''

'''