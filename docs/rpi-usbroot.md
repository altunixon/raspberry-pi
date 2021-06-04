### Download latest Raspbian/Ubuntu (Prefer 64bit OS for Rpi4)
Raspbian (32bit): https://downloads.raspberrypi.org/raspios_lite_armhf_latest </br>
Ubuntu 18.04 (32bit): https://ubuntu.com/download/raspberry-pi/thank-you?version=18.04&versionPatch=.4&architecture=armhf+raspi3 </br>
Ubuntu 20.04 (32bit): https://ubuntu.com/download/raspberry-pi/thank-you?version=20.04&architecture=armhf+raspi </br>
Ubuntu 18.04 (64bit): https://ubuntu.com/download/raspberry-pi/thank-you?version=18.04&versionPatch=.4&architecture=arm64+raspi3 </br>
Ubuntu 20.04 (64bit): https://ubuntu.com/download/raspberry-pi/thank-you?version=20.04&architecture=arm64+raspi </br>
Ubuntu MATE 18.04 (64bit): https://ubuntu-mate.org/download/arm64/bionic/ </br>
Ubuntu MATE 20.04 (64bit): https://ubuntu-mate.org/download/arm64/focal/ </br>
Flash image to sdcard with yout preferred program
### Migrate SD Card content to external HDD
- Using another *nix computer:
  - Connect both the SD card and external hdd to said computer
    ```bash
    sudo lsblk
    # create mount folders
    sudo mkdir -p /media/$USER/rpi-sdcard/{boot,root,hdd}
    # mount sdcard boot partition (for editing cmdline.txt, touch ssh, etc...)
    sudo mount /dev/sdm1 /media/$USER/rpi-sdcard/boot
    # mount sdcard root partition to migrate its content to external hdd
    sudo mount /dev/sdm2 /media/$USER/rpi-sdcard/root
    ```
  - Prepare external hdd for migration
    ```bash
    # edit external hdd partition table, follow other guide and pray lord, be careful
    sudo fdisk /dev/sdq
    # format external hdd as root partion (ext4)
    sudo mkfs.ext4 /dev/sdq1
    # optional, format another partition to use as /home
    sudo mkfs.ext3 /dev/sdq2
    # mount external hdd root partition
    sudo mount /dev/sdq1 /media/$USER/rpi-sdcard/hdd
    ```
  - Migrate sdcard /root to external hdd
    ```bash
    # migrate sdcard root partition to external hdd
    sudo cp --archive /media/$USER/rpi-sdcard/root/* /media/$USER/rpi-sdcard/hdd/
    ```
  - Edit **external hdd's** /etc/fstab
    ```bash
    sudo vim /media/$USER/rpi-sdcard/hdd/etc/fstab
    ```
    Modify Line:
    ```
    PARTUUID=ed8acfca-02  /               ext4    defaults,noatime  0       1
    ```
    Set **PARTUUID=ed8acfca-02** to **external hdd's** partition id.
  - Backup then modify **sdcard's** boot config cmdline.txt </br>
    Note: on Ubuntu might be located under **/boot/firmware/cmdline.txt**
    ```bash
    sudo cp /media/$USER/rpi-sdcard/boot/cmdline.{txt,sd}
    sudo vim /media/$USER/rpi-sdcard/boot/cmdline.txt
    ```
    Change boot line's option **root=PARTUUID=ed8acfca-02**:
    ```
    dwc_otg.lpm_enable=0 console=tty1 root=PARTUUID=ed8acfca-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
    ```
    to **external hdd's** partition id.
  - Finish, you can now unmount sdcard and external hdd, insert both to your rpi and powerup.
- Using the Rpi itself:
  - Connect external hdd to the pi
  - Prepare external hdd for migration
    ```bash
    sudo lsblk
    sudo mkdir -p /media/$USER/rpi-hdd
    # edit external hdd partition table, follow other guide and pray lord, be careful
    sudo fdisk /dev/sdq
    # format external hdd as root partion (ext4)
    sudo mkfs.ext4 /dev/sdq1
    # optional, format another partition to use as /home
    sudo mkfs.ext3 /dev/sdq2
    # mount external hdd root partition
    sudo mount /dev/sdq1 /media/$USER/rpi-hdd
    ```
  - Migrate sdcard /root to external hdd
    ```bash
    # migrate sdcard root partition to external hdd
    rsync -ax / /media/$USER/rpi-hdd/
    ```
  - Edit **external hdd's** /etc/fstab (same as above)
  - Backup then modify **sdcard's** boot config cmdline.txt (same as above)
  - Finish, you can now reboot.

- The pi will boot using **sdcard's** boot config, which will then mount **external hdd** as root partition (if god wills it). </br>
  Preferred method is mounting both sdcard and external hdd since migrating from a non active os is much more stable

