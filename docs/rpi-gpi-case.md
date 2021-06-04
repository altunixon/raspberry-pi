# Migrated to gpi-case repo, this file wont be undate anymore

## Community Images
See the bottom of this file, at Resources, the UserGroup's 4.5.1-v1.2 image seems promising

## Raspbian
### 1. Flash raspbian \(-lite preferable\) image to your sd card

### 2. ~Expand the root filesystem~ Raspbian now automatically expands the filesystem so that step is no longer necessary.

### 3. Install update `sudo apt update && sudo apt upgrade`

### 4. Verify Locale Settings
Most of the install scripts will attempt to install a variety of packages and libraries that each emulator requires.</br>
These installations will fail if your system locale settings are invalid.</br>
You can easily verify this by executing the `locale` command.</br>
A valid locale will return values set for all options, such as in the example below.
```bash
locale
LANG=en_US.UTF-8
LANGUAGE=en_US:en
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=en_US.UTF-8
```
If any of the above configuration lines are unset (particularly LANG, LANGUAGE, and LC_ALL), you should set them before installing RetroPie.</br>
The easiest way to set each item is to use the `update-locale` command, such as `sudo update-locale LC_ALL="en_US.UTF-8"`.</br>
Users can also set the locale through the `raspi-config` tool.</br>
A reboot is required before these changes will be reflected by the locale command.
    
### 5. Verify the allocated video memory (memory split)
Running Emulationstation requires a larger than default GPU memory split.</br>
Make sure you reserve enough memory for EmulationStation by modifying the `/boot/config.txt` configuration file </br>
or by using `raspi-config` as described in the [Memory Split] page.</br>
**Note**:
- Raspberry Pi 4:</br>
  On the Raspberry Pi 4 the 3D component of the GPU has its own memory management unit (MMU), and does not use memory from the gpu_mem allocation. </br>
  Instead memory is allocated dynamically within Linux.</br>
  Increasing this amount can harm emulation performance.
- Raspberry Pi 0-3:</br>
  If you don't use the RetroPie provided image, and you install using the manual installation method, </br>
  you have to adjust the memory split settings manually before installation to reserve at enough video memory for running Emulationstation without problems.</br>
  The default values used by the RetroPie image are:
  ```bash
  vim /boot/config.txt
  gpu_mem_256=128
  gpu_mem_512=256
  gpu_mem_1024=256
  ```
  In order to ensure sensible memory splits across older Pi models, the RetroPie Pi image uses the gpu_mem_256, gpu_mem_512 and gpu_mem_1024 overrides, </br>
  which apply to Pis with that amount of memory (for example, the Pi 2 has 1024MB memory, so will use the gpu_mem_1024 setting).</br>
  These settings override the gpu_mem setting, so if you still want to adjust the memory split, you will have to manually edit `/boot/config.txt` and adjust the relevant value, or delete the lines entirely.
- These defaults should be adequate, and you can test via observing the GPU memory usage whilst an emulator is running.</br>
  A complex display of the GPU memory usage can be viewed with: `sudo vcdbg reloc`
- A reboot is required after any modifications to the video memory allocation.

### 6. [Install Retropie] packages
1. Install the needed packages for the RetroPie setup script:
    ```bash
    sudo apt install git lsb-release
    ```
    
2. Download the latest RetroPie setup script:
    ```bash
    git clone --depth=1 https://github.com/RetroPie/RetroPie-Setup.git
    cd RetroPie-Setup
    chmod +x retropie_setup.sh
    sudo ./retropie_setup.sh
    ```
    
3. Full Install `Setup >> Basic Install >> Quick Install`
    This will install the core and main packages which are equivalent to what is provided with the RetroPie SD image.</br>
    Now, you have to copy your rom files into the ROMs directory.</br>
    If you followed the steps above the main directory for all ROMs is `~/RetroPie/roms` (or `/home/pi/RetroPie/roms`, which is the same here).</br>
    In this directory there is a subdirectory for every emulated system, e.g., nes, snes, megadrive.</br>
    Attention has to be taken for the extensions of the ROM files.</br>
    All the information needed for each system is detailed in this wiki \(see [emulator wiki home page] or sidebar for systems\)</br>
    EmulationStation can be run from the terminal with `emulationstation` command.
    
