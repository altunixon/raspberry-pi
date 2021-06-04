**First:**
```bash
vim /etc/apt/sources.list.d/docker.list
```
**Change:**
```
deb [arch=armhf] https://download.docker.com/linux/raspbian 10 stable
```
**To:**
```
deb [arch=armhf] https://download.docker.com/linux/raspbian stretch edge
```
**Then:**
```bash
sudo apt update
sudo apt install docker-ce
sudo usermod -a -G docker $USER
docker pull hypriot/rpi-mysql
```

