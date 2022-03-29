### Raspberry Pi preparation

**1. Changing the keyboard layout to US**

```bash
sudo nano /etc/default/keyboard
```

and change XKBLAYOUT="gb" to XKBLAYOUT="us"

**2. Change the timezone**

```bash
sudo timedatectl set-timezone Europe/Bucharest
sudo timedatectl set-ntp true
```

**3. Disabling swap**

```bash
sudo systemctl stop dphys-swapfile.service
sudo systemctl mask dphys-swapfile.service
```

```bash
sudo dphys-swapfile swapoff
sudo rm /var/swap
```

**4. Creating a new user**

```bash
sudo adduser --home /home/nas --shell /usr/bin/false --disabled-login nas
```

append the `gpio` group to newly created user

```bash
sudo usermod -aG gpio nas
```

give shutdown permissions to newly created user

```bash
sudo visudo
```

and add

```text
nas ALL=NOPASSWD: /sbin/shutdown
```

**5. Installing & configuring ifplugd**

```bash
sudo apt install ifplugd -y
```

edit ifplugd configuration

```bash
sudo nano /etc/default/ifplugd
```

and make sure the `INTERFACES` and `HOTPLUG_INTERFACES` are filled with the Raspberry Pi's network interfaces

```text
INTERFACES="eth0"
HOTPLUG_INTERFACES="eth0"
```

add an extra action file (I'm not sure if it's required, but it doesn't seem to harm in any way)

```bash
sudo cat << EOF > /etc/ifplugd/action.d/restartnetwork
#!/bin/sh

if [ "$1" = "up" ] ; then
    service networking restart
fi
EOF
```

**6. Enabling the serial console**

If you don't want to add a serial console to your NAS, you can skip this step.

```bash
sudo raspi-config
```

select `3 Interfacing Options`  
select `P6 Serial Port`  
select `Yes` when you are asked `Would you like a login shell to be accessible over serial?`

### Software installation and configuration

**1. Installing & configuring Samba**

```bash
sudo apt install samba -y
```

**2. Installing Mosquitto**

```bash
sudo apt install mosquitto -y
```

**3. Cloning the Github repository**

```bash
cd /home/nas
git clone https://github.com/ElectronicaXAB3/Raspberry-Pi-1-NAS
```

**4. Installing the requirements**

```bash
sudo apt install python3-pip python3-rpi.gpio -y
sudo -u nas pip3 install paho-mqtt
```

**5. Installing the LCD application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/LCD-app/LCD-app.service /etc/systemd/system/LCD-app.service
sudo systemctl daemon-reload
sudo systemctl start LCD-app.service
sudo systemctl enable LCD-app.service
```

**6. Installing the Keyboard application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Keyboard-app/Keyboard-app.service /etc/systemd/system/Keyboard-app.service
sudo systemctl daemon-reload
sudo systemctl start Keyboard-app.service
sudo systemctl enable Keyboard-app.service
```

**7. Installing the Shutdown application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Shutdown-app/Shutdown-app.service /etc/systemd/system/Shutdown-app.service
sudo systemctl daemon-reload
sudo systemctl start Shutdown-app.service
sudo systemctl enable Shutdown-app.service
```

### Raspberry Pi cleanup

This step is optional. But if you proceed with it, you will have fewer running processes, making the installation lighter. It will also boot a bit faster.

**1. Disabling cron service**

```bash
sudo systemctl stop cron
sudo systemctl mask cron
```

**2. Disabling rainbow splash**

```bash
sudo nano /boot/config.txt
```

and add

```text
# Disable rainbow splash
disable_splash=1
```

**3. Disabling SPI and I2C**

```bash
sudo nano /boot/config.txt
```

and add

```text
# Disable I2C and SPI
dtparam=i2c_arm=off
dtparam=spi=off
```

### Resources

- [How to Add and Delete Users on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-ubuntu-18-04)
- [RPi.GPIO examples](https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/)
- [eclipse/paho.mqtt.python examples](https://github.com/eclipse/paho.mqtt.python/tree/af64c3845663caaebaba0720549eb363067ca07a/examples)