4. Partial Install `Managed Packages >>`
    Say you don't want to bloat your system with all of RetroPie - you also have the option to only install the emulators you want.</br>
    When you select Manage Packages, you will first want to start by installing the core packages.</br>
    - **Core Packages**:</br>
      The core components needed for RetroPie to function are:
      - **RetroArch**: Frontend for the libretro api, necessary for most emulators to run.
      - **EmulationStation**: Frontend for sorting and launching all of your games.
      - **RetroPie Menu**: Menu in emulationstation for simpler configuration of your system.
      - **Runcommand**: The runcommand launch menu that assists launching your games with proper configurations, see the related Runcommand documentation page.
    - Main / Optional / Experimental:</br>
      Emulators can be installed and updated individually from the Main, Optional, and Experimental packages.</br>
      **NOTE**: If you intend to run ROMs from a USB drive or use an USB drive for transferring ROMs, </br>
      don't forget to install and enable the `usbromservice`, located in the Optional packages section.
    - Samba Roms: If you want to use Samba shares you can set them up from the setup/tools option of the RetroPie setup script.



### 8. Further Optimizations:
On Debian Jessie add ` consoleblank=0` to the existing line in `/boot/cmdline.txt` (with a space before it so it's an additional parameter).</br>
This prevents the screenblanker kicking in. With it, runcommand dialog is always displayed.
There is also a gui option in `RetroPie-Setup -> Configuration / Tools -> Raspbian Tools` to disable the blanker, but it doesn't work in Jessie due to a Debian bug.

### 9. [FAQ]
- Q: How doth one [Boot to EmulationStation]?</br>
  A: In retropie `setup script >> Configuration / tools >> autostart`:
  - Start EmulationStation at Boot: Boots into EmulationStation.
  - Start Kodi at Boot: Boots into Kodi- if you exit Kodi you will be returned to EmulationStation.
  - Manually Edit `/opt/retropie/configs/all/autostart.sh`: you can manually add other programs to start on boot.
  - Boot to text console (autologin): Boots into the terminal.
  - Boot to Desktop: If you have a desktop environment installed like LXDE this will boot into the desktop.</br>
    **Note**: you'll want to disable the retropie splash from the setup script first.

- Q: How do I remove the black borders?</br>
  A: See [Overscan]

- Q: How would I start from command line, say, the SNES emulator by itself?</br>
  A: First you need to make sure your emulators and systems are configured and working properly from EmulationStation.</br>
  To manually start a specific system and a game from the command line, use runcommand as shown below, replacing</br>
  \<SYSTEM\>: with the system you want (nes, snes, gba, arcade, ...) and </br>
  \<ROM\>: with the full path to the ROM to launch (example: $HOME/RetroPie/roms/snes/My Rom.smc).</br>
  `/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ "<SYSTEM>" "<ROM>"` </br>
  To automatically start a specific system and a game directly instead of EmulationStation, you need to edit `/opt/retropie/configs/all/autostart.sh` and add the above line (again replacing the variables with your own values).</br>
  Then, in the same file, remove any line containing `#auto` entirely to avoid EmulationStation or KODI to autostart again.
    
### Retropie
PLACEHOLDER

## Prepare /boot partition for headless WiFi & SSH
- Enable SSH: create a empty "ssh" file `touch ssh` in the /boot partition(fat) of the sdcard
- Headless WiFi: create a "wpa_supplicant.conf" file on the same partition with the following content
  ```txt
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=US

  network={
    ssid="<Name of your wireless LAN>"
    psk="<Password for your wireless LAN>"
  }
  ```
- **Notes**:
  - Depending on the OS and editor you are creating this on, the file could have incorrect newlines or the wrong file extension so make sure you use an editor that accounts for this.</br>
    Linux expects the line feed (LF) newline character. Notepad++ seems to be a safe bet (just remember to set file format to Unix and endline to LF)
  - The Pi zero w does **NOT support 5g wifi** and even some older dongles also do not, so stick with **2.4g**

## Hardware Installation Notes ([Guide with images])
### 1. Before you start, make sure the case's main power switch is in the OFF position.
### 2. Install the micro USB extension cable
Insert the included micro USB extension ribbon cable into the Pi's micro USB **data** port.</br>
This is the port closer to the center of the Pi.
### 5. Attach the IO conversion board
Carefully lower the IO conversion board into place so that it lines up with the Pi.</br>
**Note**: Make sure that the micro USB **extension ribbon cable** is out of the way (not under the IO pcb) before screwing the board down!</br>
Then, slide the brown cable retaining clip outward, insert the USB extension cable, and then slide the retaining clip back to secure the cable.
### 9. Install the GPi Case patch
Because RetroPie and Recalbox output video via HDMI by default, we need to configure it to output over the GPIO header instead.</br>
Retroflag wrapped this, and other configuration settings, into a small patch file that needs to be run.</br>
Download the patch ZIP file from the [Retroflag downloads page] or [directly]. Unzip the file, and then:
- For Windows
  1. In Windows Explorer, copy the entire GPi_Case_patch folder to the root directory of your SD card \(which is actually /boot\).
  2. Open the GPi_Case_patch folder and double-click install_patch.bat to execute it.
  3. You're done! To undo this and output to HDMI again, run the uninstall_patch.bat file in that folder \(though I don't know why you'd want to do this\).
- For nix
  1. Mount sdcard /boot partition and navigate to the mounted directory
  2. Back up /boot/config.txt and /boot/overlays/dpi24.dtbo by copying them somewhere safe, like a backup folder.
      ```
      mv /boot/config{,-dist}.txt
      mv /boot/overlays/dpi24{,-dist}.dtbo
      ```
  3. Extract the patch archive and copy its config.txt, overlays/dpi24.dtbo and overlays/pwm-audio-pi-zero.dtbo to the SD card's /boot partiton.
      ```
      cp /tmp/gpi-patch/config.txt /boot/config.txt
      cp /tmp/gpi-patch/overlays/dpi24.dtbo /boot/overlays/
      cp /tmp/gpi-patch/overlays/pwm-audio-pi-zero.dtbo /boot/overlays/
      ```
  4. You're done! To undo this and output to HDMI by default, replace those two files with your backups from earlier.

## Post bootup
### Install the [RetroFlag safe shutdown] script
- Connect to your raspi zero via SSH
- For RetroPie (pi:raspberry):
  1. Press F4 enter terminal.
  2. In the terminal, type the one-line command below:
      ```bash
      wget -O - "https://raw.githubusercontent.com/RetroFlag/retroflag-picase/master/install_gpi.sh" | sudo bash
      # OR
      wget https://raw.githubusercontent.com/RetroFlag/retroflag-picase/master/install_gpi.sh -O install-gpi-safe-shutdown-retro.sh
      sudo bash ./install-gpi-safe-shutdown-retro.sh
      ```
- For Recalbox (root:recalboxroot)
  1. Press F4 first. And then press ALT-F2 enter terminal.
  2. In the terminal, type the one-line command below(Case sensitive):
      ```bash
      wget -O - "https://raw.githubusercontent.com/RetroFlag/retroflag-picase/master/recalbox_install_gpi.sh" | bash
      # OR
      wget https://raw.githubusercontent.com/RetroFlag/retroflag-picase/master/recalbox_install_gpi.sh -O install-gpi-safe-shutdown-recal.sh
      sudo bash ./install-gpi-safe-shutdown-recal.sh
      ```

## Resources
- [RetroFlag manual]
- Retroflag GPi CASE [User's group] Image 4.5.1-v1 final, now available.
  - [Release Notes and Download]
  - [GPiUsers Facebook]
  - [Xboxdrv Scripts, version Gpi3] also now available
  - **Note**: For proper operation of this image, it is necessary to switch your d-pad mode to Axis mode.</br>
    Hold **Start + Left** \(Select + Left on older version\) for about 10 seconds, until the power light flashes purple.
  - 4.5.1-v1.2 has replaced v1.1 and v1. Don't expect there to be any more patches for a long time now, hopefully.
- Gpi pre build images
  - Super Retropie \(retropie 4.4\) \([Link to Super Retropie]\)
  - Supreme Retropie v 1.1 \(based on retropie 4.4\) \([Link to Supreme Retropie]\)
  - Recalbox v6.1 BETA 3 \([Link to Recalbox]\)
  - Gpi user group Image v1 finale \(retropie 4.5.1\) \([Link to Gpi user group Image]\)
  - Lakka image for GPi case \(with RetroArch 1.7.6 or 1.7.8\) \([Link to Lakka Image]\)

## Recommended packages for the anemic rpi0
- Run Retropie installer script > Install Packages
- main
  - SNES: lr-snes9x2002
  - Genesis: lr-picodrive
- opt: optional
  - GBA: gpsp
  - PS1: pcsx-rearmed
  - usbromservice
- exp: experimental retropie-manager
  - Set the service to manual enable/disable mode to conserve resources, check `/etc/rc.local`
  - Redirect logs to tmpfs: `ln -s /tmp /opt/retropie/supplementary/retropie-manager/logs`
  - Start/Stop script: `/opt/retropie/supplementary/retropie-manager/rpmanager.sh`

## Configurations
- Autologin service: `/lib/systemd/system/getty@.service`, `/etc/systemd/system/getty@tty1.service.d/autologin.conf`
- Autostart script : `/etc/profile.d/10-retropie.sh`
- Consider links these locations to a tmpfs either `/tmp` or `/dev/shm` is fine
  - Installer build tempdir: `ln -s /dev/shm RetroPie-Setup/tmp/build`
  - Log: /dev/shm/runcommand.log - will be your game loading
  - Log: /home/pi/.emulationstation/ - will have some Emulationstation logging.
- Disable controller notification: In EmuStation, go to Retropie config menu > Retroarch > settings > onscreen display > Onscreen notifications and turn them off.
- Disable `runcommand` rom boot menu: Run Retropie installer script > Configuration / tools > runcommand > Launch menu

## Controller shortcuts
- Select + Start simultaneously: Quit game
- Select + Right shoulder button: Save state
- Select + Left shoulder button: Load state
- Select + Right or Left D-pad button: Change save state slot
- Select + X: View emulator configuration menu, > change disk
- Select + B: Reset game



[Install Retropie]: https://retropie.org.uk/docs/Manual-Installation/
[Memory Split]: https://retropie.org.uk/docs/Memory-Split/
[emulator wiki home page]: https://retropie.org.uk/docs/Game-Boy-Advance/
[Boot to EmulationStation]: https://retropie.org.uk/docs/FAQ/#how-do-i-boot-to-the-desktop-or-kodi
[FAQ]: https://retropie.org.uk/docs/FAQ/#how-do-i-boot-to-the-desktop-or-kodi
[Overscan]: https://retropie.org.uk/docs/Overscan/
[Guide with images]: https://howchoo.com/gpi/retroflag-gpi-setup#install-retropie
[Retroflag downloads page]: http://download.retroflag.com/
[directly]: http://download.retroflag.com/Products/GPi_Case/GPi_Case_patch.zip
[RetroFlag safe shutdown]: https://github.com/RetroFlag/retroflag-picase
[RetroFlag manual]: http://download.retroflag.com/manual/case/GPi_CASE_Manual.pdf
[User's group]: https://www.reddit.com/r/retroflag_gpi/comments/cwiifp/retroflag_gpi_case_users_group_image_451v1_final/
[Release Notes and Download]: https://drive.google.com/drive/folders/1a4PJI1axHDaKanj2wIbSsvKj3PHbHqL9
[GPiUsers Facebook]: https://www.facebook.com/groups/GPiUsers/
[Xboxdrv Scripts, version Gpi3]: https://github.com/SinisterSpatula/Gpi3
[Link to Super Retropie]: https://drive.google.com/drive/folders/1btBKnAYBHR3iHhWI9gDWG6gnhYmjQjqV?usp=sharing&fbclid=IwAR0RHleoua_jYxC78salgEMe77vHgQooO_nvkG2KX2TeWlo_2n_kR_vmqf4
[Link to Supreme Retropie]: https://drive.google.com/drive/folders/1wc_xd-lWmdZnX6JtM9r7iV7awxqpHG6y
[Link to Recalbox]: https://forum.recalbox.com/topic/18158/gpi-case-recalbox-6-1-beta-3-disponible
[Link to Gpi user group Image]: https://drive.google.com/drive/folders/1a4PJI1axHDaKanj2wIbSsvKj3PHbHqL9
[Link to Lakka Image]: http://le.builds.lakka.tv/RPi.GPICase.arm/Lakka-RPi.GPICase.arm-2.3.1.img.gz
[Runcommand]: https://retropie.org.uk/docs/Runcommand/
