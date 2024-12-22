#!/usr/bin/env python

import os
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidgetAction
from PyQt6.QtGui import QIcon
from pathlib import Path

check_version_cmd = 'pacman -Qi ideapad2024-power-management | grep "Version"'
VERSION_CHECK= subprocess.run(check_version_cmd, shell=True, capture_output=True)
# decode stdout
VERSION_CHECK = VERSION_CHECK.stdout.decode("utf-8")

def get_current_power_status():
    command = "/usr/bin/env ideapad2024-power-manage -c"
    output = subprocess.run(command, shell=True, capture_output=True)
    # decode stdout
    output = output.stdout.decode("utf-8")
    # also get battery percentage
    battery_info_command = "cat /sys/class/power_supply/BAT0/uevent"
    battery_info_output = subprocess.run(battery_info_command, shell=True, capture_output=True)
    battery_info_output = battery_info_output.stdout.decode("utf-8",errors='ignore')
    battery_percentage = None
    full_capacity = None
    for line in battery_info_output.split("\n"):
        if "POWER_SUPPLY_ENERGY_NOW" in line:
            battery_percentage = line.split("=")[1]
        if "POWER_SUPPLY_ENERGY_FULL" in line:
            full_capacity = line.split("=")[1]
        if battery_percentage and full_capacity:
            break
    if battery_percentage and full_capacity:
        battery_percentage = int(battery_percentage) / int(full_capacity) * 100
        output += f"Battery Percentage: {battery_percentage:.2f}%"
    # add version
    output += "\n" + VERSION_CHECK
    
    return output
        
def tray_showmessage(tray, message):
    tray.showMessage("Power Status", message, QSystemTrayIcon.MessageIcon.Information, 3000)
    
    
def set_battery_normal():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --battery-mode normal"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)

def set_battery_conserve():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --battery-mode conserve"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)

def set_battery_rapid():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --battery-mode rapid"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)

def set_performance_performance():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --performance-mode performance"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)

def set_performance_extreme():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --performance-mode extreme"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)

def set_performance_powersave():
    global tray
    command = "/usr/bin/env ideapad2024-power-manage --performance-mode powersave"
    subprocess.run(command, shell=True)
    result = get_current_power_status()
    tray_showmessage(tray, result)


    
def update_traytip_content():
    global status_action
    status = get_current_power_status()
    status_action.setText(status.strip())

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # create the tray icon
    if os.path.exists('/usr/share/ideapad2024-power-management/power_management.png'):
        icon_fp = '/usr/share/ideapad2024-power-management/power_management.png'
    elif os.path.exists(os.path.join(Path(__file__).parent.resolve(), 'power_management.png')):
        icon_fp = os.path.join(Path(__file__).parent.resolve(), 'power_management.png')
    else:
        icon_fp = None
    if icon_fp:
        icon = QIcon(icon_fp)
    
    # Create the tray 
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.setToolTip("Power Options")
    
    
    # Create the menu
    menu = QMenu()
    # text status action
    status_action = QWidgetAction(menu)
    status_action.setText("Power Status")
    status_action.setEnabled(False)
    
    
    
    # Create the actions
    performance_performance_action = QWidgetAction(menu)
    performance_performance_action.setText("Performance - Performance")
    performance_performance_action.triggered.connect(set_performance_performance)
    
    performance_extreme_action = QWidgetAction(menu)
    performance_extreme_action.setText("Performance - Extreme")
    performance_extreme_action.triggered.connect(set_performance_extreme)
    
    performance_powersave_action = QWidgetAction(menu)
    performance_powersave_action.setText("Performance - Powersave")
    performance_powersave_action.triggered.connect(set_performance_powersave)
    
    battery_save_action = QWidgetAction(menu)
    battery_save_action.setText("Battery - Conserve")
    battery_save_action.triggered.connect(set_battery_conserve)
    
    battery_normal_action = QWidgetAction(menu)
    battery_normal_action.setText("Battery - Normal")
    battery_normal_action.triggered.connect(set_battery_normal)
    
    battery_rapid_action = QWidgetAction(menu)
    battery_rapid_action.setText("Battery - Rapid")
    battery_rapid_action.triggered.connect(set_battery_rapid)
    
    # Add quit 
    quit_action = QWidgetAction(menu)
    quit_action.setText("Quit")
    quit_action.triggered.connect(app.quit)
    
    
    # menu event will update tooltip
    menu.aboutToShow.connect(update_traytip_content)
    
    # Add the actions to the menu
    menu.addAction(status_action)
    menu.addSeparator()
    menu.addAction(performance_performance_action)
    menu.addAction(performance_extreme_action)
    menu.addAction(performance_powersave_action)
    menu.addSeparator()
    menu.addAction(battery_save_action)
    menu.addAction(battery_normal_action)
    menu.addAction(battery_rapid_action)
    menu.addSeparator()
    menu.addAction(quit_action)
    
    # add the menu to the tray
    tray.setContextMenu(menu)
    
    # set that if click in left button will also show the menu
    def on_click(reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            tray_showmessage(tray, get_current_power_status())
    tray.activated.connect(on_click)
 
    
    sys.exit(app.exec()) # 
    
    
    
    
    
