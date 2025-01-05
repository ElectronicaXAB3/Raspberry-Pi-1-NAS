# /home/user/Raspberry-Pi-1-NAS/.venv/bin/python /home/user/Raspberry-Pi-1-NAS/Shutdown-app/main.py
#
import paho.mqtt.client as mqtt
from time import sleep
import os

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_KEYBOARD_TOPIC = "nas/keyboard"
MQTT_LCD_TOPIC = "nas/lcd"
MQTT_TIMEOUT = 10

_client = None

def main():
    mqtt_init()

    while True:
        sleep(0.5)

def mqtt_on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT server with result code: {reason_code}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "top_key_pressed":
        payload = "Shutting|down..."
        client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)
        print("Shutting down the system...")

        os.system("sudo halt")

def mqtt_init():
    global _client

    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    _client.on_connect = mqtt_on_connect
    _client.on_message = mqtt_on_message
    _client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
    _client.loop_start()

# Start the main
if __name__ == '__main__':
    try:
        print("App started")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup MQTT
        if _client:
            _client.loop_stop()
            _client.disconnect()
        print("App stopped")
