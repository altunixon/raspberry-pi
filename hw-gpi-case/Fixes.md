### Mount multi partition image in order to use rsync instead of flashing them with dd
- Use fdisk to list image's patitions `fdisk -l /path/to/file.img`
- Take note of the 
  - `Units: sectors of 1 * 512 = 512 bytes` or rather, `Sector size (logical/physical): 512 bytes / 512 bytes` and
  - Device's `./GPi-Case-Users-v1.2-final.img1 *      8192   499711   491520  240M  e W95 FAT16 (LBA)` start sector, in this case, 8192
- Calculate the offset value \(start of partition in bytes\): offset = sector\_start(8192) * sector\_size(512)
- Mount image as loop device statting from the data offset location:
  ```bash
  fdisk -l ./GPi-Case-Users-v1.2-final.img
  #Disk ./GPi-Case-Users-v1.2-final.img: 5.9 GiB, 6269719040 bytes, 12245545 sectors
  #Units: sectors of 1 * 512 = 512 bytes
  #Sector size (logical/physical): 512 bytes / 512 bytes
  #Device                           Boot  Start      End  Sectors  Size Id Type
  #./GPi-Case-Users-v1.2-final.img1 *      8192   499711   491520  240M  e W95 FAT16 (LBA)
  #./GPi-Case-Users-v1.2-final.img2      499712 12245544 11745833  5.6G 83 Linux
  sudo mount -o "loop,offset=$((8192 * 512))" ./GPi-Case-Users-v1.2-final.img /media/alt/iso
  sudo mount -o "loop,offset=$((499712 * 512))" ./GPi-Case-Users-v1.2-final.img /media/alt/iso

  fdisk -l ./2021-03-04-raspios-buster-armhf-lite.img
  sudo mount -o "loop,offset=$((532480 * 512))" ./2021-03-04-raspios-buster-armhf-lite.img /media/alt/iso
  sudo mount -o "loop,offset=$((8192 * 512))" ./2021-03-04-raspios-buster-armhf-lite.img /media/alt/iso
  ```
- Sync iso to sdcard
  ```bash
  sudo mount -o "loop,offset=$((8192 * 512))" $HOME/Downloads/GPi-Case-Users-v1.2-final.img /media/alt/iso
  cd /media/$USER/sdcard/boot
  rm -rf /media/$USER/sdcard/boot/*
  sudo rsync -avH --ignore-existing /media/alt/iso/ /media/$USER/sdcard/boot/
  sudo umount /media/alt/iso
  sudo mount -o "loop,offset=$((499712 * 512))" $HOME/Downloads/GPi-Case-Users-v1.2-final.img /media/alt/iso
  cd /media/$USER/sdcard/
  sudo rm -rf bin/ dev/ etc/ lib/ lost+found/ media/ mnt/ proc/ root/ run/ sbin/ srv/ sys/ tmp/ usr/ var/
  sudo rm -rf home/pi/RetroPie/{retropiemenu/,splashscreens/} home/pi/RetroPie-Setup/ home/pi/.*
  sudo rm -rf opt/RetroFlag/ opt/bootlogos/ opt/retropie/
  cat << EOT >> /tmp/iso-exclude.txt
  *var/swap*
  *var/run*
  *home/pi/RetroPie/roms*
  EOT
  sudo rsync -avH --ignore-existing --exclude-from=/tmp/iso-exclude.txt /media/alt/iso/ /media/$USER/sdcard/
  sudo umount /media/alt/iso
  ```
- Edit `boot/cmdline.txt` and `etc/fstab` to reflect current sdcard's PARTUUID
- Add ssh and wpa_supplicant.conf files to sdcard's `/boot/` folder:
  ```
  sudo touch /boot/ssh
  sudo cp wpa_supplicant.conf /boot/
  ```
