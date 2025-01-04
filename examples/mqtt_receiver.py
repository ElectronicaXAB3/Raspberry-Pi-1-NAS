# /home/user/Raspberry-Pi-1-NAS/.venv/bin/python /home/user/Raspberry-Pi-1-NAS/examples/mqtt_receiver.py
#
# https://www.emqx.com/en/blog/comparision-of-python-mqtt-client
# https://github.com/eclipse/paho.mqtt.python/tree/master/examples
import paho.mqtt.client as mqtt
from time import sleep

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/lcd"

# The callback function of connection
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code: {reason_code}")
    client.subscribe(MQTT_TOPIC)

# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode('UTF-8'))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
client.loop_start()

while True:
    sleep(0.5)
