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
dirs=("/etc/phoebus" "/etc/iptables" "/var/log/phoebus" "/etc/phoebus/data" "/etc/phoebus/tools" "/etc/phoebus/wpa_supplicant" "/etc/phoebus/data/ap_scan" "/etc/phoebus/data/connected_clients" "/etc/phoebus/data/interfaces")

# Ask the user indefinitely until they choose a valid option
while true; do
echo "Chose a device."
echo "1) Raspberry Pi"
echo "2) Orange Pi"
echo "3) Exit"
read -p "Enter the number: " pi_type

# Check if the user entered a valid number
if [ "$pi_type" -eq 1 ] || [ "$pi_type" -eq 2 ]; then
    break
elif [ "$pi_type" -eq 3 ]; then
    exit 0
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
sudo apt install iptables dnsmasq hostapd python3-pip vnstat nginx php-fpm -y
if [ "$pi_type" -eq 1 ]; then
    sudo apt install toilet figlet -y
elif [ "$pi_type" -eq 2 ]; then
    sudo apt install net-tools -y
fi

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx

sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old
sudo pip3 install maskpass influxdb-client numpy scikit-learn pandas
done_message

# Make directories for config files
echo "Creating directories..."
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "Directory $dir already exists."
    else
        mkdir $dir
    fi
done
touch /etc/phoebus/data/ap_scan/scan_results.txt
done_message

