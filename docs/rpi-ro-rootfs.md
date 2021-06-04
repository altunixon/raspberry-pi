### Preface
Although the process is the same, there are some slight differences between Buster and Stretch. </br>
These differences will be noted as such in the tutorial. </br>
Sources: </br>
[Stretch] </br>
[Buster]

### Preparations
- Update packages
  ```bash
  sudo apt-get update && sudo apt-get upgrade
  ```
- Cleanup unneeded packages and/or packages that will need writing access to the root filesystem, </br>
  If these were not installed in the first place then just skip this step:
  ```bash
  sudo apt-get remove --purge triggerhappy logrotate
  sudo apt-get remove --purge wolfram-engine anacron xserver-common lightdm
  sudo apt-get autoremove --purge
  # Disable display service (run in init 3, multiuser commandline mode)
  sudo systemctl get-default
  sudo systemctl list-units --type=target
  sudo systemctl set-default multi-user.target
  # Stretch: Remove some startup scripts
  sudo systemctl disable bootlogs
  sudo systemctl disable console-setup
  ```
- Replace your log manager
  ```bash
  sudo apt-get install busybox-syslogd
  sudo apt-get remove --purge rsyslog
  ```
  Hint: From now on use sudo logread to check your system logs.

### Prepare the filesystems
- Disable swap, filesystem check and set mount option to read-only </br>
  Disable swap:
  ```bash
  sudo swapoff -a
  sudo dphys-swapfile swapoff
  sudo systemctl disable dphys-swapfile.service
  sudo apt-get remove --purge dphys-swapfile
  ```
  Edit **"/boot/cmdline.txt"** and add the following three words at the end of the line: **fastboot noswap ro**
  ```bash
  cat /boot/cmdline.txt
  dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait fastboot noswap ro
  ```
- Make the file-systems read-only (fstab directive) and add tmpfs mounts
  Update file **"/etc/fstab"** and add the ,ro flag to all block devices. </br>
  The updated file should look like this:
  ```bash
  cat /etc/fstab
  proc                  /proc     proc    defaults                  0     0
  PARTUUID=fb0d460e-01  /boot     vfat    defaults,ro               0     2
  PARTUUID=fb0d460e-02  /         ext4    defaults,noatime,ro       0     1
  # Added temporary storage mounts
  tmpfs                 /tmp      tmpfs   rw,nosuid,nodev,size=16M  0     0
  tmpfs                 /var/log  tmpfs   rw,nosuid,nodev,size=32M  0     0
  tmpfs                 /var/tmp  tmpfs   rw,nosuid,nodev,size=16M  0     0
  ```

### Relocate write required system files and change configurations pointing to said files
- Relocate some system files to temp filesystem </br>
  **Note:** This part is different from previous Raspbian versions (Stretch etc.). </br>
  On Raspbian Buster do **NOT** move the **"/var/lock"** and **"/var/run"** directories as they are already symlinked to tmpfs directories. </br>
  You can read more about these changes in the [Debian Buster tmpfs documentation]. </br>
  **Buster:**
  ```bash
  sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/spool /etc/resolv.conf
  sudo ln -s /tmp /var/lib/dhcp
  sudo ln -s /tmp /var/lib/dhcpcd5
  sudo ln -s /tmp /var/spool
  sudo touch /tmp/dhcpcd.resolv.conf
  sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
  ```
  **Stretch:**
  ```bash
  sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/run /var/spool /var/lock /etc/resolv.conf
  sudo ln -s /tmp /var/lib/dhcp
  sudo ln -s /tmp /var/lib/dhcpcd5
  sudo ln -s /tmp /var/run
  sudo ln -s /tmp /var/spool
  sudo ln -s /tmp /var/lock
  sudo touch /tmp/dhcpcd.resolv.conf
  sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
  # Edit the file /etc/systemd/system/dhcpcd5 and change the line:
  # PIDFile=/run/dhcpcd.pid
  cat /etc/systemd/system/dhcpcd5
  PIDFile=/var/run/dhcpcd.pid
  ```
- Update the systemd random seed:
  ```bash
  sudo rm /var/lib/systemd/random-seed
  sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed
  ```
  Edit the service configuration file **"/lib/systemd/system/systemd-random-seed.service"** to have the file created on boot. </br>
  Add the line **ExecStartPre=/bin/echo "" > /tmp/random-seed** under the [Service] section. </br>
  The modified [Service] section should look simillar to this:
  ```bash
  cat /lib/systemd/system/systemd-random-seed.service
  [Service]
  Type=oneshot
  RemainAfterExit=yes
  ExecStartPre=/bin/echo "" > /tmp/random-seed
  ExecStart=/lib/systemd/systemd-random-seed load
  ExecStop=/lib/systemd/systemd-random-seed save
  TimeoutSec=30s
  # Reload service
  sudo systemctl daemon-reload
  ```

### FIN
If everything is in order, after reboot your root filesystem should now be read only.

### Optional: Adding some fancy commands to switch between RO and RW modes </br>
- Here we create two shell commands ro (read-only) and rw (read-write) which can be used at any time to switch between the modes. </br>
  In addition it will add an indicator to your command prompt to show the current mode.
- Edit **"/etc/bash.bashrc"** and add the following lines at the end:
  ```bash
  set_bash_prompt() {
    fs_mode=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")
    PS1='\[\033[01;32m\]\u@\h${fs_mode:+($fs_mode)}\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
  }
  alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
  alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
  PROMPT_COMMAND=set_bash_prompt
  ```
- Finally ensure the file system goes back to read-only once you log out. </br>
  Edit (or create) the file /etc/bash.bash_logout and add the following lines at the end:
  ```bash
  sudo mount -o remount,ro /
  sudo mount -o remount,ro /boot
  ```



[Stretch]: https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353
[Buster]: https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-c558694de79
[Debian Buster tmpfs documentation]: https://manpages.debian.org/buster/initscripts/tmpfs.5.en.html
