# /home/user/Raspberry-Pi-1-NAS/.venv/bin/python /home/user/Raspberry-Pi-1-NAS/Keyboard-app/main.py
#
# https://abyz.me.uk/lg/py_lgpio.html
import lgpio
import paho.mqtt.client as mqtt
from time import sleep

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/keyboard"
MQTT_TIMEOUT = 10

KEY_TOP = 22
KEY_BOTTOM = 17

_client = None
_gpioh = None
_top_key_prev_state = 1
_bottom_key_prev_state = 1

def main():
    mqtt_init()
    keys_init()

    while True:
        read_keys()
        sleep(0.2)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT server with result code: {reason_code}")

def top_key_pressed():
    print("Pressed top key")
    _client.publish(MQTT_TOPIC, payload="top_key_pressed", qos=0, retain=False)

def bottom_key_pressed():
    print("Pressed bottom key")
    _client.publish(MQTT_TOPIC, payload="bottom_key_pressed", qos=0, retain=False)

def mqtt_init():
    global _client
    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    _client.on_connect = on_connect
    _client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
    _client.loop_start()

def keys_init():
    global _gpioh

    # Initialize GPIO
    _gpioh = lgpio.gpiochip_open(0)
    print(f"GPIO chip opened with handle: {_gpioh}")

    # Get GPIO info
    chip_info = lgpio.gpio_get_chip_info(_gpioh)
    print(f"Chip info = status: {chip_info[0]}, lines: {chip_info[1]}, name: {chip_info[2]}, label: {chip_info[3]}")

    # Configure pins as inputs with pull-ups
    lgpio.gpio_claim_input(_gpioh, KEY_TOP, lgpio.SET_PULL_UP)
    lgpio.gpio_claim_input(_gpioh, KEY_BOTTOM, lgpio.SET_PULL_UP)

def read_keys():
    global _top_key_prev_state, _bottom_key_prev_state

    top_key_state = lgpio.gpio_read(_gpioh, KEY_TOP)
    bottom_key_state = lgpio.gpio_read(_gpioh, KEY_BOTTOM)

    if top_key_state == 0 and top_key_state != _top_key_prev_state:
        _top_key_prev_state = top_key_state
        top_key_pressed()
    if bottom_key_state == 0 and bottom_key_state != _bottom_key_prev_state:
        _bottom_key_prev_state = bottom_key_state
        bottom_key_pressed()

    if top_key_state == 1:
        _top_key_prev_state = top_key_state
    if bottom_key_state == 1:
        _bottom_key_prev_state = bottom_key_state

# Start the main
if __name__ == '__main__':
    try:
        print("App started")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup GPIO and MQTT
        if _gpioh:
            lgpio.gpiochip_close(_gpioh)
        if _client:
            _client.loop_stop()
            _client.disconnect()
        print("App stopped")
