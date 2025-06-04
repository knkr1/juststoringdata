# Tank Drive WebSocket + Web UI for Raspberry Pi 5 using gpiozero
# Folder structure:
# - main.py
# - static/index.html

# main.py
import asyncio
from aiohttp import web
from gpiozero import PWMOutputDevice

# Motor setup
speed = 0.5  # Set your overall speed (0.0 - 1.0)
left_motor = PWMOutputDevice(18)
right_motor = PWMOutputDevice(19)

def set_drive(left, right):
    left_motor.value = left * speed
    right_motor.value = right * speed
    print(f"[MOTOR] L:{left * speed:.2f} R:{right * speed:.2f}")

# WebSocket handler
async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = msg.data
            if data == "forward":
                set_drive(1, 1)
            elif data == "backward":
                set_drive(-1, -1)
            elif data == "left":
                set_drive(-1, 1)
            elif data == "right":
                set_drive(1, -1)
            elif data == "stop":
                set_drive(0, 0)
            await ws.send_str(f"Executed: {data}")
            print(f"[WS] {data}")
    return ws

# Web server
app = web.Application()
app.router.add_get('/ws', ws_handler)
app.router.add_static('/', path='static', name='static')

web.run_app(app, port=8080)