# Copy files to their correct directories
if [ -d "$dnsmasq_dir" ] && [ -d "$hostapd_dir" ]; then

    # Raspberry Pi
    if [ "$pi_type" -eq 1 ]; then
        
        echo "Copying and moving files..."

        ap_setup_dir=$(pwd)

        # Copy the scripts to the tools directory
        echo "Installing scripts..."
        cp Scripts/AccessPoint/*.py /etc/phoebus/tools/
        cp Scripts/ConnectedClients/*.py /etc/phoebus/tools/
        cp Scripts/InterfaceData/*.py /etc/phoebus/tools/

        echo "Installing configuration files..."
        cd Files/RaspberryPi/etc
        cp "dnsmasq.conf" "/etc/dnsmasq.conf"
        cp "sysctl.conf" "/etc/sysctl.conf"
        cp "default/hostapd" "/etc/default/hostapd"
        cp dnsmasq.d/* /etc/dnsmasq.d/
        cp "network/interfaces" "/etc/network/interfaces"
        done_message

        # Copy the iptables config files
        echo "Installing iptables configuration files..."
        cp iptables/* /etc/iptables/
        done_message

        # Copy the wpa_supplicant templates
        echo "Installing wpa_supplicant templates..."
        cp wpa_supplicant/* /etc/phoebus/wpa_supplicant/
        done_message

        # Copy and edit the MOTD files
        echo "Installing MOTD files..."
        sudo rm /etc/update-motd.d/*
        cp update-motd.d/* /etc/update-motd.d/
        sudo chmod +x /etc/update-motd.d/*
        if [ -f "/etc/motd" ]; then
            sudo rm /etc/motd
        fi
        done_message

        # Check what interfaces are available
        interfaces=$(ls /sys/class/net)
        
        # Check if wlan1 is available
        # If wlan1 is available, copy the eth0-lan, wlan0-wan, and wlan1-lan files
        if [[ $interfaces == *"wlan1"* ]]; then
            echo "Installing configuration files for wlan1..."
            cp "hostapd/hostapd-wlan1.conf" "/etc/hostapd/hostapd.conf"
            cp "network/interfaces.d/eth0-lan" "/etc/network/interfaces.d/eth0"
            cp "network/interfaces.d/wlan0-wan" "/etc/network/interfaces.d/wlan0"
            cp "network/interfaces.d/wlan1-lan" "/etc/network/interfaces.d/wlan1"
            done_message

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/eth0-wlan1.rules
            done_message
        
        # If wlan1 is not available, copy the eth0-lan, wlan0-wan files
        else
            echo "Installing configuration files for wlan0..."
            cp "hostapd/hostapd-wlan0.conf" "/etc/hostapd/hostapd.conf"
            cp "network/interfaces.d/eth0-wan" "/etc/network/interfaces.d/eth0"
            cp "network/interfaces.d/wlan0-lan" "/etc/network/interfaces.d/wlan0"
            done_message

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/eth0-wlan0.rules
            done_message
        fi

        cd $current_dir

        echo "Installing Web Interface..."
        sudo mv ../WebInterface/php.ini /etc/php/8.2/fpm/php.ini
        sudo mv ../WebInterface/default /etc/nginx/sites-available/default
        sudo cp -r ../WebInterface/* /var/www/html/
        sudo rm /var/www/html/index.nginx-debian.html
        sudo systemctl restart nginx
        done_message

        echo "Installing cron jobs..."


    # Orange Pi
    elif [ "$pi_type" -eq 2 ]; then
        
        echo "Copying and moving files..."

        ap_setup_dir=$(pwd)

        echo "Installing configuration files..."
        cd Files/OrangePi/etc
        cp "dnsmasq.conf" "/etc/dnsmasq.conf"
        cp "sysctl.conf" "/etc/sysctl.conf"
        cp "default/hostapd" "/etc/default/hostapd"
        cp dnsmasq.d/* /etc/dnsmasq.d/
        cp "network/interfaces" "/etc/network/interfaces"
        done_message

        # Copy the iptables config files
        echo "Installing iptables configuration files..."
        cp iptables/* /etc/iptables/
        done_message

        # Copy the wpa_supplicant templates
        echo "Installing wpa_supplicant templates..."
        cp wpa_supplicant/* /etc/phoebus/wpa_supplicant/
        done_message

        # Copy and edit the MOTD files
        echo "Installing MOTD files..."
        sudo rm /etc/update-motd.d/*
        cp update-motd.d/* /etc/update-motd.d/
        sudo chmod +x /etc/update-motd.d/*
        if [ -f "/etc/motd" ]; then
            sudo rm /etc/motd
        fi
        done_message

        # Check what interfaces are available
        interfaces=$(ls /sys/class/net)
        
        # Check if wlx00c0cab3f534 is available
        # If wlx00c0cab3f534 is available, copy the enP3p49s0-lan, enP4p65s0-wan, wlP2p33s0-wan, and wlx00c0cab3f534-lan files
        if [[ $interfaces == *"wlx00c0cab3f534"* ]]; then
            echo "Installing configuration files for wlx00c0cab3f534 interface..."
            cp "hostapd/hostapd-wlx00c0cab3f534.conf" "/etc/hostapd/hostapd.conf"
            cp "network/interfaces.d/enP3p49s0-lan" "/etc/network/interfaces.d/enP3p49s0"
            cp "network/interfaces.d/enP4p65s0-wan" "/etc/network/interfaces.d/enP4p65s0"
            cp "network/interfaces.d/wlP2p33s0-wan" "/etc/network/interfaces.d/wlP2p33s0"
            cp "network/interfaces.d/wlx00c0cab3f534-wan" "/etc/network/interfaces.d/wlx00c0cab3f534"
            done_message

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/enP4p65s0-wlx00c0cab3f534.rules
            done_message
        
        # If wlx00c0cab3f534 is not available, copy the enP3p49s0-lan, wlP2p33s0-wan files
        else
            echo "Installing configuration files for wlP2p33s0 interface..."
            cp "hostapd/hostapd-wlP2p33s0.conf" "/etc/hostapd/hostapd.conf"
            cp "network/interfaces.d/enP3p49s0-lan" "/etc/network/interfaces.d/enP3p49s0"
            cp "network/interfaces.d/enP4p65s0-wan" "/etc/network/interfaces.d/enP4p65s0"
            cp "network/interfaces.d/wlP2p33s0-lan" "/etc/network/interfaces.d/wlP2p33s0"
            done_message

            # Restore firewall rules
            echo "Restoring firewall rules..."
            sudo iptables-restore < /etc/iptables/enP4p65s0-wlP2p33s0.rules
            done_message
        fi

        cd $current_dir
    fi

else
    echo "Required directories do not exist! Exiting..."
    exit 1
fi

chmod -R 777 /etc/phoebus

# Unmask hostapd service
echo "Unmasking and starting hostapd..."
sudo systemctl unmask hostapd
done_message

# Reboot the Pi
echo "Rebooting..."
sudo reboot
