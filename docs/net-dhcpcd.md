## With-OUT predictive interface name
Disable predictive interface name by adding `net.ifnames=0 biosdevname=0` to `/boot/cmdline.txt`</br>
First, remove the `interface eth0:?` stuff in `/etc/dhcpcd.conf` - but keep the entries for `interface eth0` if that exists.</br>
Or better yet, add/replace them with `denyinterfaces eth0:?` to tell dhcpcd to ignore `eth0:?`</br>
Create a file in `/etc/network/interfaces.d` - call it whatever eth0-subs or something, the name doesn't matter since the `/etc/network/interfaces` file includes the whole directory</br>
Content:
```bash
auto eth0:1
allow-hotplug eth0:1
iface eth0:1 inet static
    vlan-raw-device eth0
    address 192.168.11.53
    netmask 255.255.255.0
    gateway 192.168.11.1

auto eth0:2
allow-hotplug eth0:2
iface eth0:2 inet static
    vlan-raw-device eth0
    address 192.168.11.69
    netmask 255.255.255.0
    gateway 192.168.11.1
```

## WITH predictive interface name
NOTE: I've enabled predictable interface names and I found it is impossible to create such "sub-interfaces" at all
</br>
i.e. even ifconfig enxXXXXXXXXXXXX:0 192.168.1.3 just changes the IP address of enxXXXXXXXXXXXX and does not "create" a sub-interface
</br>
OK - for those who use "predictable interface names"
```bash
auto enxb827ebXXXXXX
allow-hotplug enxb827ebXXXXXX

iface enxb827ebXXXXXX inet static
  address 192.168.0.71
  netmask 255.255.255.0

iface enxb827ebXXXXXX inet static
  address 192.168.0.72
  netmask 255.255.255.0

iface enxb827ebXXXXXX inet static
  address 192.168.0.73
  netmask 255.255.255.0
```

ifconfig in this case will probably show 192.168.0.71 as the primary for enxb827ebXXXXXX - but ip address show will show all four addresses, with 0.24 as the last secondary - if this is an issue, then remove the eth0 entry in /etc/dhcpcd.conf, and add
```bash
iface enxb827ebXXXXXX inet static
  address 192.168.0.71
  netmask 255.255.255.0
  gateway 192.168.0.1
```
just below allow-hotplug