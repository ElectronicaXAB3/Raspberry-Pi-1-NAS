### Very important

All git commands **MUST** be run with any user but `root` or `nas`.  
Otherwise, it will not work and give false/fake errors.  

Before any change can be made under development, change permissions to allow all:

```bash
sudo find /home/nas/Raspberry-Pi-1-NAS/ -type d -exec chmod 777 {} \;
sudo find /home/nas/Raspberry-Pi-1-NAS/ -type f -exec chmod 666 {} \;
```

Before the end of the day, change permissions back to defaults:

```bash
sudo find /home/nas/Raspberry-Pi-1-NAS/ -type d -exec chmod 755 {} \;
sudo find /home/nas/Raspberry-Pi-1-NAS/ -type f -exec chmod 644 {} \;
sudo chown nas:nas /home/nas/Raspberry-Pi-1-NAS/ -R
```

### Push the local changes to GitHub

```bash
cd /home/nas/Raspberry-Pi-1-NAS/
eval $(ssh-agent -s)
ssh-add key
```

```bash
git add .
git commit -m 'wip'
git push -u origin master
```

### Check the local changes

```bash
git status
```

```bash
git log -3
```

### Pull the latest changes

```bash
cd /home/nas/Raspberry-Pi-1-NAS/
eval $(ssh-agent -s)
ssh-add key
```

```bash
git pull
```

### List local config

```bash
git config --list
```
