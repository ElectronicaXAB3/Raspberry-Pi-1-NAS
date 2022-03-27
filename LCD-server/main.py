# https://www.electronicshub.org/interfacing-16x2-lcd-with-raspberry-pi/
# https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/python-code
import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR   = True
LCD_CMD   = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

LCD_LINE_1_BUFFER = ""
LCD_LINE_2_BUFFER = ""
LCD_LINE_1_LAST_BUFFER = ""
LCD_LINE_2_LAST_BUFFER = ""

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/lcd"

def main():
    global LCD_LINE_1_BUFFER, LCD_LINE_1_LAST_BUFFER
    global LCD_LINE_2_BUFFER, LCD_LINE_2_LAST_BUFFER

    lcd_init()
    mqtt_init()

    while True:
        if LCD_LINE_1_BUFFER != LCD_LINE_1_LAST_BUFFER:
            lcd_string(LCD_LINE_1_BUFFER, LCD_LINE_1)
            LCD_LINE_1_LAST_BUFFER = LCD_LINE_1_BUFFER

        if LCD_LINE_2_BUFFER != LCD_LINE_2_LAST_BUFFER:
            lcd_string(LCD_LINE_2_BUFFER, LCD_LINE_2)
            LCD_LINE_2_LAST_BUFFER = LCD_LINE_2_BUFFER

        sleep(0.3)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7

def mqtt_on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT server with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global LCD_LINE_1_BUFFER, LCD_LINE_2_BUFFER

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    lines = message.split('|')

    LCD_LINE_1_BUFFER = lines[0]
    LCD_LINE_2_BUFFER = lines[1]

def mqtt_init():
    global client

    client = mqtt.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
    client.loop_start()

def lcd_init():
    setup_gpio()

    # Initialise display
    lcd_display(0x33, LCD_CMD) # 110011 Initialise
    lcd_display(0x32, LCD_CMD) # 110010 Initialise
    lcd_display(0x06, LCD_CMD) # 000110 Cursor move direction
    lcd_display(0x0C, LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_display(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_clear()                # 000001 Clear display

    sleep(E_DELAY)

def lcd_clear():
    lcd_display(0x01, LCD_CMD)

def lcd_display(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode) # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_display(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_display(ord(message[i]), LCD_CHR)


# Start the main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_clear()
        GPIO.cleanup()
