# /home/user/Raspberry-Pi-1-NAS/.venv/bin/python /home/user/Raspberry-Pi-1-NAS/examples/mqtt_sender.py
#
# https://www.emqx.com/en/blog/comparision-of-python-mqtt-client
# https://github.com/eclipse/paho.mqtt.python/tree/master/examples
import paho.mqtt.client as mqtt
from time import sleep

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/lcd"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
client.loop_start()

index = 0
while True:
    line1 = "Hello #" + str(index)
    line2 = "from Python"

    payload = line1 + "|" + line2

    client.publish(MQTT_TOPIC, payload=payload, qos=0, retain=False)
    print(f"sent {payload}")
    index += 1

    sleep(1)
