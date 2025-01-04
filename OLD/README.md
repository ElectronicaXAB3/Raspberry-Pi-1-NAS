### Introduction

This project aims to create a simple, custom and cheap [NAS](https://en.wikipedia.org/wiki/Network-attached_storage) (network attached storage) out of a Raspberry Pi board and a few parts that were lying around for years.

### Features

- LCD screen that displays useful information
- button with shutdown function
- button with extra information to display on the LCD
- Linux serial console via micro USB
- network file sharing (compatible with Windows/Linux file sharing)
- wired and wireless network access
- front panel activity LED
- automatic network restart in case of disconnect

### Software used

- Samba (network file sharing)
- Python (for LCD driver, buttons application and MQTT publisher/subscriber application)
- Mosquitto (MQTT server - to bind every module together)
- ifplugd (automatic network restart after any type of disconnection)

### Installation

Check [Installation.md](Installation.md).
