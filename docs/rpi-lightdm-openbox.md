### Sources
Rpi Forum: [Raspbian Lite with RPD/LXDE/XFCE/MATE/i3/Openbox/X11 GUI](https://www.raspberrypi.org/forums/viewtopic.php?t=133691) </br>
Debian: [Openbox](https://wiki.debian.org/Openbox#From_a_graphical_login_manager) </br>

### Update packages
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get clean
sudo reboot
```

### Install Display server and DE
#### 1. Xorg Display Server
- Install Xorg, and optionally xinit to start xserver from cmdline (handy for vnc)
  ```bash
  sudo apt-get install --no-install-recommends xserver-xorg
  sudo apt-get install --no-install-recommends xinit
  ```
- With xinit installed, setup a **~/.xsession** file in your home directory and add the following line to it to make Openbox the default session type:
  ```bash
  exec openbox-session
  ```
- Create a **~/.xinitrc** in your home directory with the same content to start openbox session from cmdline with **startx**
- Alternatively there is the possibility to use the Debian alternatives (see [update-alternatives]) and setup x-window-manager to be Openbox. 
#### 2. Raspberry Pi Desktop (RPD) or Lightweight X11 Desktop Environment (LXDE) or XFCE Desktop Environment (XFCE) or MATE Desktop Environment (MATE)
- This part is optional??? but try this if all else failed
- Install LXDE
  ```bash
  sudo apt-get install lxde-core lxappearance
  ```
- By default, Openbox Window Manager is installed when you install **lxde-core**. </br>
  You do not need to do anything here. </br>
  You can customize the look of the titlebar using the Openbox settings which is also installed by default. </br>
  By using LXAppearance and Openbox settings together, you chose what LXDE looks like!
#### 3. Openbox Window Manager (RPD/LXDE) or XFWM Window Manager (XFCE) or Marco Window Manager (MATE)
- Install Openbox WM, and optially feh to use wallpaper
  ```bash
  sudo apt-get install --no-install-recommends openbox obmenu obconf
  sudo apt-get install --no-install-recommends feh
  ```
- Nifty rando wallpaper script:
  ```bash
  #!/usr/bin/env bash
  WALLPAPERS="$HOME/Wallpapers"
  desktop_bg=$(ls -1 "${WALLPAPERS%/}"/*.{jpg,jpeg,png} | shuf | head -n 1) && exec feh --bg-scale "$desktop_bg"
  ```
- Openbox config, System-wide: 
  ```bash
  /etc/xdg/openbox/rc.xml
  /etc/xdg/openbox/menu.xml
  /etc/xdg/openbox/environment
  /etc/xdg/openbox/autostart 
  ```
- User-specific: 
  ```bash
  ~/.config/openbox/rc.xml
  ~/.config/openbox/menu.xml
  ~/.config/openbox/environment
  ~/.config/openbox/autostart 
  ```
- Kb shortcuts (abbr, most commonly used): </br>
  **Alt-F4**: Close the active window </br>
  **Alt-Space**: Show the client menu for the active window </br>
  **Alt-Tab**: Cycle between windows on the desktop </br>
  **Alt-Shift-Tab**: Cycle between windows on the desktop in reverse order </br>
  **Control-Alt-Tab**: Cycle between panel and desktop windows on the desktop </br>
  **Windows-D**: Hide all windows to show the desktop </br>
  **Windows-E**: Run the Konqueror file manager (This is an example of how to run a program with a key binding) </br>
  **Alt-Escape**: Lower the active window behind other windows, and activate the last window that was in use </br>
  **Windows-F{1..4}**: Go to the first desktop instantly </br>
  ...
#### 4. LightDM Login Manager
- Install LightDM
  ```bash
  sudo apt-get install lightdm
  ```
- Resolution fixes (not rpi specific)
  - Query attached display info
    ```bash
    xrandr -q
    ```
  - Use xrandr or the Displays control utility to configure your monitors how you'd like them to be configured in the login screen
    ```bash
    xrandr --output HDMI-0 --mode 1920x1080
    ```
    maybe also add this line to the top of **~/.xsession** file.
  - Copy **'~/.config/monitors.xml'** to **'/var/lib/lightdm/.config/'**
  - OR edit lightdm config file **'/etc/lightdm/lightdm.conf'**:
    ```bash
    # edit or add line (un tested)
    display-setup-script=xrandr --output default --mode 1920x1080
    ```
### Rpi4 [HDMI settings]
#### Using boot config file: **'/boot/config.txt'**
```bash
# Boot with maximum HDMI compatibility
hdmi_safe=1
# Normal HDMI mode (sound will be sent if supported and enabled)
hdmi_drive=2
# HDMI output group to be either [1]=CEA(TVs), [2]=DMT(Monitors) or [0]=Auto-detect(EDID)
hdmi_group=2
# Depends on hdmi_group, should either be [16]=1080p60Hz(16:9) for hdmi_group 1(CEA) or [82]=1080p60Hz(16:9) for hdmi_group 2(DMT)
# see https://www.raspberrypi.org/documentation/configuration/config-txt/video.md for details
hdmi_mode=82
# Setting to 1 will remove all other modes except the ones specified by hdmi_mode and hdmi_group from the internal list
hdmi_force_mode=0
# Remove pesky black borders
disable_overscan=1
```
#### Which values are valid for my monitor?
Your HDMI monitor may only support a limited set of formats. </br>
To find out which formats are supported, use the following method:
- Set the output format to safe value **VGA (640x480) 60Hz 4:3** (hdmi_group=1 and hdmi_mode=1) and boot up your Raspberry Pi
- Enter the following command to give a list of CEA-supported modes: 
  ```bash
  /opt/vc/bin/tvservice -m CEA
  ```
- Enter the following command to give a list of DMT-supported modes: 
  ```bash
  /opt/vc/bin/tvservice -m DMT
  ```
- Enter the following command to show your current state: 
  ```bash
  /opt/vc/bin/tvservice -s
  ```
- Enter the following commands to dump more detailed information from your monitor: 
  ```bash
  /opt/vc/bin/tvservice -d edid.dat
  /opt/vc/bin/edidparser edid.dat
  ```
The edid.dat should also be provided when troubleshooting problems with the default HDMI mode.

[update-alternatives]: https://wiki.debian.org/update-alternatives
[HDMI settings]: https://www.raspberrypi.org/documentation/configuration/config-txt/video.md
