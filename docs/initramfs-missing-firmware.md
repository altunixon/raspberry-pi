### W: Possible missing firmware /lib/firmware/rtl_nic/rtl8156b-2.fw for built-in driver r8152
Solved by downloading firmware files and including them into initramfs:
[Rtl Firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/)
```bash
mkdir r8152
cd r8152
wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/rtl8156a-2.fw
wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/rtl8156b-2.fw
wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/rtl8153c-1.fw
sudo cp *.fw /lib/firmware/rtl_nic/
sudo /usr/sbin/update-initramfs -b /media/ramdisk/ -c -k $(uname -r)
```