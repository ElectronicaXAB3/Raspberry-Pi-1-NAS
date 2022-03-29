import os
import sys
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
stepOnce = True
step = 0

def main():
    mqtt_init()

    while True:
        handle_step_change()
        sleep(0.1)

def handle_step_change():
    global stepOnce, step

    """ if stepOnce:
        step += 1
        step %= 2 """

    # The clock
    if step == 0:
        if stepOnce:
            client.publish(MQTT_LCD_TOPIC, payload="|", qos=0, retain=False)
            sleep(0.1)
            stepTimer.reset()
            stepOnce = False

        if stepTimer.readMs() > 900:
            now = datetime.now()
            # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
            payload = now.strftime('%d %b %Y') + "|" + now.strftime('%H:%M:%S')
            client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)
            stepTimer.reset()

def mqtt_on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global stepOnce

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "bottom_key_pressed":
        stepOnce = True

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

