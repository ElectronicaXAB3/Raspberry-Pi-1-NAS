### Introduction

This project aims to create a simple NAS (network attached storage) out of a Raspberry Pi board and a few parts that were lying around for years.

### Features

- LCD screen that displays useful information
- button with shutdown function
- button with extra information to display on the LCD
- Linux serial console via micro USB
- network file sharing (compatible with Windows file sharing)
- wired and wireless network access
- front activity LED
- automatic network restart in case of disconnect

### Software used

- Samba (network file sharing)
- LCD server (written in Python)
- buttons server (written in Python)
- Mosquitto (MQTT server - to bind every module together)
- ifplugd (automatic network restart after any type of disconnection)

### Installation

Check [Installation.md](Installation.md).
