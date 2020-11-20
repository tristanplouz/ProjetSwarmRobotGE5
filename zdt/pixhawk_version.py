from dronekit import connect
import asyncio
import websockets
import time
import json

slave = connect('/dev/ttyUSB0',baud=56700,wait_ready=False)
master = connect('/dev/ttyACM0',baud=56700,wait_ready=False)

async def processus(websocket, path):
    await bat(websocket)
    while True :
        message = await websocket.recv()
        data = json.loads(message)
        if (data["type"]=="GO"):
            if (data["ctn"]=="c'est parti"):
                print("OK j'y vais !")

async def bat(websocket):
    message = {
        "type": "version",
	"ctn" : str(master.version)
    }
    y = json.dumps(message)
    await websocket.send(y)
    time.sleep(2)

start_server = websockets.serve(processus, "172.20.10.6", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
