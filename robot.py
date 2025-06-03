# Tank Drive Control with Web Interface and WebSocket

import RPi.GPIO as GPIO
import asyncio
import websockets
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

# Motor pins (PWM)
LEFT_MOTOR_PIN = 18
RIGHT_MOTOR_PIN = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_MOTOR_PIN, 100)
right_pwm = GPIO.PWM(RIGHT_MOTOR_PIN, 100)
left_pwm.start(0)
right_pwm.start(0)

# Global state
status = "Idle"

# Control functions
def move_forward():
    left_pwm.ChangeDutyCycle(70)
    right_pwm.ChangeDutyCycle(70)

def move_backward():
    left_pwm.ChangeDutyCycle(30)
    right_pwm.ChangeDutyCycle(30)

def turn_left():
    left_pwm.ChangeDutyCycle(30)
    right_pwm.ChangeDutyCycle(70)

def turn_right():
    left_pwm.ChangeDutyCycle(70)
    right_pwm.ChangeDutyCycle(30)

def stop():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)

# WebSocket handler
async def control(websocket):
    global status
    async for message in websocket:
        if message == "forward":
            move_forward()
            status = "Moving forward"
        elif message == "backward":
            move_backward()
            status = "Moving backward"
        elif message == "left":
            turn_left()
            status = "Turning left"
        elif message == "right":
            turn_right()
            status = "Turning right"
        elif message == "stop":
            stop()
            status = "Stopped"
        await websocket.send(f"Status: {status}")

# Start WebSocket server
def start_ws():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(control, "0.0.0.0", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# Basic HTML interface
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tank Drive Control</title>
    <style>
        button { width: 100px; height: 100px; font-size: 20px; margin: 10px; }
    </style>
</head>
<body>
    <h1>Tank Drive Control</h1>
    <p>Status: <span id="status">Idle</span></p>
    <button onclick="send('forward')">Forward</button><br>
    <button onclick="send('left')">Left</button>
    <button onclick="send('stop')">Stop</button>
    <button onclick="send('right')">Right</button><br>
    <button onclick="send('backward')">Backward</button>

    <script>
        let ws = new WebSocket('ws://' + location.hostname + ':6789');
        ws.onmessage = msg => document.getElementById('status').innerText = msg.data;
        function send(cmd) { ws.send(cmd); }
    </script>
</body>
</html>
'''

class WebHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_error(404, "Not Found")

# Start HTTP server
def start_http():
    server = HTTPServer(("0.0.0.0", 80), WebHandler)
    server.serve_forever()

try:
    threading.Thread(target=start_http).start()
    threading.Thread(target=start_ws).start()
except KeyboardInterrupt:
    stop()
    GPIO.cleanup()
