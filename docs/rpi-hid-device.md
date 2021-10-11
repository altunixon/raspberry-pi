### Hardware
- Pi Zero
- Pi 4
- Boards that supports otg

### Enabling Modules and Drivers [iSticktoit]
- Enable dwc2 device tree overlay: `echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt`
- Enable dwc2 driver: `echo "dwc2" | sudo tee -a /etc/modules`
- Enable libcomposite driver: `echo "libcomposite" | sudo tee -a /etc/modules`

### Device init \(libcomposite configuration\) script
```bash
#!/bin/bash
_device_name="rpi_hid_emu"
cd /sys/kernel/config/usb_gadget/
mkdir -p ${_device_name}
cd ${_device_name}
echo 0x1d6b > idVendor  # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB    # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Alt" > strings/0x409/manufacturer
echo "Rpi Emulated USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower
# Add functions here
# see gadget configurations below
# End functions
ls /sys/class/udc > UDC
```

### Emulate Serial Adapter
- This is quite useful for debugging and is the easiest to setup.</br>
  to our init script, insert the following between the "functions" comments:
```bash
# Add functions here
mkdir -p functions/acm.usb0
ln -s functions/acm.usb0 configs/c.1/
# End functions
```
- Then, enable a console on the USB serial:
- To connect from the Pi to the attached Linux computer, use screen: `sudo screen /dev/ttyACM0 115200`
- Note: if screen terminates automatically, you may need to change the device file.</br>
  Consult for example dmesg: `dmesg | grep "USB ACM device"`

### Emulate Ethernet Adapter
- Add to init script:
```bash
# Add functions here
mkdir -p functions/ecm.usb0
# first byte of address must be even
HOST="48:6f:73:74:50:43" # MAC address host pc will see "HostPC"
SELF="42:61:64:55:53:42" # MAC address seen by rpi zero "BadUSB"
echo $HOST > functions/ecm.usb0/host_addr
echo $SELF > functions/ecm.usb0/dev_addr
ln -s functions/ecm.usb0 configs/c.1/
# End functions
ls /sys/class/udc > UDC

# PUT THIS AT THE VERY END OF THE FILE:
ifconfig usb0 10.0.0.1 netmask 255.255.255.252 up
route add -net default gw 10.0.0.2
```
- When you have problems with the automatic connection (e.g. "Wired Connection 2" on host computer),</br>
  disconnect and execute this: `dmesg | grep -i cdc_ether`</br>
  it will tell you, how your ethernet adapter is named \(and maybe renamed afterwards\).</br>
  Plug the interface name (enp0s20u1i2) into this line: `sudo ifconfig enp0s20u1i2 10.0.0.2 netmask 255.255.255.252 up`
- Then, connect via ssh from Pi to host pc: `ssh 10.0.0.2 -l pc_user`

### Emulate Keyboard / Mouse / Joystick (HID)
- Init script:
```bash
# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/
# End functions
```
- The simplest way to send keystrokes is by echoing HID packets to the device file:
  - Press \(HOLD\) \[A\]: `sudo bash -c 'echo -ne "\0\0\x4\0\0\0\0\0" > /dev/hidg0'`
  - Release ALL Keys: `sudo bash -c 'echo -ne "\0\0\0\0\0\0\0\0" > /dev/hidg0'`
- This isn’t practicable however, instead lets use girst's string to key-code converter instead
  - Download: `git clone https://github.com/girst/sendHID-mirror-of-git.gir.st.git`
  - Build: `cd sendHID-mirror-of-git.gir.st/; make`
  - Usage: `echo -n "hello world!" | sudo ./scan /dev/hidg0 1 2`</br>
    This will write the piped in string over the HID protocol.</br>
    The first argument "1" means US-Layout, a "2" in its place would be German/Austrian layout.</br>
    The second argument is for entering characters not available on your keyboard</br>
    i.e: 2=Linux \(3=Windows \(but no windows drivers\)\)

### Mass storage
Mass storage is somewhat difficult.</br>
You cannot share the Pi's partition with the host computer, but only a disk image file.</br>
I created a very small one to store the ethernet host configuration `sudo ifconfig …` on it.</br>
- First, lets make a disk image: `dd if=/dev/zero of=/media/usbdisk.img bs=1024 count=1024`</br>
  `bs=1024` blocksize 1Kb * `count=1024` = 1 Mbytes
- Format image as fat: `mkdosfs /media/usbdisk.img`
- Edit device script:
```bash
# Add functions here
FILE=/media/usbdisk.img
mkdir -p ${FILE/img/d}
mount -o loop,ro -t vfat $FILE ${FILE/img/d} # FOR IMAGE CREATED WITH DD
mkdir -p functions/mass_storage.usb0
echo 1 > functions/mass_storage.usb0/stall
echo 0 > functions/mass_storage.usb0/lun.0/cdrom
echo 0 > functions/mass_storage.usb0/lun.0/ro
echo 0 > functions/mass_storage.usb0/lun.0/nofua
echo $FILE > functions/mass_storage.usb0/lun.0/file
ln -s functions/mass_storage.usb0 configs/c.1/
# End functions
```
- A FAT32 formatted removable drive should show up, when you plug the Pi into a computer the next time.</br>
  To get access to the files stored on the disk-image from the Pi, you can unmount it completely</br>
  \(**in the host first, then in the pi**\), and remount it somewhere else.

### Others
There are about 20 different USB gadgets the Linux Kernel can emulate.</br>
Have a look at the [Kernel documentation] to find out more!


[iSticktoit]: http://www.isticktoit.net/?p=1383
[Kernel documentation]: https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt
[sendHID repo]: https://git.gir.st/sendHID.git