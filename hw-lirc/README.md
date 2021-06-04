### Pinout
IR_OUTPUT=18: gpio-ir-tx,gpio_pin=18
IR_INPUT=17: gpio-ir,gpio_pin=17
PIR_OUT=27: use gpio controller treat it as a momentary switch of sort

### Install & Configure
- Install lircd 0.10.1
  ```bash
  sudo apt-get install -y lirc
  ```
- Post Install:</br>
  Add the following lines to /boot/config.txt. Change pin numbers based on your own wiring.
  ```bash
  dtoverlay=gpio-ir,gpio_pin=17
  dtoverlay=gpio-ir-tx,gpio_pin=18
  ```
  **Note**: Since we are using gpio-ir, You don't have to add anything to /etc/modules.</br>
- Reboot
- Inspect lirc devices
  ```bash
  sudo cat /sys/kernel/debug/gpio
  ls -lh /dev/lirc*
  udevadm info -a /dev/lirc0
  udevadm info -a /dev/lirc1
  # or
  ls /dev/lirc* | xargs -I {} sudo udevadm info -a "{}"
  ```
- Disable devinput (default remote configuration of lirc).
  ```bash
  sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.{conf,dist}
  ```
- lircd Configuration:</br>
  lircd could be configured to monitor transmitter or receiver devices
  ```bash
  [lircd]
  driver = default
  device = /dev/lirc0
  ```
  device values:
    - /dev/lirc0: For ir_transmitter(gpio-ir-tx) device
    - /dev/lirc1: For ir_receiver(gpio-ir)
    - udevadm info -a /dev/lircX: Find out which is which
  device file number lircX could be changed arbitrary by the underlying OS so if everything stopped working without probable cause, </br>
  inspect device with `udevadm info -a /dev/lirc0` again may provide you with some clue.
- lircmd Usage:</br>
  Read Mode: When using following commands: "irrecord -n", "mode2", "irw", and "irexec".</br>
  Please note that there is no need to add "-d" option with the configuration below.
  ```bash
  [lircmd]
  driver = default
  device = /dev/lirc1
  ```
  Although mode2 could be used with -d /dev/lirc1 and does not require lircd to be listening to /dev/lirc1
  ```
  mode2 -d /dev/lirc1
  ```
  Which is very useful for debugging transmitter (which needs lircd to manage that device to work)</br>
  Write Mode:</br>
  When using lircd in transmitter mode with the command irsend, please edit /etc/lirc/lirc_options.conf as follows.
  ```bash
  [lircd]
  driver = default
  device = /dev/lirc0
  [lircmd]
  driver = default
  device = /dev/lirc0
  ```
  Same as above, as long as you have configured your device in the lircmd block, there is no need to use "-d" flag to specify the device to use
  Restarting lircd is required. Some commandline example:
  ```bash
  # List available transmitter commands
  irsend LIST LEGO_Combo_Direct ''
  # Send a particular signal ONCE
  irsend SEND_ONCE LEGO_Combo_Direct FORWARD_FORWARD
  # Send repeated signal (#youspinmerightroundbabyrightround)
  irsend SEND_START LEGO_Combo_Direct FORWARD_BACKWARD ; sleep 3
  irsend SEND_STOP LEGO_Combo_Direct FORWARD_BACKWARD
  ```

### Resources
[irsend]: https://www.lirc.org/html/irsend.html
[LEGO power functions config files]: https://github.com/iConor/lego-lirc/tree/master/config-files
[Deprecated lirc9x+stretch Guide1]: https://www.raspberry-pi-geek.com/Archive/2015/10/Raspberry-Pi-IR-remote
[Deprecated lirc9x+stretch Guide2]: http://alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/
