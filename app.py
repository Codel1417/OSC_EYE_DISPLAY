import asyncio
from quart import Quart, render_template, websocket, g
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from EyeData import EyeData

app = Quart(__name__)
dispatcher = Dispatcher()
eyeData = EyeData()

async def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


def print_handler(address, *args):
    print(f"{address}: {args}")
    eyeData.eyeX = args[0]
    eyeData.eyeY = args[1]


dispatcher.map("/xy1", print_handler)
dispatcher.set_default_handler(handler=default_handler, needs_reply_address=False)


@app.route('/')
async def eyes():  # put application's code here
    return await render_template('eyes.html')


@app.websocket("/ws")
async def ws():
    previousJson = g.get("previousJson")
    while True:
        data = eyeData.toJson()
        if data != previousJson:
            await websocket.send(data)
            g.setdefault("previousJson",previousJson)


@app.before_serving
async def startup():
    print("Starting OSC")
    loop = asyncio.get_event_loop()
    server = AsyncIOOSCUDPServer(("0.0.0.0", 9000), dispatcher, loop)
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    g.setdefault("osc", transport)


@app.after_serving
async def shutdown():
    print("Stopping OSC")
    transport = g.get("osc")
    if transport != None:
        transport.close()


if __name__ == '__main__':
    app.run(debug=True)
