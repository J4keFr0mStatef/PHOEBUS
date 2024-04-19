#!/bin/bash

interfaces=$(ls /sys/class/net)

# Loop through all interfaces
for interface in $interfaces; do
    if [[ "$interface" == "lo" ]]; then
        continue
    
    elif [[ -n "$interface" ]] && vnstat -i "$interface" &> /dev/null; then
        
        traffic=$(vnstat -i $PRIMARY_INTERFACE --oneline | cut -d";" -f4,5)
        traffic_rx=$(echo $traffic | cut -d";" -f1,1 | sed -r 's/([0-9]+\.[0-9]{1})[0-9]*/\1/')
        traffic_tx=$(echo $traffic | cut -d";" -f2,2 | sed -r 's/([0-9]+\.[0-9]{1})[0-9]*/\1/')

        echo "Interface: $interface"
        echo "Incoming Traffic: $traffic_rx     Outgoing Traffic: $traffic_tx"
        echo " "