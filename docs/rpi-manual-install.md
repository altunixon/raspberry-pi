#### Clone current system (create a flash-compatible image)
- Prequisites: </br>
  We will need a partition editor in-order to shrink the created image, either parted or fdisk will do. </br>
  Since parted is quite commonly used (and newer) so we will use that. </br>
  ```bash
  sudo apt-get install parted losetup tune2fs md5sum e2fsck resize2fs
  ```
- **Before Continuing:** </br>
  Makesure you have everything you need on the root partition (on the main disk, the one that has boot & root partition) </br>
  **Disable & Delete Swap** partition if you have any. </br>
  ```bash
  free -m
  swapoff -a
  # Comment Swap mount in fstab if needed
  vim /etc/fstab
  ```
  Backup if you're paranoid.
- Shrinking disk (sdcard):
  ```bash
  lsblk
  parted -l /dev/mmcblk
  # Delete Swap partition if any then shrink sdcard, below is just a representation, ymmv
  parted /dev/mmcblk
  GNU Parted 3.2
  Using /dev/mmcblk
  Welcome to GNU Parted! Type 'help' to view a list of commands.
  (parted) p
  Model: ATA VBOX HARDDISK (scsi) <-- This is the device name and type
  Disk /dev/mmcblk: 16.1GB
  Sector size (logical/physical): 512B/512B
  Partition Table: msdos
  Disk Flags:

  Number  Start   End     Size    Type     File system     Flags
   1      1049kB  538MB   537MB   primary  ext4            boot
   2      538MB   11.3GB  10.7GB  primary  ext4
   3      11.3GB  12.3GB  1074MB  primary  linux-swap(v1)  <-- Lookout for swap partition

  (parted) rm 3  <-- First we need to delete swap partition
  (parted) p
  Model: ATA VBOX HARDDISK (scsi)
  Disk /dev/mmcblk: 16.1GB
  Sector size (logical/physical): 512B/512B
  Partition Table: msdos
  Disk Flags:

  Number  Start   End     Size    Type     File system  Flags
   1      1049kB  538MB   537MB   primary  ext4         boot
   2      538MB   11.3GB  10.7GB  primary  ext4

  (parted) u  <-- Change the unit type to sector to avoid any risk of loosing data when you resize root partition
  Unit?  [compact]? s
  (parted) p <-- Print the available partition table
  Model: ATA VBOX HARDDISK (scsi)
  Disk /dev/mmcblk: 31457280s
  Sector size (logical/physical): 512B/512B
  Partition Table: msdos
  Disk Flags:

  Number  Start     End        Size       Type     File system  Flags
   1      2048s     1050623s   1048576s   primary  ext4         boot
   2      1050624s  22022143s  20971520s  primary  ext4			<--- Note down the start sector number, this will be used in next step

  (parted) rm 2 <-- We will delete the root partition's entry. This will not impact the content of root partition and only partition table is modified. 
  Warning: Partition /dev/mmcblk0 is being used. Are you sure you want to continue?
  Yes/No? Yes
  Error: Partition(s) 2 on /dev/mmcblk have been written, but we have been unable to inform the kernel of the change, probably because
  it/they are in use.  As a result, the old partition(s) will remain in use.  You should reboot now before making further changes.
  Ignore/Cancel? Ignore  <-- If you reboot your server at this stage then you may end up with a broken node so don't reboot your node at this stage.
  (parted) p <-- Print the current partition table
  Model: ATA VBOX HARDDISK (scsi)
  Disk /dev/mmcblk: 31457280s
  Sector size (logical/physical): 512B/512B
  Partition Table: msdos
  Disk Flags:

  Number  Start  End       Size      Type     File system  Flags
   1      2048s  1050623s  1048576s  primary  ext4         boot

  (parted) mkpart <-- Now we will create root partition with new size
  Partition type?  primary/extended? primary
  File system type?  [ext2]? ext4
  Start? 1050624s  <-- Here give the start sector as it was earlier for root partition
  End? 24022143s  <-- Give the new end sector higher than the earlier value to resize root partition
  (parted) p  <-- Print the new partition table after you extend non lvm root partition
  Model: ATA VBOX HARDDISK (scsi)
  Disk /dev/mmcblk: 31457280s
  Sector size (logical/physical): 512B/512B
  Partition Table: msdos
  Disk Flags:

  Number  Start     End        Size       Type     File system  Flags
   1      2048s     1050623s   1048576s   primary  ext4         boot
   2      1050624s  24022143s  22971520s  primary  ext4         lba

  (parted) quit  <-- We are all done here
  Information: You may need to update /etc/fstab.
  ```
