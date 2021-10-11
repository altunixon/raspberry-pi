# Slimming Down Raspbian Stretch Lite

Notes for slimming down a fresh installation of Raspbian Stretch Lite.
This guide does not strip Raspbian of basic functionality such as Bluetooth and mDNS.

## Instructions

Install a fresh Raspbian Stretch Lite image into the SD card ([source][1]).

    $ unzip -p 2018-04-18-raspbian-stretch-lite.zip | dd bs=4M of=/dev/sdX conv=fsync
    $ sync
   
Configure headless SSH and Wi-Fi (if necessary) before starting the SD card ([source][2]).

    $ mount /dev/sdX /media
    $ :> /media/ssh
    $ cat > /media/wpa_supplicant.conf <<"EOF"
    country=GB
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    
    network={
        ssid="YOUR_SSID"
        psk="YOUR_PSK"
    }
    EOF
    $ umount /media
    $ sync

Configure `apt` so that it does not install additional packages ([source][3]).

    $ cat > /etc/apt/apt.conf.d/80noadditional <<"EOF"
    APT::Install-Recommends "0";
    APT::Install-Suggests "0";
    EOF

Update Raspbian in the freshly installed system.

    $ apt-get update
    $ apt-get dist-upgrade
    $ reboot

Mark all libraries as autoinstalled, so they are autoremoved when no longer required.

    $ dpkg-query -Wf '${binary:Package}\n' 'lib*[!raspberrypi-bin]' | xargs apt-mark auto

Remove non-critical packages.

    $ xargs apt-get purge <<"EOF"
    aptitude aptitude-common apt-listchanges apt-utils bash-completion blends-tasks build-essential
    bzip2 cifs-utils console-setup console-setup-linux cpp debconf-i18n dmidecode dosfstools
    dpkg-dev ed gcc gcc-4.6-base gcc-4.7-base gcc-4.8-base gcc-4.9-base gcc-5-base gcc-6 gdb
    geoip-database gettext-base groff-base hardlink htop info install-info iptables iputils-ping
    isc-dhcp-client isc-dhcp-common kbd keyboard-configuration less libc-l10n libglib2.0-data
    liblocale-gettext-perl libtext-charwidth-perl libtext-iconv-perl libtext-wrapi18n-perl locales
    logrotate luajit make manpages manpages-dev mime-support mountall ncdu netcat-openbsd
    netcat-traditional net-tools nfs-common perl plymouth python rpcbind rsync rsyslog samba-common
    sgml-base shared-mime-info strace tasksel tasksel-data tcpd traceroute triggerhappy unzip
    usb-modeswitch usb-modeswitch-data usbutils v4l-utils vim-common vim-tiny wget xauth
    xdg-user-dirs xxd xz-utils zlib1g-dev
    EOF

Remove all packages that were automatically installed and are no longer required.

    $ apt-get autoremove --purge

## Optionals

Configure `dpkg` so that it does not install documentation in packages ([source][4]).

    $ cat > /etc/dpkg/dpkg.cfg.d/nodoc <<"EOF"
    path-exclude /usr/share/doc/*
    path-include /usr/share/doc/*/copyright
    path-exclude /usr/share/man/*
    path-exclude /usr/share/groff/*
    path-exclude /usr/share/info/*
    path-exclude /usr/share/lintian/*
    path-exclude /usr/share/linda/*
    EOF

Configure `dpkg` so that it does not install locales in packages.

    $ cat > /etc/dpkg/dpkg.cfg.d/nolocale <<"EOF"
    path-exclude /usr/share/locale/*
    EOF

Remove documentation from already installed packages ([source][4]).

    $ find /usr/share/doc -depth -type f ! -name copyright | xargs rm
    $ find /usr/share/doc -empty | xargs rmdir
    $ rm -rf /usr/share/man/* /usr/share/groff/* /usr/share/info/*
    $ rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/*

Remove locales from already installed packages.

    $ rm -rf /usr/share/locale/*

Remove log files.

    $ rm -f /var/log/{auth,boot,bootstrap,daemon,kern}.log
    $ rm -f /var/log/{debug,dmesg,messages,syslog}

Empty the Message-Of-The-Day file.

    $ :> /etc/motd

Generate a unique hostname based on MAC address during boot.

    $ cat > /etc/systemd/system/mac-hostname.service <<"EOF"
    [Unit]
    Description=MAC-based hostname
    DefaultDependencies=no
    After=sysinit.target local-fs.target
    Before=basic.target
    
    [Service]
    Type=oneshot
    ExecStart=/bin/bash -c '\
        _HOSTNAME=$(sed "s/^.*macaddr=\\([0-9A-F:]*\\) .*$/\\1/;s/://g;s/\\(.*\\)/rpi-\\L\\1/" /proc/cmdline); \
        if [ "$_HOSTNAME" ]; then \
            _CURRENT_HOSTNAME=$(cat /etc/hostname | tr -d " \\t\\n\\r"); \
            if [ "$_HOSTNAME" != "$_CURRENT_HOSTNAME" ]; then \
                echo "Setting MAC-based hostname to <$_HOSTNAME>"; \
                echo "$_HOSTNAME" > /etc/hostname; \
                sed -i "s/127.0.1.1.*$_CURRENT_HOSTNAME/127.0.1.1\\t$_HOSTNAME/g" /etc/hosts; \
                /bin/hostname -b -F /etc/hostname; \
            fi; \
        fi'
    
    [Install]
    WantedBy=basic.target
    EOF
    $ systemctl enable mac-hostname.service
    $ reboot

Disable onboard Bluetooth device (RPI0W, RPI3).

    $ echo dtoverlay=pi3-disable-bt >> /boot/config.txt
    $ systemctl disable hciuart
    $ apt-get purge bluez bluez-firmware pi-bluetooth  # if BT is not needed again

## References

[1]: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md
[2]: https://www.raspberrypi.org/forums/viewtopic.php?t=191252
[3]: https://wiki.debian.org/ReduceDebian
[4]: https://askubuntu.com/a/401144