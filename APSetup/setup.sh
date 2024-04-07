#!/usr/bin/env bash

done_message() {
    echo "Done!"
    echo ""
}

# Check if script is being run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

# Variables
phoebus_dir="/etc/phoebus"
phoebus_log_dir="/var/log/phoebus"
dnsmasq_dir="/etc/dnsmasq.d"
hostapd_dir="/etc/hostapd"

# Ask the user indefinitely until they choose a valid option
while true; do
echo "Chose a device."
echo "1) Raspberry Pi"
echo "2) Orange Pi"
echo "3) Exit"
read -p "Enter the number: " pi_type

# Check if the user entered a valid number
if [ "$pi_type" -eq 1 ] || [ "$pi_type" -eq 2 ] || [ "$pi_type" -eq 3 ]; then
    break
else
    echo "Invalid number. Please try again."
fi
done

# update and upgrade
echo "Updating and Upgrading packages..."
sudo apt update && sudo apt upgrade -y
done_message

# Install necessary packages
echo "Installing necessary packages..."
sudo apt install iptables dnsmasq hostapd -y
sudo wget https://github.com/xero/figlet-fonts/blob/0c0697139d6db66878eee720ebf299bc3a605fd0/starwars.flf
done_message

# Make directories for config files
if [ -d "$phoebus_dir" ]; then
    echo "Directory $phoebus_dir already exists."
else
    echo "Creating directories..."
    mkdir /etc/phoebus /etc/iptables /var/log/phoebus
    mkdir /etc/phoebus/data /etc/phoebus/wpa_supplicant
    mkdir /etc/phoebus/data/ap_scan
    done_message
fi

# Copy files to their correct directories
if [ -d "$dnsmasq_dir" ] && [ -d "$hostapd_dir" ]; then

    # Raspberry Pi 
    if [ "$pi_type" -eq 1 ]; then
        
        echo "Copying and moving files..."

        ap_setup_dir=$(pwd)

        cd Files/RaspberryPi/etc
        cp "dnsmasq.conf" "/etc/dnsmasq.conf"
        cp "sysctl.conf" "/etc/sysctl.conf"
        cp "default/hostapd" "/etc/default/hostapd"
        cp "dnsmasq.d/*" "/etc/dnsmasq.d/"
        cp "hostapd/hostapd.conf" "/etc/hostapd/hostapd.conf"
        cp "network/interfaces" "/etc/network/interfaces"

        # Copy the iptables config files
        cp "iptables/*" "/etc/iptables/"

        # Copy the wpa_supplicant templates
        cp "wpa_supplicant/*" "/etc/phoebus/wpa_supplicant/"

        # Copy and edit the MOTD files
        sudo rm /etc/uptade-motd.d/*
        cp "update-motd.d/*" "/etc/update-motd.d/"
        sudo chmod +x /etc/update-motd.d/*
        sudo rm /etc/motd

        # Check what interfaces are available
        interfaces=$(ls /sys/class/net)
        
        # Check if wlan1 is available
        # If wlan1 is available, copy the eth0-lan, wlan0-wan, and wlan1-lan files
        if [[ $interfaces == *"wlan1"* ]]; then
            cp "network/interfaces.d/eth0-lan" "/etc/network/interfaces.d/eth0-lan"
            cp "network/interfaces.d/wlan0-wan" "/etc/network/interfaces.d/wlan0-wan"
            cp "network/interfaces.d/wlan1-lan" "/etc/network/interfaces.d/wlan1-lan"

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/eth0-wlan1.rules
            done_message
        
        # If wlan1 is not available, copy the eth0-lan, wlan0-wan files
        else
            cp "network/interfaces.d/eth0-wan" "/etc/network/interfaces.d/eth0-wan"
            cp "network/interfaces.d/wlan0-lan" "/etc/network/interfaces.d/wlan0-lan"

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/eth0-wlan0.rules
            done_message
        fi

        cd $current_dir
        done_message

    # Orange Pi
    elif [ "$pi_type" -eq 2 ]; then
        
        echo "Copying and moving files..."

        ap_setup_dir=$(pwd)

        cd Files/OrangePi/etc
        cp "dnsmasq.conf" "/etc/dnsmasq.conf"
        cp "sysctl.conf" "/etc/sysctl.conf"
        cp "default/hostapd" "/etc/default/hostapd"
        cp "dnsmasq.d/*" "/etc/dnsmasq.d/"
        cp "hostapd/hostapd.conf" "/etc/hostapd/hostapd.conf"
        cp "network/interfaces" "/etc/network/interfaces"

        # Copy the iptables config files
        cp "iptables/*" "/etc/iptables/"

        # Copy the wpa_supplicant templates
        cp "wpa_supplicant/*" "/etc/phoebus/wpa_supplicant/"

        # Copy and edit the MOTD files
        sudo rm /etc/uptade-motd.d/*
        cp "update-motd.d/*" "/etc/update-motd.d/"
        sudo chmod +x /etc/update-motd.d/*

        # Check what interfaces are available
        interfaces=$(ls /sys/class/net)
        
        # Check if wlx00c0cab3f534 is available
        # If wlx00c0cab3f534 is available, copy the enP3p49s0-lan, enP4p65s0-wan, wlP2p33s0-wan, and wlx00c0cab3f534-lan files
        if [[ $interfaces == *"wlx00c0cab3f534"* ]]; then
            cp "network/interfaces.d/enP3p49s0-lan" "/etc/network/interfaces.d/enP3p49s0-lan"
            cp "network/interfaces.d/enP4p65s0-wan" "/etc/network/interfaces.d/enP4p65s0-wan"
            cp "network/interfaces.d/wlP2p33s0-wan" "/etc/network/interfaces.d/wlP2p33s0-wan"
            cp "network/interfaces.d/wlx00c0cab3f534-wan" "/etc/network/interfaces.d/wlx00c0cab3f534-wan"

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/enP4p65s0-wlx00c0cab3f534.rules
            done_message
        
        # If wlx00c0cab3f534 is not available, copy the enP3p49s0-lan, wlP2p33s0-wan files
        else
            cp "network/interfaces.d/enP3p49s0-lan" "/etc/network/interfaces.d/enP3p49s0-lan"
            cp "network/interfaces.d/enP4p65s0-wan" "/etc/network/interfaces.d/enP4p65s0-wan"
            cp "network/interfaces.d/wlP2p33s0-lan" "/etc/network/interfaces.d/wlP2p33s0-lan"

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/enP4p65s0-wlP2p33s0.rules
            done_message
        fi

        cd $current_dir
        done_message
    fi

else
    echo "Required directories do not exist! Exiting..."
    exit 1
fi

# Unmask hostapd service
echo "Unmasking and starting hostapd..."
sudo systemctl unmask hostapd
done_message

# Reboot the Pi
echo "Rebooting..."
sudo reboot