- To complete the steps to resize non lvm root partition, execute resizefs to expand partition and refresh the changes
  ```bash
  resize2fs /dev/mmcblk0
  ```
  Reboot for good measures (and to see if your shrunked partition still works)
- Create disk image: </br>
  Since the primary storage device is now shrunk, you will need to connect an external drive to store the created image. </br>
  Create image with dd:
  ```bash
  dd if=/dev/mmcblk of=/media/external_drive/clone.img
  # Optional, compress image for smaller footprint
  gzip -9 /media/external_drive/clone.img
  ```
- Extra: </br>
  Seems there is a utility scrip to shrink the raw image created with dd over @https://github.com/Drewsif/PiShrink </br>
  ```bash
  wget https://github.com/Drewsif/PiShrink/blob/master/pishrink.sh
  chmod +x pishrink.sh
  sudo ./pishrink.sh /media/external_drive/clone.img /media/external_drive/clone-shrunk.img 
  ```
  But theres too much magick in there, i dont really reccommend it if you're not sure what it actually does </br>
  Mount image as loopback device then shrink the loopback device's partition? like i said, magick.
  
#### Creating the layout
- On an empty Micro SD card:
  ```bash
  # Open fdisk on your card.
  fdisk /dev/sda
  # 1. Press “n” to create a partition.
  # 2. Press “p” to make it a primary partition.
  # 3. Press “1” to make it the first partition in the table.
  # 4. Type "8192" to set the start sector. (mimicking original rpi image) or press <enter> to use default start sector which is 2048.
  # 5. Type +size to choose the size. In my case I want 512MB, so I’ll type “+512M”.
  # 6. After it’s created, press “a” to make it bootable.
  # 7. Now we press “p” to print and view the partition table, as shown below.
  Command (m for help): p
   Disk /dev/sda: 3.7 GiB, 3965190144 bytes, 7744512 sectors
   Geometry: 122 heads, 62 sectors/track, 1023 cylinders
   Units: sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x4eb27b84
   Device     Boot Start     End Sectors Size Id Type
   /dev/sda1  *     8192 2099199 2097152   1G 83 Linux
  # 8. Now we need to set the partition type. Press “t” to set a partition type, choose the partition, and type “c” for “W95 FAT32 (LBA)”.
  # We’re now left with this partition table.
  Disk /dev/sda: 59.6 GiB, 64021856256 bytes, 125042688 sectors
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x4eb27b84
  Device     Boot  Start       End   Sectors  Size Id Type
  /dev/sda1  *     8192     532479   524288   256M  c W95 FAT32 (LBA) <-- Default boot partition info, our newly created partition should resemble this
  # 9. Press “w” to write and save, and exit fdisk.
  # 10. We now need to format the partition. Run the following command on your device.
  mkfs.vfat /dev/sda1
  # 11. Finally, you can now set a label to the partition. 
  #     Ubuntu uses the label “system-boot” whereas Raspbian uses “boot”. You can set it with the following command:
  fatlabel /dev/sda1 NEW_LABEL
  ```
- You now have a clean partition layout that can be used to boot a Raspberry Pi. </br>
  Remember that this is just the partition layout and the files are still needed from an image or your current running instance. </br>
  These can simply be copied over from a raspbian image mounted as a loopback device. </br>
  ```bash
  # Inspect image layout
  fdisk -l disk.img
  # Mount multipart disk image with losetup (util-linux >= 2.21 / Ubuntu 16.04)
  sudo losetup -Pf disk.img
  # or with other utilities
  sudo kpartx -a -v file.iso
  sudo partx -a -v file.iso
  ```
  If you need just a simple boot partition, you don’t need to purchase large Micro SD cards.
