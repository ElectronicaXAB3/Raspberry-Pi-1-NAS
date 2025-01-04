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

**3. Disabling the swap**

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

**3. Install disk management tools**

Install the disks daemon

```bash
sudo apt install udisks2 -y
```

Install the frontend

```bash
sudo pip3 install udiskie
```

The `udiskie` command will install `udiskie`, `udiskie-info`, `udiskie-mount` and `udiskie-umount` executables located in `/usr/local/bin/` folder.

**4. Installing the HDD**

Find the HDD partition we are about to mount

```bash
lsblk
```

example output

```text
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 931.5G  0 disk
├─sda1        8:1    0 499.7M  0 part
├─sda2        8:2    0  34.6G  0 part
├─sda3        8:3    0     1K  0 part
└─sda5        8:5    0 896.5G  0 part 
```

**Note:** mine is /dev/sda5 on a 1TB HDD.

Find the partition UUID

```bash
sudo blkid
```

example output

```text
...
/dev/sda5: UUID="20e5d1c9-10aa-4804-8501-c618d78d8004" TYPE="ext4" PARTUUID="7e025efc-05"
```

**Note:** mine is `20e5d1c9-10aa-4804-8501-c618d78d8004`.

Create the mounting point

```bash
sudo mkdir /mnt/1tb-hdd
```

Add the partition to mount automatically on every boot

```bash
sudo nano /etc/fstab
```

and add

```text
# USB HDD
UUID=20e5d1c9-10aa-4804-8501-c618d78d8004 /mnt/1tb-hdd  ext4   noatime,nodiratime,errors=remount-ro 0       2
```

mount it now

```
sudo mount -a
```

change whole HDD files permissions

```bash
sudo chown pi:pi /mnt/1tb-hdd -R
```

**5. Installing & configuring samba**

```bash
sudo apt install samba -y
```

```bash
sudo nano /etc/samba/smb.conf
```

and add

```text
[1TB_USB_HDD]
    comment = An almost 1TB USB HDD
    path = /mnt/1tb-hdd
    browseable = yes
    guest ok = no
    writable = yes
    force user = pi
    force group = pi
    valid users = pi
```

create a samba user and set a password

```bash
sudo smbpasswd -a pis
```

**Note:** this password should be something else than the Linux account's password

restart the Samba service

```bash
sudo systemctl restart smbd.service
```

**6. Cloning the GitHub repository**

```bash
cd /home/nas
git clone https://github.com/ElectronicaXAB3/Raspberry-Pi-1-NAS
```

**7. Installing the Python requirements**

```bash
sudo apt install python3-pip python3-rpi.gpio -y
sudo -u nas pip3 install paho-mqtt
```

**8. Installing the LCD application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/LCD-app/LCD-app.service /etc/systemd/system/LCD-app.service
sudo systemctl daemon-reload
sudo systemctl start LCD-app.service
sudo systemctl enable LCD-app.service
```

**9. Installing the Keyboard application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Keyboard-app/Keyboard-app.service /etc/systemd/system/Keyboard-app.service
sudo systemctl daemon-reload
sudo systemctl start Keyboard-app.service
sudo systemctl enable Keyboard-app.service
```

**10. Installing the Shutdown application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Shutdown-app/Shutdown-app.service /etc/systemd/system/Shutdown-app.service
sudo systemctl daemon-reload
sudo systemctl start Shutdown-app.service
sudo systemctl enable Shutdown-app.service
```

**11. Installing the Main application**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Main-app/Main-app.service /etc/systemd/system/Main-app.service
sudo systemctl daemon-reload
sudo systemctl start Main-app.service
sudo systemctl enable Main-app.service
```

**12. Installing the `unmount HDD at shutdown` service**

copy & enable the service

```bash
sudo cp /home/nas/Raspberry-Pi-1-NAS/Unmount-HDD-at-shutdown.service /etc/systemd/system/Unmount-HDD-at-shutdown.service
sudo systemctl daemon-reload
sudo systemctl enable Unmount-HDD-at-shutdown.service
```

This will make sure the HDD will get unmounted and powered-down (parking heads) before the Raspberry Pi completes the shutdown process.

### Raspberry Pi cleanup

This step is optional. But if you proceed with it, you will have fewer running processes, making the installation lighter. It will also boot a bit faster.

**1. Disable the cron service**

```bash
sudo systemctl stop cron
sudo systemctl mask cron
```

**2. Disable the rainbow splash**

```bash
sudo nano /boot/config.txt
```

and add

```text
# Disable rainbow splash
disable_splash=1
```

**3. Disable the SPI and the I2C**

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
- [How to run script with systemd at shutdown only](https://www.golinuxcloud.com/run-script-with-systemd-at-shutdown-only-rhel/)
- [RPi.GPIO examples](https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/)
- [eclipse/paho.mqtt.python examples](https://github.com/eclipse/paho.mqtt.python/tree/af64c3845663caaebaba0720549eb363067ca07a/examples)
- [udiskie manual](https://raw.githubusercontent.com/coldfix/udiskie/master/doc/udiskie.8.txt)
- [samba users config](https://www.samba.org/samba/docs/using_samba/ch09.html)
