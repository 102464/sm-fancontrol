## Disclaimer: This software may not be reliable, as it does not contain many exception checks. I am not responsible for any possible software or hardware damage caused by the program, please use it at your own risk.

# sm-fancontrol

## Description
Automated fan control for Supermicro X11 series motherboards. The program will adjust the fan speed according the CPU and GPU temperature. Only tested on X11SCA-F.

## Requirements
There are some requirements for the program:
1. Your motherboard must be manufactured by Supermicro, and it should have IPMI.
2. Your operating system must be Linux-based.
3. You must use NVIDIA GPU on your motherboard, and the official driver must be installed, the script only supports NVIDIA GPU.
4. Python 3.x and ipmitool must be installed on your device.

## Installation
The installation is very simple:
1. git clone this repository.
```
git clone https://github.com/102464/sm-fancontrol
cd sm-fancontrol
```
2. copy the script to /usr/local/bin, and set permissions.
```
sudo cp sm_fancontrol.py /usr/local/bin
sudo chmod +x /usr/local/bin/sm_fancontrol.py
```
3. (optional) copy the service configuration. This allows you to use sm-fancontrol as a systemd service.
```
sudo cp sm-fancontrol.service /etc/systemd/system
sudo systemctl daemon-reload
```

## Usage
The script does not have extra arguments. Just run it to test if it is working correctly.
```
sm_fancontrol.py
```

Then your fans should be at full speed for 3 seconds, then slow down. Then the fans will adjust the speed according to the temperature. Press Control+C to stop the script.<br>

If you want to start the program on boot, please copy the service configuration and then run:
```
sudo systemctl enable sm-fancontrol.service
```

## Support
If the program has some bugs, please send me an issue or pull request.