import paho.mqtt.client as mqtt
from time import sleep
import os

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_KEYBOARD_TOPIC = "nas/keyboard"
MQTT_LCD_TOPIC = "nas/lcd"

def main():
    mqtt_init()

    while True:
        sleep(1)

def mqtt_on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "top_key_pressed":
        payload = "Shutting|down..."
        client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)

        os.system("shutdown -h now")

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
