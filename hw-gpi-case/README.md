## FUC
```bash
rsync -rlvH --checksum --include-from=./rsync-include.txt --max-size=5m pi@192.168.11.65:~/RetroPie-Data/ ~/RetroPie-Data/
rsync -rlvH --checksum --include-from=./rsync-include.txt --max-size=5m ~/RetroPie-Data/ pi@192.168.11.65:~/RetroPie-Data/

rsync -rlvH --checksum --include-from=./rsync-include.txt --max-size=5m alt@192.168.11.66:~/RetroPie-Data/ ~/RetroPie-Data/
rsync -rlvH --checksum --include-from=./rsync-include.txt --max-size=5m ~/RetroPie-Data/ alt@192.168.11.66:~/RetroPie-Data/
```

## Ansible
```bash
ansible-playbook -i gpi-hosts.yml playbook-push.yml
ansible-playbook -i gpi-hosts.yml --user pi --ask-pass playbook-push.yml
```

## Sync save file
```bash
ssh pi@192.168.11.65
export gpihome='~'
ln -s ${gpihome}/RetroPie-Data/roms ${gpihome}/RetroPie/roms
ln -s ${gpihome}/RetroPie-Data/BIOS ${gpihome}/RetroPie/BIOS
ln -s ${gpihome}/RetroPie-Data/pcsx-memcards /opt/retropie/emulators/pcsx-rearmed/memcards
ln -s ${gpihome}/RetroPie-Data/pcsx-sstates /opt/retropie/configs/psx/pcsx/sstates
for x in $(ls ${gpihome}/RetroPie/BIOS/scph*); do ln -s "$x" /opt/retropie/emulators/pcsx-rearmed/bios/; done
exit
cat << EOT >> ~/RetroPie-Data/retropie-exclude.txt
*roms/*.bin
*roms/*.BIN
*roms/*.cue
*.zip
*.rar
*.7z
*.iso
EOT
cat << EOT >> ~/RetroPie-Data/retropie-include.txt
*.srm
*.sav
*.mcd
*.cht
EOT
--include-from
alias save-push="rsync -rlvH --checksum --exclude-from=~/RetroPie-Data/retropie-exclude.txt --max-size=5m ~/RetroPie-Data/ pi@192.168.11.65:~/RetroPie-Data/"
alias save-pull="rsync -rlvH --checksum --exclude-from=~/RetroPie-Data/retropie-exclude.txt --max-size=5m pi@192.168.11.65:~/RetroPie-Data/ ~/RetroPie-Data/"
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
[sinisterspatula]: https://sinisterspatula.github.io/RetroflagGpiGuides/
