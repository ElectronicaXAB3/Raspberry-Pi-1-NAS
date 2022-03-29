import paho.mqtt.client as mqtt
from time import sleep,time

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_KEYBOARD_TOPIC = "nas/keyboard"
MQTT_LCD_TOPIC = "nas/lcd"

lastTime = 0
trigger = False

def main():
    global lastTime, trigger

    mqtt_init()

    while True:
        if trigger:
            now = time()

            if int(now - lastTime) > 2:
                client.publish(MQTT_LCD_TOPIC, payload="|", qos=0, retain=False)

                trigger = False
                lastTime = now

        sleep(0.3)

def mqtt_on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")
    client.subscribe(MQTT_KEYBOARD_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global lastTime, trigger

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    if message == "bottom_key_pressed":
        payload = "Bottom button|was pressed"
        client.publish(MQTT_LCD_TOPIC, payload=payload, qos=0, retain=False)

        lastTime = time()
        trigger = True

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

