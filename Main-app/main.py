# /home/user/Raspberry-Pi-1-NAS/.venv/bin/python /home/user/Raspberry-Pi-1-NAS/Main-app/main.py
#
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.dont_write_bytecode = True

import requests
import psutil
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
from timer import ElapsedTimer

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_KEYBOARD_TOPIC = "nas/keyboard"
MQTT_LCD_TOPIC = "nas/lcd"
MQTT_TIMEOUT = 10

_stepChanged = False
_step = 0
_shuttingDown = False
_client = None
_clock_timer = ElapsedTimer(1.0)
_cpu_and_mem_timer = ElapsedTimer(1.0)
_ip_address_timer = ElapsedTimer(2.0)

def main():
    mqtt_init()

    while True:
        sleep(0.1)

        if _shuttingDown:
            continue

        handle_app()

def handle_app():
    handle_step_increment()

    if _step == 0:
        handle_clock()
    elif _step == 1:
        handle_cpu_load_and_memory_usage()
    elif _step == 2:
        handle_external_ip_address()

def handle_clock():
    if _clock_timer.elapsed():
        now = datetime.now()

        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        date = now.strftime('%d %b %Y')
        time = now.strftime('%H:%M:%S')

        # Replace months names from US to Romanian
        date = date.replace("Jan", "Ian")
        date = date.replace("May", "Mai")
        date = date.replace("Jun", "Iun")
        date = date.replace("Jul", "Iul")
        date = date.replace("Nov", "Noi")

        # Center the rows on the LCD (16 chars)
        date = date.center(16)
        time = time.center(16)

        payload = date + "|" + time

        _client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)

        _clock_timer.reset()

def handle_cpu_load_and_memory_usage():
    if _cpu_and_mem_timer.elapsed():
        # https://www.delftstack.com/howto/python/get-cpu-usage-in-python/
        cpu_percent = psutil.cpu_percent()
        whole = int(cpu_percent)
        decimal = int((cpu_percent - whole) * 100)
        cpu_load = f"{whole:d}.{decimal:02d}%"

        used_mb = psutil.virtual_memory().used // 1024**2
        total_mb = psutil.virtual_memory().total // 1024**2
        memory_usage = f"{used_mb}MB/{total_mb}MB"

        first_row = "CPU: " + cpu_load
        second_row = "RAM: " + memory_usage

        payload = first_row + "|" + second_row
        _client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)

        _cpu_and_mem_timer.reset()

def handle_external_ip_address():
    if _ip_address_timer.elapsed():
        # https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
        ip_address = requests.get('https://api64.ipify.org').text

        first_row = "IP Address"
        second_row = ip_address

        # Center the rows on the LCD (16 chars)
        first_row = first_row.center(16)
        second_row = second_row.center(16)

        payload = first_row + "|" + second_row
        _client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)

        _ip_address_timer.reset()

def handle_step_increment():
    global _step, _stepChanged

    if _stepChanged:
        _step = (_step + 1) % 3

        clear_the_lcd()
        _stepChanged = False

def clear_the_lcd():
    _client.publish(MQTT_LCD_TOPIC, payload="|", qos=0, retain=False)
    sleep(0.3) # Wait for the message to be sent and processed

def mqtt_on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT server with result code: {reason_code}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global _shuttingDown, _stepChanged

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "top_key_pressed":
        _shuttingDown = True
    elif message == "bottom_key_pressed":
        _stepChanged = True

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
        # Cleanup MQTT client
        if _client:
            _client.loop_stop()
            _client.disconnect()
        print("App stopped")
