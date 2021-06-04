### Hostname / timezone / locale
```bash
sudo apt-get update
sudo apt-get install -y vim screen
cat << EOT >> ~/.vimrc

set mouse-=a
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab

EOT
newhost="XXX"
sudo sed -i 's/raspberrypi/'"$newhost"'/g' /etc/hostname
sudo sed -i 's/raspberrypi/'"$newhost"'/g' /etc/hosts
ls -l /etc/localtime
sudo unlink /etc/localtime
sudo ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
sudo raspi-config nonint do_change_locale 'en_US.UTF-8'
```
### tmpfs
```bash
cat << EOT >> /etc/fstab
tmpfs   /tmp        tmpfs    defaults,noatime,nosuid,size=128m    0 0
tmpfs   /var/tmp    tmpfs    defaults,noatime,nosuid,size=32m     0 0
tmpfs   /var/log    tmpfs    defaults,noatime,nosuid,mode=0755,size=128m  0 0
tmpfs   /var/run    tmpfs    defaults,noatime,nosuid,mode=0755,size=8m    0 0
tmpfs   /var/spool/mqueue    tmpfs    defaults,noatime,nosuid,mode=0700,gid=12,size=32m    0 0
EOT
```
### User add
```bash
passwd root
# PLACEHOLDER
```
### Setup NICs
- Disable IPv6
  ```bash
  dip6="net.ipv6.conf.all.disable_ipv6=1\nnet.ipv6.conf.default.disable_ipv6=1\nnet.ipv6.conf.lo.disable_ipv6=1\nnet.ipv6.conf.eth0.disable_ipv6=1\n"
  [ ! -f /etc/sysctl.d/96-disable-ipv6.conf ] && echo -e "$dip6" >> /etc/sysctl.d/96-disable-ipv6.conf || echo "IPv6 Already disabled?"
  ```
- Disable onboard wireless devices
  Hard disable (device tree)
  ```bash
  vim /boot/config.txt
  [All]
  dtoverlay=disable-wifi
  dtoverlay=disable-bt
  ```
  Soft disable (driver blacklist)
  ```bash
  cat << EOT >> /etc/modprobe.d/brcm-blacklist.conf
  blacklist brcmfmac
  blacklist brcmutil
  EOT
  ```
  disable /etc/profile wificheck.sh
  ```bash
  sudo mv /etc/profile.d/wifi-check.sh{,-disabled}
  ```
- Static addresses (optional, static ip setup via dhcp is preferred)
  ```bash
  vim /etc/dhcpcd.conf
  interface eth0
    static ip_address=192.168.11.61/24    
    static routers=192.168.11.1
    static domain_name_servers=192.168.11.53 1.1.1.1
  ```
### Setup environment
list installed packages on previous env
```bash
apt list --installed | tee raspbian-installed.txt
```
install on new env
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y firmware-misc-nonfree firmware-realtek
sudo apt-get install -y nfs-common \
  file findutils ranger \
  fdisk e2fsprogs dosfstools \
  ffmpeg libopenjp2-7 libpng16-16 libpng-dev libpng-tools
sudo apt-get install -y python3 python3-pip python3-venv
python3 -m venv --copies --upgrade-deps ~/py3-venv
```
### Extra
Useful aliases (pi specific)
```bash
cat << EOT >> ~/.bash_aliases

alias pi-temp="vcgencmd measure_temp"
alias pi-lowv="vcgencmd get_throttled"
alias cpu-temp="echo $(($(</sys/class/thermal/thermal_zone0/temp)/1000)) c"

EOT
```
Generating Ed25519 Key
```bash
ssh-keygen -o -a 128 -t ed25519 -f ~/.ssh/id_ed25519 -C "$USER@$HOSTNAME"
```
- -o: Save the private-key using the new OpenSSH format rather than the PEM format.</br>
  Actually, this option is implied when you specify the key type as ed25519.</br>
- -a: It’s the numbers of KDF (Key Derivation Function) rounds.</br>
  Higher numbers result in slower passphrase verification, </br>
  increasing the resistance to brute-force password cracking should the private-key be stolen.</br>
- -t: Specifies the type of key to create, in our case the Ed25519.</br>
- -f: Specify the output key file.</br>
- -C: An option to specify a comment.

### ~~Check TRIM for SSD [jeffgeerling]~~ might brick usb flash drive!! → ABANDONNED
```bash
sudo fstrim -v /
```
~~If this reports back fstrim: /: the discard operation is not supported, then TRIM is not enabled.</br>
You can also check with:~~
```bash
lsblk -D
```
~~If the DISC-MAX value is 0B, then TRIM is not enabled.</br>
Checking if the SSD Firmware supports TRIM~~
```bash
sudo apt-get install -y sg3-utils lsscsi
```


[jeffgeerling]: https://www.jeffgeerling.com/blog/2020/enabling-trim-on-external-ssd-on-raspberry-pi
