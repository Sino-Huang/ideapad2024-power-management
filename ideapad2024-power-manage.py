#!/usr/bin/env python 
import argparse
import subprocess
import re

# check https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_15are05#Rapid_Charge

def check_battery_status():
    # rapid charge status 
    command = """echo '\_SB.PCI0.LPC0.EC0.QCHO' > /proc/acpi/call
    cat /proc/acpi/call; printf '\n'
    """
    
    result = subprocess.run(command, shell=True, capture_output=True)
    result = result.stdout.decode("utf-8").strip().rstrip('\x00')
    rapid_charge_state = None 
    if result == "0x0":
        rapid_charge_state = False 
    elif result == "0x1":
        rapid_charge_state = True
    else:
        raise Exception("Error getting rapid charge state")
    
    # battery conservation status
    command = """echo '\_SB.PCI0.LPC0.EC0.BTSM' > /proc/acpi/call
    cat /proc/acpi/call; printf '\n'
    """
    
    result = subprocess.run(command, shell=True, capture_output=True)
    result = result.stdout.decode("utf-8").strip().rstrip('\x00')
    battery_conservation_state = None
    if result == "0x0":
        battery_conservation_state = False
    elif result == "0x1":
        battery_conservation_state = True
    else:
        raise Exception("Error getting battery conservation state")
    
    if rapid_charge_state and battery_conservation_state:
        return "WARNING: Both rapid charge and battery conservation are enabled"
    elif rapid_charge_state and not battery_conservation_state:
        return "Rapid"
    elif not rapid_charge_state and battery_conservation_state:
        return "Conserve"
    else:
        return "Normal"
    
def check_performance_status():
    # performance mode from acpi_call
    command = """echo '\_SB.PCI0.LPC0.EC0.SPMO' > /proc/acpi/call
    cat /proc/acpi/call; printf '\n'
    """
    result = subprocess.run(command, shell=True, capture_output=True)
    result = result.stdout.decode("utf-8").strip().rstrip('\x00')
    performance_mode = None
    if result == "0x0":
        performance_mode = "Performance"
    elif result == "0x1":
        performance_mode = "Extreme"
    elif result == "0x2":
        performance_mode = "Powersave"
    else:
        raise Exception("Error getting performance mode")
    
    # also check cpupower status 
    # the information is 'current policy' and the following 1 line 
    command = "/usr/bin/cpupower frequency-info | grep -A1 'current policy'"
    result = subprocess.run(command, shell=True, capture_output=True)
    result = result.stdout.decode("utf-8")
    # check The governor
    governor = re.search(r'''The governor\s['"](\w+)['"]''', result).group(1)
    return f"{performance_mode}, CPU governor: {governor}"

TURN_OFF_RAPID_CHARGE_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x08' > /proc/acpi/call"
TURN_ON_RAPID_CHARGE_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x07' > /proc/acpi/call"
TURN_OFF_BATTERY_CONSERVATION_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x05' > /proc/acpi/call"
TURN_ON_BATTERY_CONSERVATION_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x03' > /proc/acpi/call"

POWER_PERFORMANCE_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x000FB001' > /proc/acpi/call"
POWER_EXTREME_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x0012B001' > /proc/acpi/call"
POWER_POWERSAVE_COMMAND = "echo '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x0013B001' > /proc/acpi/call"

def set_battery_normal():
    # turn off rapid charge 
    command = TURN_OFF_RAPID_CHARGE_COMMAND
    subprocess.run(command, shell=True)
    
    # turn off battery conservation
    command = TURN_OFF_BATTERY_CONSERVATION_COMMAND
    subprocess.run(command, shell=True)
    
def set_battery_conserve():
    # turn off rapid charge
    command = TURN_OFF_RAPID_CHARGE_COMMAND
    subprocess.run(command, shell=True)
    # turn on battery conservation
    command = TURN_ON_BATTERY_CONSERVATION_COMMAND
    subprocess.run(command, shell=True)
    
def set_battery_rapid():
    # turn off battery conservation
    command = TURN_OFF_BATTERY_CONSERVATION_COMMAND
    subprocess.run(command, shell=True)
    # turn on rapid charge
    command = TURN_ON_RAPID_CHARGE_COMMAND
    subprocess.run(command, shell=True)

def set_performance_performance():
    command = POWER_PERFORMANCE_COMMAND
    subprocess.run(command, shell=True)
    # also set cpupower governor to performance
    command = "sudo /usr/bin/cpupower frequency-set -g performance"
    subprocess.run(command, shell=True)
    
def set_performance_extreme():
    command = POWER_EXTREME_COMMAND
    subprocess.run(command, shell=True)
    # also set cpupower governor to performance
    command = "sudo /usr/bin/cpupower frequency-set -g performance"
    subprocess.run(command, shell=True)
    
def set_performance_powersave():
    command = POWER_POWERSAVE_COMMAND
    subprocess.run(command, shell=True)
    # also set cpupower governor to powersave
    command = "sudo /usr/bin/cpupower frequency-set -g powersave"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Power management for Lenovo Ideapad 2024')
    parser.add_argument('-c', '--check', help='Check the current power status', action='store_true', default=False)
    parser.add_argument('-b', '--battery-mode', help='Set the battery mode', choices=['conserve', 'normal', 'rapid'], type=str)
    parser.add_argument('-p', '--performance-mode', help='Set the performance mode', choices=['performance', 'extreme', 'powersave'], type=str)
    
    args = parser.parse_args()
    
    if args.check:
        battery_mode = check_battery_status()
        print(f"Battery Mode: {battery_mode}")
        performance_mode = check_performance_status()
        print(f"Performance Mode: {performance_mode}")
        
    wanted_battery_mode = args.battery_mode
    wanted_performance_mode = args.performance_mode
    
    if wanted_battery_mode == "conserve":
        set_battery_conserve()
    elif wanted_battery_mode == "normal":
        set_battery_normal()
    elif wanted_battery_mode == "rapid":
        set_battery_rapid()
        
    if wanted_performance_mode == "performance":
        set_performance_performance()
    elif wanted_performance_mode == "extreme":
        set_performance_extreme()
    elif wanted_performance_mode == "powersave":
        set_performance_powersave()
        
    if wanted_battery_mode or wanted_performance_mode:
        print("Settings applied...")
        battery_mode = check_battery_status()
        print(f"Battery Mode: {battery_mode}")
        performance_mode = check_performance_status()
        print(f"Performance Mode: {performance_mode}")
        
