import asyncio
import random
import time

from quart import Quart, render_template, websocket
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from selenium.webdriver.firefox.options import Options

from EyeData import EyeData
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

options = Options()
options.page_load_strategy = 'none'

driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
driver.fullscreen_window()

app: Quart = Quart(__name__)
dispatcher: Dispatcher = Dispatcher()
eyeData: EyeData = EyeData()
lastOSCMessage: float = time.time() - 20
lastEyeTime: float = time.time() - 20
eyeAutoTime: float = 5
previousJson: str = ""
server = None
transport = None


async def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


def print_handler(address, *args):
    global lastOSCMessage
    global eyeData
    eyeData.eyeX = args[0]
    eyeData.eyeY = args[1]
    lastOSCMessage = time.time()


dispatcher.map("/xy1", print_handler)
dispatcher.set_default_handler(handler=default_handler, needs_reply_address=False)


@app.route('/')
async def eyes():  # put application's code here
    return await render_template('eyes.html')


@app.websocket("/ws")
async def ws():
    global lastOSCMessage
    global lastEyeTime
    global eyeAutoTime
    global previousJson
    global eyeData
    while True:
        currentTime = time.time()
        timeSince = currentTime - lastOSCMessage
        if timeSince > 15:
            timeSince = currentTime - lastEyeTime
            if timeSince > eyeAutoTime:
                eyeData.eyeX = random.uniform(0.3, 0.7)
                eyeData.eyeY = random.uniform(0.3, 0.7)
                eyeAutoTime = random.uniform(0.3, 4)
                lastEyeTime = time.time()
        data = eyeData.toJson()
        await websocket.send(data)
        await asyncio.sleep(0.01)

@app.before_serving
async def startup():
    global server
    global transport
    loop = asyncio.get_event_loop()
    server = AsyncIOOSCUDPServer(("0.0.0.0", 9000), dispatcher, loop)
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    driver.get("http://127.0.0.1:5000")


@app.after_serving
async def shutdown():
    global transport
    if transport is not None:
        transport.close()
    driver.quit()

if __name__ == '__main__':
    app.run(debug=True, threaded=False, use_reloader=False)
