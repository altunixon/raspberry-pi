## Mount image to rsync instead of flashing them
```bash
fdisk -l ./2021-03-04-raspios-buster-armhf-lite.img
sudo mount -o "loop,offset=$((532480 * 512))" ./2021-03-04-raspios-buster-armhf-lite.img /media/alt/iso
sudo mount -o "loop,offset=$((8192 * 512))" ./2021-03-04-raspios-buster-armhf-lite.img /media/alt/iso

fdisk -l ./GPi-Case-Users-v1.2-final.img
sudo mount -o "loop,offset=$((8192 * 512))" ./GPi-Case-Users-v1.2-final.img /media/alt/iso
sudo mount -o "loop,offset=$((499712 * 512))" ./GPi-Case-Users-v1.2-final.img /media/alt/iso
```
**Note**: edit `boot/cmdline.txt` and `etc/fstab` to reflect current sdcard's PARTUUID
