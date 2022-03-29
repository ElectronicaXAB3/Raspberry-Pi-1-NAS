import os
import sys
import psutil
import paho.mqtt.client as mqtt
from time import sleep,time
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

import timer

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_KEYBOARD_TOPIC = "nas/keyboard"
MQTT_LCD_TOPIC = "nas/lcd"

stepTimer = timer.timer()
stepTimer.start()
stepChanged = False
step = 0

shuttingDown = False

def main():
    mqtt_init()

    while True:
        if shuttingDown:
            sleep(10)
            return

        handle_app()
        sleep(0.1)

def handle_app():
    handle_step_increment()

    if step == 0:
        handle_clock()
    elif step == 1:
        handle_cpu_time()

def handle_clock():
    if stepTimer.readMs() < 800:
        return

    now = datetime.now()
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    payload = now.strftime('%d %b %Y') + "|" + now.strftime('%H:%M:%S')
    client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)
    stepTimer.reset()

def handle_cpu_time():
    if stepTimer.readMs() < 1000:
        return

    payload = "CPU load|" + str(psutil.cpu_percent()) + "%"
    client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)
    stepTimer.reset()

def handle_step_increment():
    global step, stepChanged

    if stepChanged:
        step += 1
        if (step == 2):
            step = 0

        clear_the_lcd()
        stepTimer.reset()
        stepChanged = False

def clear_the_lcd():
    client.publish(MQTT_LCD_TOPIC, payload="|", qos=0, retain=False)
    sleep(0.1)

def mqtt_on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global shuttingDown, stepChanged

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "top_key_pressed":
        shuttingDown = True
    elif message == "bottom_key_pressed":
        stepChanged = True

def mqtt_init():
    global client

    client = mqtt.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
    client.loop_start()

# Start the main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pass