- Add neccessary links to emulators \(bios, memcards and such\)
  ```
  sudo ln -s /home/pi/RetroPie-Data/pcsx-memcards opt/retropie/configs/psx/pcsx/memcards
  sudo ln -s /home/pi/RetroPie/BIOS/scph1001.bin opt/retropie/emulators/pcsx-rearmed/bios/SCPH1001.BIN 
  sudo ln -s /home/pi/RetroPie/BIOS/scph101.bin  opt/retropie/emulators/pcsx-rearmed/bios/scph101.bin 
  sudo ln -s /home/pi/RetroPie/BIOS/scph5501.bin opt/retropie/emulators/pcsx-rearmed/bios/scph5501.bin 
  sudo ln -s /home/pi/RetroPie/BIOS/scph7001.bin opt/retropie/emulators/pcsx-rearmed/bios/scph7001.bin 
  ```

### \[ERROR\] XboxdrvDaemon::launch\_controller\_thread\(\): USB device disappeared before it could be opened
The driver for the xbox controller built into the kernel (xpad) seems to be quite broken.
so let's disable it and use xboxdrv instead.
- Blacklist xpad kernel driver -> this results in the gpicase controller not get recognized
  ```bash
  sudo bash -c 'echo "blacklist xpad" >> /etc/modprobe.d/blacklist.conf'
  sudo rmmod xpad
  ```
- Install xboxdrv via retropie install script > Manage Packages > Drivers > xbox driver

### lvl0: VolumeControl::init\(\) - [Failed to find mixer elements!]
A recent change in [Raspbian Buster's kernel/firmware updates for May 2020] is causing Audio/Sound issues for RPI users - users that installed the 4.6 image or installed RetroPie manually on-top of Raspbian Buster.</br>
Symptoms include:
- Error messages showing when a game is launched \(lvl0: VolumeControl::init\(\) - Failed to find mixer elements\).
- Sound missing in EmulationStation and/or games.
- System Volume slider stuck at 0% in EmulationStation's Sound settings.

To verify if you're affected by the audio changes, you can check your Raspbian Linux kernel version with `uname -r`, if it's 4.19.118 or later, your system is affected.
To solve this issue\(s\), here is a list of steps need to be taken:
- [update your RetroPie-Setup] installation.
- use the Audio menu in RetroPie to choose your Audio output \(HDMI/Headphones\).</br>
  This will set the default Sound card/device for your system, but wouldn't always solve the problem of missing audio in EmulationStation.
- [update the EmulationStation core package] - you should have at least version v2.9.2.
- Re-configure your Sound in EmulationStation, depending on how your sound output is configured.</br>
  The table below shows the Sound settings as they worked before the update and how they should be configured after the update is applied.
  Audio output|Before the update|After the update
  HDMI|Audio Card: Default, Audio Device: PCM, OMX Audio Device: HDMI|Audio Card: Default, Audio Device: HDMI, OMX Audio Device: ALSA
  Headphone Jack|Audio Card: Default, Audio Device: PCM, OMX Audio Device: Local|Audio Card: Default, Audio Device: Headphone, OMX Audio Device: ALSA
Notes:
- If you're using an external \(USB/I2S/etc.\) soundcard, you might be affected by the change - the system configures now \(at least\) 2 sound cards instead of 1 \(as it was the default before the update\). If you've disabled the on-board sound, then you shouldn't be affected.
- RetroPie users still using an a system based on Raspbian Strech should not be affected by this change, since Raspbian no longer provides any updates for this version.
- Optional if you wish to revert to the previous Audio configuration, then you can add to `/boot/cmdline.txt`
  `snd_bcm2835.enable_hdmi=1 snd_bcm2835.enable_headphones=1 snd_bcm2835.enable_compat_alsa=1`


[Failed to find mixer elements!]: https://retropie.org.uk/forum/topic/26628/audio-issues-after-latest-raspbian-updates-june-2020
[Raspbian Buster's kernel/firmware updates for May 2020]: https://www.raspberrypi.org/blog/latest-raspberry-pi-os-update-may-2020/
[update your RetroPie-Setup]: https://retropie.org.uk/docs/Updating-RetroPie/
[update the EmulationStation core package]: https://retropie.org.uk/docs/Updating-RetroPie/#updatinginstalling-individual-packages
