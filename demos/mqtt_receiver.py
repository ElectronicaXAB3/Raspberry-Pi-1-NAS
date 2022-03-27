# https://www.emqx.com/en/blog/comparision-of-python-mqtt-client
# https://github.com/eclipse/paho.mqtt.python/tree/master/examples
import paho.mqtt.client as mqtt
from time import sleep

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/lcd"

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode('UTF-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
client.loop_start()

while True:
    sleep(2.5)
