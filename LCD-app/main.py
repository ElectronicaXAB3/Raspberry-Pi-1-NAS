# https://www.electronicshub.org/interfacing-16x2-lcd-with-raspberry-pi/
# https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/python-code
import lgpio
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

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "nas/lcd"
MQTT_TIMEOUT = 10

_client = None
_gpioh = None
_lcd_line_1_buffer = ""
_lcd_line_2_buffer = ""
_lcd_line_1_last_buffer = ""
_lcd_line_2_last_buffer = ""

def main():
    global _lcd_line_1_buffer, _lcd_line_1_last_buffer
    global _lcd_line_2_buffer, _lcd_line_2_last_buffer

    lcd_init()
    mqtt_init()

    while True:
        if _lcd_line_1_buffer != _lcd_line_1_last_buffer:
            lcd_string(_lcd_line_1_buffer, LCD_LINE_1)
            _lcd_line_1_last_buffer = _lcd_line_1_buffer

        if _lcd_line_2_buffer != _lcd_line_2_last_buffer:
            lcd_string(_lcd_line_2_buffer, LCD_LINE_2)
            _lcd_line_2_last_buffer = _lcd_line_2_buffer

        sleep(0.3)

def setup_gpio():
    global _gpioh

    # Initialize GPIO
    _gpioh = lgpio.gpiochip_open(0)
    print(f"GPIO chip opened with handle: {_gpioh}")

    # Get GPIO info
    chip_info = lgpio.gpio_get_chip_info(_gpioh)
    print(f"Chip info = status: {chip_info[0]}, lines: {chip_info[1]}, name: {chip_info[2]}, label: {chip_info[3]}")

    # Configure pins as inputs with pull-ups
    lgpio.gpio_claim_output(_gpioh, LCD_E, 0)  # E
    lgpio.gpio_claim_output(_gpioh, LCD_RS, 0) # RS
    lgpio.gpio_claim_output(_gpioh, LCD_D4, 0) # DB4
    lgpio.gpio_claim_output(_gpioh, LCD_D5, 0) # DB5
    lgpio.gpio_claim_output(_gpioh, LCD_D6, 0) # DB6
    lgpio.gpio_claim_output(_gpioh, LCD_D7, 0) # DB7

def mqtt_on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT server with result code: {reason_code}")
    client.subscribe(MQTT_TOPIC)

def mqtt_on_message(client, userdata, msg):
    global _lcd_line_1_buffer, _lcd_line_2_buffer

    message = msg.payload.decode('UTF-8')

    print("Received from MQTT server: " + msg.topic + " " + message)

    lines = message.split('|')

    _lcd_line_1_buffer = lines[0]
    _lcd_line_2_buffer = lines[1]

def mqtt_init():
    global _client

    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    _client.on_connect = mqtt_on_connect
    _client.on_message = mqtt_on_message
    _client.connect(MQTT_HOSTNAME, MQTT_PORT, MQTT_TIMEOUT)
    _client.loop_start()

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

    lgpio.gpio_write(_gpioh, LCD_RS, mode) # RS

    # High bits
    lgpio.gpio_write(_gpioh, LCD_D4, 0)
    lgpio.gpio_write(_gpioh, LCD_D5, 0)
    lgpio.gpio_write(_gpioh, LCD_D6, 0)
    lgpio.gpio_write(_gpioh, LCD_D7, 0)

    if bits & 0x10 == 0x10:
        lgpio.gpio_write(_gpioh, LCD_D4, 1)
    if bits & 0x20 == 0x20:
        lgpio.gpio_write(_gpioh, LCD_D5, 1)
    if bits & 0x40 == 0x40:
        lgpio.gpio_write(_gpioh, LCD_D6, 1)
    if bits & 0x80 == 0x80:
        lgpio.gpio_write(_gpioh, LCD_D7, 1)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    lgpio.gpio_write(_gpioh, LCD_D4, 0)
    lgpio.gpio_write(_gpioh, LCD_D5, 0)
    lgpio.gpio_write(_gpioh, LCD_D6, 0)
    lgpio.gpio_write(_gpioh, LCD_D7, 0)

    if bits & 0x01 == 0x01:
        lgpio.gpio_write(_gpioh, LCD_D4, 1)
    if bits & 0x02 == 0x02:
        lgpio.gpio_write(_gpioh, LCD_D5, 1)
    if bits & 0x04 == 0x04:
        lgpio.gpio_write(_gpioh, LCD_D6, 1)
    if bits & 0x08 == 0x08:
        lgpio.gpio_write(_gpioh, LCD_D7, 1)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    sleep(E_DELAY)
    lgpio.gpio_write(_gpioh, LCD_E, 1)
    sleep(E_PULSE)
    lgpio.gpio_write(_gpioh, LCD_E, 0)
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
        print("App started")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_clear()
        # Cleanup GPIO and MQTT
        if _gpioh:
            lgpio.gpiochip_close(_gpioh)
        if _client:
            _client.loop_stop()
            _client.disconnect()
        print("App stopped")