### Other Sources:
[Adafruit Guide](https://cdn-learn.adafruit.com/downloads/pdf/external-drive-as-raspberry-pi-root.pdf) </br>
[Rpi forum Sticky](https://www.raspberrypi.org/forums/viewtopic.php?t=44177) </br>

### Potential issue: Slow external drive speed due to [UASP Hdd adapter quirk](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=245931)
#### The most common symptoms of a misbehaving UAS device are
- Extremely slow performance - in the kilobytes per second range
- Frequent disconnects-reconnects of the device with the desktop repeatedly displaying the "removable medium inserted" dialogue box
- The kernel message log (dmesg) reports errors relating to a UAS device that look like this: 
  ```
  [ 501.594683] usbcore: registered new interface driver usb-storage
  [ 501.599729] scsi host6: uas
  [ 501.599800] usbcore: registered new interface driver uas
  ...
  [ 573.203294] sd 6:0:0:0: [sda] tag#29 uas_eh_abort_handler 0 uas-tag 9 inflight: CMD OUT
  [ 573.203302] sd 6:0:0:0: [sda] tag#29 CDB: Write(10) 2a 00 00 4f a0 00 00 04 00 00
  [ 573.205063] sd 6:0:0:0: [sda] tag#28 uas_eh_abort_handler 0 uas-tag 10 inflight: CMD OUT
  [ 573.205070] sd 6:0:0:0: [sda] tag#28 CDB: Write(10) 2a 00 00 4f a4 00 00 04 00 00
  [ 573.208537] sd 6:0:0:0: [sda] tag#27 uas_eh_abort_handler 0 uas-tag 6 inflight: CMD OUT
  ...
  [ 573.269992] scsi host6: uas_eh_device_reset_handler start
  [ 573.393710] usb 2-4: reset SuperSpeed Gen 1 USB device number 2 using xhci_hcd
  [ 573.414256] scsi host6: uas_eh_device_reset_handler success
  ```
  These errors may also appear due to poor power quality or overloading the Pi's maximum 1.2A downstream USB port current, </br>
  but if they persist when using a powered hub then they are genuine UAS issues. 
- All UAS drives by design must support mass-storage as a fallback option. </br>
  Thus the kernel can be told to ignore the UAS interface of a device and just use mass-storage, </br>
  the usb-storage driver has a "quirks" option for this purpose. </br>
  As UAS is built-in to the kernel to allow the root filesystem to be installed on an SSD, </br>
  the quirk needs to go into cmdline.txt as a module parameter. </br>
  This parameter matches the USB Vendor ID (vid), Product ID (pid) and overlays the specified quirks that disable specific features for this device.
#### Finding the VID and PID of your USB SSD
- Disconnect the USB SSD. In a terminal window, run the command sudo dmesg -C. 
- Now, plug in the SSD and run dmesg with no parameters.
- You should get output that looks like this: 
  ```
  [ 4096.609817] usb 2-1: new SuperSpeed Gen 1 USB device number 4 using xhci_hcd
  [ 4096.646369] usb 2-1: New USB device found, idVendor=2109, idProduct=0715, bcdDevice=a0.00
  [ 4096.646385] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
  [ 4096.646397] usb 2-1: Product: SABRENT
  [ 4096.646409] usb 2-1: Manufacturer: SABRENT
  [ 4096.646421] usb 2-1: SerialNumber: 000000123AD2
  [ 4096.655154] scsi host0: uas
  [ 4096.669178] scsi 0:0:0:0: Direct-Access              SABRENT          2210 PQ: 0 ANSI: 6
  [ 4096.670993] sd 0:0:0:0: Attached scsi generic sg0 type 0
  [ 4096.673710] sd 0:0:0:0: [sda] 234441648 512-byte logical blocks: (120 GB/112 GiB)
  ```
- The idVendor and idProduct are the two hexadecimal numbers you need to take a note of.
- If you have multiple USB SSD devices plugged into a single Pi 4, </br>
  then for each device experiencing issues repeat Step 1 above and make a note of each idVendor and idProduct pair.
#### Add the quirks to /boot/cmdline.txt
- Run a text editor as root:
  ```
  # from the console
  sudo nano /boot/cmdline.txt
  # or from the desktop
  sudo leafpad /boot/cmdline.txt
  ```
- At the start of the line of parameters, add the text:
  ```
  usb-storage.quirks=aaaa:bbbb:u
  ```
  where aaaa is the idVendor for your device and bbbb is the idProduct. </br>
  So, with the example device above the string will be:
  ```
  usb-storage.quirks=2109:0715:u dwc_otg.lpm_enable=0 console=tty1 root=PARTUUID=ed8acfca-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
  ```
- For multiple devices with different VID:PID pairs, expand the parameter with a comma "," between each vid:pid:u triplet like this: 
  ```
  usb-storage.quirks=0123:4567:u,2109:0715:u dwc_otg.lpm_enable=0 console=tty1 root=PARTUUID=ed8acfca-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
  ```
- Save file and reboot
- ~Unverified approach:~ Retracted, since you boot from sdcard with the pi and the refer to the root partition, </br>
  adding below option to the destination root partition is ineffective in this particular use case. </br>
  This fix should still be applicable to other not referred from boot config external uas device.</br>
  Add device to blacklist [Ubuntu forum](https://ubuntuforums.org/showthread.php?t=2307662)
  ```bash
  echo 'options usb-storage quirks=357d:7788:u' | sudo tee -a /etc/modprobe.d/blacklist_uas_357d.conf
  sudo update-initramfs -u
  ```
  Config file in modprobe.d should start with **blacklist_uas** and end with **.conf** extension, vendor name is optional.
#### Check that it worked
To check that the quirk has been applied successfully, run dmesg and check that the VID and PID is listed as having a quirk applied: 
```bash
dmesg | grep usb-storage
[    2.495725] usb 2-1: UAS is blacklisted for this device, using usb-storage instead
[    2.512739] usb 2-1: UAS is blacklisted for this device, using usb-storage instead
[    2.531823] usb-storage 2-1:1.0: USB Mass Storage device detected
[    2.549642] usb-storage 2-1:1.0: Quirks match for vid 2109 pid 0715: 800000
[    2.566177] scsi host0: usb-storage 2-1:1.0
```
Typically, most drives are still performant with usb-storage. </br>
They may not be able to saturate a USB3.0 connection but should still get 150-200MB/s under most workloads.
