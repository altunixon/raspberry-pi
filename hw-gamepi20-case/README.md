## cmake Param for patched fbcp-ili9341-patched-gamepi20.zip spi driver
```bash
mkdir -p build && cd build
cmake -DWAVESHARE_GAMEPI20=ON -DSPI_BUS_CLOCK_DIVISOR=6 ..
cmake -DWAVESHARE_GAMEPI20=ON -DSPI_BUS_CLOCK_DIVISOR=6 -DSTATISTICS=0 ..
```
- With `#define ALL_TASKS_SHOULD_DMA` disabled in ../config.h and also disable Statistic line with `-DSTATISTICS=0`
```bash
mkdir -p build && cd build
cmake -DWAVESHARE_GAMEPI20=ON -DSPI_BUS_CLOCK_DIVISOR=6 -DUSE_DMA_TRANSFERS=ON -DSTATISTICS=0 ..
```
Note: un official commit based on juj's [fbcp-ili9341], see [commit diff] for more details.

## Audio overlay [darrenliew96], Video uses [fbcp-ili9341]/[tasanakorn] driver
```bash
cat << EOF >> | sudo tee /boot/config.txt
audio_pwm_mode=2
dtoverlay=audremap,pins_18_19
EOF
```
- `dtoverlay=audremap,pins_18_19` sets the Audio output via the GPIO=18 \(PWM GPIO pin 12 / PWM CLK\)
- `audio_pwm_mode=2` enable "better" PWM output
## Raspbian update breaks gpio audio fix
Add `snd_bcm2835.enable_hdmi=1 snd_bcm2835.enable_headphones=1 snd_bcm2835.enable_compat_alsa=1` to `/boot/cmdline.txt`</br>
This will mimic the old audio which changed in May 2020.</br>
The new audio is more sensible but incompatible with GPIO audio device-tree overlays.
``bash`
echo -n "$(cat cmdline.txt) snd_bcm2835.enable_hdmi=1 snd_bcm2835.enable_headphones=1 snd_bcm2835.enable_compat_alsa=1" > cmdline.txt
```
You could also try retroarch/emulationstation</br>
Configuration -> configedit -> Advanced Configuration -> Configure libretro options -> all/retroarch/retroarch.cfg -> audiodriver.</br>
Make sure it's set to alsathread. There are per-core configs like arcade/retroarch.cfg where you can also set audiodriver to alsathread.

[fbcp-ili9341]: https://github.com/juj/fbcp-ili9341
[commit diff]: https://github.com/juj/fbcp-ili9341/pull/198/files?diff=split&w=0
[darrenliew96]: https://github.com/darrenliew96/gamepi20_drivers
[tasanakorn]: https://github.com/tasanakorn/rpi-fbcp

