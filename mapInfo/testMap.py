import asyncio
import websockets
import time
import dronekit

def connect()
    print("Connection au slave....")
    slave = dronekit.connect("/dev/ttyUSB0",baud=56700)
    time.sleep(3)
    print("Slave: "+str(slave.version))

    print("Connection au master....")
    master = dronekit.connect("/dev/ttyACM0",baud=56700)
    time.sleep(5)
    print("Master: "+str(master.version))
    return slave,master

async def processus(websocket, path):
    message = await websocket.recv()
    print(message)
    
    while True:
        latM,lonM,headM = master.location.global_frame.lat,master.location.global_frame.lon,master.heading
        latS,lonS,headS = slave.location.global_frame.lat,slave.location.global_frame.lon,slave.heading
        print("master "+headM)
        print("slave "+headS)
        await websocket.send('{"type":"masterP","lat":'+str(latM)+',"lon":'+str(lonM)+',"head":'+str(headM)+'}')
        await websocket.send('{"type":"slaveP","lat":'+str(latS)+',"lon":'+str(lonS)+',"head":'+str(headS)+'}')
        time.sleep(5)

slave,master = connect()
start_server = websockets.serve(processus, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



'''

'''
