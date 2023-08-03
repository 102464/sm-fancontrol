#!/usr/bin/env python3
import os
import time
import subprocess
import re

cputemp = re.compile(r'^CPU\sTemp.*\|\s([0-9][0-9])\sdegrees\sC$', re.MULTILINE)

def get_nvidia_gpu_temp():
    return int(os.popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader | tail -n 1").read())

def get_cpu_temp():
    try:
        temp = subprocess.check_output(['ipmitool','sdr','type','Temperature']).decode('utf-8')
        temp = re.search(cputemp, temp)
        temp = temp.group(1)
        return int(temp)
    except Exception as e:
        print('cpu temp detection failure!')

def gpu_fan_curve(temp):
    if temp < 40:
        return 20
    elif temp >= 40 and temp < 60:
        return 4 * temp - 140
    elif temp >= 60:
        return 100
    
def cpu_fan_curve(temp):
    if temp < 50:
        return 20
    elif temp >= 50 and temp < 90:
        return 2 * temp - 80
    elif temp >= 90:
        return 100

def set_fan_mode_full_speed():
    cmd = "ipmitool raw 0x30 0x45 0x01 0x01"
    print("Setting fan mode to full speed using ipmitool")
    print("command: " + cmd)
    print(os.popen(cmd).read())
    
def set_fan_mode_standard_speed():
    cmd = "ipmitool raw 0x30 0x45 0x01 0x00"
    print("Setting fan mode to standard speed using ipmitool")
    print("command: " + cmd)
    print(os.popen(cmd).read())

def gpu_fan_set_ratio(ratio):
    cmd = "ipmitool raw 0x30 0x70 0x66 0x01 0x01 " + hex(ratio)
    print("Setting gpu fan speed ratio to " + str(ratio) + "% using ipmitool")
    print("command: " + cmd)
    print(os.popen(cmd).read())

def cpu_fan_set_ratio(ratio):
    cmd = "ipmitool raw 0x30 0x70 0x66 0x01 0x00 " + hex(ratio)
    print("Setting cpu fan speed ratio to " + str(ratio) + "% using ipmitool")
    print("command: " + cmd)
    print(os.popen(cmd).read())


print("Fan control initalizing... Setting all fan to full speed for 3 seconds...")
set_fan_mode_full_speed()
time.sleep(3)
while(1):
    gpu_temp = get_nvidia_gpu_temp()
    cpu_temp = get_cpu_temp()
    gpu_fan_ratio = gpu_fan_curve(gpu_temp)
    cpu_fan_ratio = cpu_fan_curve(cpu_temp)
    print("Current GPU temp: " + str(gpu_temp) + "C")
    print("Current CPU temp: " + str(cpu_temp) + "C")
    print("Set fan speed START")
    gpu_fan_set_ratio(gpu_fan_ratio)
    cpu_fan_set_ratio(cpu_fan_ratio)
    print("Current GPU fan speed ratio: " + str(gpu_fan_ratio) + "%")
    print("Current CPU fan speed ratio: " + str(cpu_fan_ratio) + "%")
    print("Set fan speed DONE. Waiting for next cycle (3 seconds)...")
    time.sleep(3)
