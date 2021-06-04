#### PiHole [Official Document](https://docs.pi-hole.net/main/basic-install/)
- Install latest pihole service directly from commandline:
  ```bash
  curl -sSL https://install.pi-hole.net | bash
  ```
  Or download and run the install script:
  ```bash
  wget https://install.pi-hole.net -O ./pihole-install.sh
  sudo bash ./pihole-install.sh
  ```
  Either way, it'll take a while to complete the installation. </br>
  Wait for the process to complete, and you should be able to access [pihole admin console](http://localhost/admin/) with the provided password. </br>
  At this point you should have a running pihole service, if you intend to run pihole on a read-only filesystem, readon.
  
- Edit pihole.service file to support read-only filesystem
- Edit lighthttpd.service file to suport read-only filesystem
