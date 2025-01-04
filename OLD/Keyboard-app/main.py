# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/keyboard"

KEY_TOP = 22
KEY_BOTTOM = 17

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
client.loop_start()

def main():
    keys_init()

    while True:
        sleep(1)

def key_top_pressed(channel):
    print(f"Pressed top key")
    client.publish(MQTT_TOPIC, payload="top_key_pressed", qos=0, retain=False)

def key_bottom_pressed(channel):
    print(f"Pressed bottom key")
    client.publish(MQTT_TOPIC, payload="bottom_key_pressed", qos=0, retain=False)

def keys_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(KEY_TOP, GPIO.IN)
    GPIO.setup(KEY_BOTTOM, GPIO.IN)

    GPIO.add_event_detect(KEY_TOP, GPIO.FALLING, callback=key_top_pressed)
    GPIO.add_event_detect(KEY_BOTTOM, GPIO.FALLING, callback=key_bottom_pressed)

# Start the main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
