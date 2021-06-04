### vcgencmd
```bash
$ vcgencmd measure_clock core
frequency(1)=250000000
$ vcgencmd measure_volts core
volt=1.2000V
$ vcgencmd measure_temp
temp=42.2'C
$ vcgencmd get_throttled
throttled=0x50000
```
Read [return bits value], \(use python2\) convert hex to base0 int, then convert int to binary:
```python
x = int('0x50000', 0)
print (x, "=", bin(x))
print ('{:20b}'.format(bin(x)))
```
### [Python Script](https://harlemsquirrel.github.io/shell/2019/01/05/monitoring-raspberry-pi-power-and-thermal-issues.html)
```python
#!/usr/bin/env python2

import subprocess

GET_THROTTLED_CMD = 'vcgencmd get_throttled'
rpi_message = {
    0 : 'Under-voltage!',
    1 : 'ARM frequency capped!',
    2 : 'Currently throttled!',
    3 : 'Soft temperature limit active',
    16: 'Under-voltage has occurred since last reboot.',
    17: 'Throttling has occurred since last reboot.',
    18: 'ARM frequency capped has occurred since last reboot.',
    19: 'Soft temperature limit has occurred'
}

print ("Checking for throttling issues since last reboot...")

vcgencmd_output = subprocess.check_output(GET_THROTTLED_CMD, shell=True)
vcgencmd_binary = bin(int(throttled_output.split('=', 1)[1], 0)) # perhaps needs left zero padding
# vcgencmd_binary = '{:20b}'.format(bin(int(throttled_output.split('=',1)[1], 0))) # pad left to match 20 character bin array

rpi_warnings = 0
for msg_pos, msg_txt in rpi_message.iteritems():
    # reverse checking since bit is set from right->left thus bit[0] -> bin[-1] == bin [19]
    # bit:  0 1 2 3  4 5 6 7  8 9 1011 12131415 16171819
    # bin: 19181716 15141312 1110 9 8  7 6 5 4  3 2 1 0
    if len(vcgencmd_binary) > msg_pos and vcgencmd_binary[0 - msg_pos - 1] == '1': # bit iffy?, might not work with bit[19] (bin[-20])
        print ('bit [{0}] is active: {1}'.format(msg_pos, msg_txt))
        rpi_warnings += 1

if rpi_warnings == 0:
    print("Looking good!")
else:
    print("Houston, we may have a problem!")
```



[return bits value]: https://github.com/raspberrypi/documentation/blob/master/raspbian/applications/vcgencmd.md#get_throttled
