#### Original post by [Medium](https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353)
TLDR; If you’re using Raspbian Stretch (or any other Linux flavored OS) you can force your file system into “read-only mode” rather easily. </br>
While in read-only mode the system cannot write any data to your SD card thus significantly prolonging the lifespan of your card. </br>
To achieve this, we need to take the following steps:
1. **Prepare system**
  - Update and remove packages 
      ```bash
      sudo apt-get update && apt-get upgrade
      sudo apt-get remove --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm
      sudo systemctl disable x11-common
      sudo systemctl disable bootlogs
      sudo systemctl disable console-setup
      sudo apt-get install busybox-syslogd
      sudo dpkg --purge rsyslog
      ```
  - If you intend to install pihole on this host, you should do it here. Refer to [rpi-pihole-install.md](./rpi-pihole-install.md)
  - Remove dangling install files
      ```bash
      sudo apt-get autoremove --purge
      ```
  - Disable swap and filesystem check and set it to read-only </br>
    Edit **"/boot/cmdline.txt"** and add the following three words at the end of the line: 
    ```
    fastboot noswap ro
    ```
    ie:
    ```
    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 \
        rootfstype=ext4 elevator=deadline rootwait fastboot noswap ro
    ```
2. **Configure the operating system to write all temporary files to the “tmpfs” file system which resides in memory.**
  - Move and link some system files and/or folder to **"/tmp"**
    ```bash
    sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/run /var/spool /var/lock /etc/resolv.conf
    sudo ln -s /tmp /var/lib/dhcp
    sudo ln -s /tmp /var/lib/dhcpcd5
    sudo ln -s /tmp /var/run
    sudo ln -s /tmp /var/spool
    sudo ln -s /tmp /var/lock
    sudo touch /tmp/dhcpcd.resolv.conf
    sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
    ```
3. **Configure additional services to also use the tempfs file system.**
  - Edit the file "/etc/systemd/system/dhcpcd5" and change the line: </br>
    "PIDFile=/run/dhcpcd.pid" to "PIDFile=/var/run/dhcpcd.pid"
    ```bash
    sed "s/PIDFile=\/run\/dhcpcd.pid/PIDFile=\/var\/run\/dhcpcd.pid/" /etc/systemd/system/dhcpcd5
    ```
  - Update systemd random seed location
    ```bash
    sudo rm /var/lib/systemd/random-seed
    sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed
    ```
    Edit the service configuration file **"/lib/systemd/system/systemd-random-seed.service"** to have it created on boot. 
    Add the line "ExecStartPre=/bin/echo '' > /tmp/random-seed" under the **[Service]** section, inb4 **ExecStart**.
    ```bash
    sudo systemctl daemon-reload
    ```
4. **Make the file-systems read-only**
  - Update the file **"/etc/fstab"** and add the **[,ro]** flag to all block devices
    ie:
    ```vim
    proc            /proc           proc    defaults             0       0
    /dev/mmcblk0p1  /boot           vfat    defaults,ro          0       2
    /dev/mmcblk0p2  /               ext4    defaults,noatime,ro  0       1
    # Add temp mounts to ramfs
    tmpfs           /tmp            tmpfs   nosuid,nodev         0       0
    tmpfs           /var/log        tmpfs   nosuid,nodev         0       0
    tmpfs           /var/tmp        tmpfs   nosuid,nodev         0       0
    ```
5. **Add some scripts to conveniently toggle read-only mode on / off (_Optional_)**
  - Edit the file /etc/bash.bashrc and add the following lines at the end:
    ```bash
    set_bash_prompt() {
      fs_mode=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")
      PS1='\[\033[01;32m\]\u@\h${fs_mode:+($fs_mode)}\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
    }
    alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
    alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
    PROMPT_COMMAND=set_bash_prompt
    ```
6. **Reboot**
    ```bash
    sudo reboot
    ```
    Your system should now be read-only
