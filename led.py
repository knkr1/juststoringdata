from gpiozero import PWMLED
from time import sleep

led = PWMLED(18)

try:
    while True:
        for value in range(0, 101, 5):
            led.value = value / 100
            sleep(0.05)
        for value in range(100, -1, -5):
            led.value = value / 100
            sleep(0.05)
except KeyboardInterrupt:
    led.off()
