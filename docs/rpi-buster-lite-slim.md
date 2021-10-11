## Mount Image file to copy root

## Chroot 
```bash
for name in proc sys dev ; do sudo mount --bind /$name /media/alt/buster-lite-slim/$name; done
sudo chroot /media/alt/buster-lite-slim /bin/bash
```

## Disable sdcard auto resize
```bash
update-rc.d resize2fs_once remove
ls -l /etc/init.d/resize2fs_once
rm /etc/init.d/resize2fs_once
```

## Purge packages
```bash
export LC_ALL="C"
apt-get update

dpkg-query -Wf '${binary:Package}\n' 'lib*[!raspberrypi-bin]' | xargs apt-mark auto
dpkg-query -Wf '${Package;-40}${Priority}\n' | sort -b -k2,2 -k1,1 | grep optional | awk '{print $1}' | xargs -I {} apt purge -y "{}"
dpkg-query -Wf '${Package;-40}${Priority}\n' | sort -b -k2,2 -k1,1 | grep extra | awk '{print $1}' | xargs -I {} apt purge -y "{}"
dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n

apt-get install --no-install-recommends procps iproute2
apt-get upgrade
apt-get autoremove -y
```

## Quit chroot
```bash
exit
for name in proc sys dev ; do sudo umount /media/alt/buster-lite-slim/$name; done
```