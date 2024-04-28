#!/usr/bin/env bash

#output_dir="/etc/phoebus/data/tshark_outputs"
output_dir="./tshark_outputs"
dumpfile="trafficdump.pcap"
num_packets="150" # amount of packet to cap at a time
interface="any"

common_bad_ports=("1080" "3389" "4444" "6660" "6661" "6662" "6663" "6664" "6665" "6666" "6667" "6668" "6669" "8080" "8443" "31337")

# make necesary file structure for data storage
if [ ! -d "$output_dir" ]; then
    mkdir $output_dir
fi
if test -f "$output_dir/$dumpfile"; then
    echo "file exists ... will overwrite"
else
    echo "creating $output_dir/$dumpfile"
    touch $output_dir/$dumpfile
    chmod o+w $output_dir/$dumpfile
fi

# run tshark to capture num_packets amount of packets 
sudo tshark -i $interface -w $output_dir/$dumpfile -c $num_packets

# check for strange http user agents
echo "---- strange user agents: ----"
tshark -r $output_dir/$dumpfile -T fields -e http.user_agent | sort -u > $output_dir/useragentCheck.txt

# check if file is empty
if [ ! -s "$output_dir/useragentCheck.txt" ]; then
    echo "NO STRANGE USER AGENTS FOUND"
else
    cat $output_dir/useragentCheck.txt
fi
echo "---- end strange user agents. ----"

#general analytics
echo "---- general analytics: ----"
tshark -r $output_dir/$dumpfile -z endpoints,tcp -q > $output_dir/tcp_endpoint_analytics.txt
cat $output_dir/tcp_endpoint_analytics.txt

# strip tcp endpoint analytics to their values
echo "stripping tcp endpoint analytics:
dst_ip, dst_port, packet_count, Tx, Rx"
tail -n +5 $output_dir/tcp_endpoint_analytics.txt > $output_dir/temp.txt
awk '{print $1,$2,$3,$5,$7}' $output_dir/temp.txt > $output_dir/stripped_tcp_endpoint_analytics.txt
rm $output_dir/temp.txt
cat $output_dir/stripped_tcp_endpoint_analytics.txt

# TODO: put resolved hostnames next to the IP in stripped_tcp_endpoint_analytics

echo "---- end general analytics ----"

# port scanner
# Use netstat to get a list of all open ports
echo "---- begin looking for open ports ----"
open_ports=$(netstat -tle | awk '{print $4,$7}')
echo "open ports:
$open_ports"
# add ports to text file
echo "$open_ports" | tail +3 > $output_dir/open_ports.txt

# only get port numbers from open_ports.txt
ports=$(awk '{print $1}' $output_dir/open_ports.txt | grep -oE '[0-9]+' | sort -u)
echo $ports
touch $output_dir/bad_ports.txt
# Iterate over the open ports
for open_port in $ports; do
    # Check if the open port is in the list of known ports
    for known_port in "${common_bad_ports[@]}"; do
        if [[ $open_port == $bad_port ]]; then
            echo "Port $open_port is open and is potentially dangerous."
            echo "$open_port" >> $output_dir/bad_ports.txt
        fi
    done
done

# call on python script to wrap open_ports.txt into JSON
echo "---- end looking for open ports ----"

# use nslookup to get the IP address of the domain
echo "---- begin host resolutions ----"

# Get all the unique IP addresses in the dump file
tshark -r $output_dir/$dumpfile -T fields -e ip.dst | sort -u > $output_dir/ip_dst.txt

# Perform nslookup for each IP address in ip_dst.txt
# echo "" > $output_dir/ip_dst_nslookup.txt # clear file
# while read -r ip_address; do
#     hostname=$(nslookup $ip_address | awk '/name =/{print $4}')
#     echo "$ip_address, $hostname" >> $output_dir/ip_dst_nslookup.txt # append: ip, hostname
# done < $output_dir/ip_dst.txt
sudo tshark -r $output_dir/$dumpfile -z hosts -q | sort -u | tail +3 > $output_dir/hosts.txt

cat $output_dir/hosts.txt
echo "---- end host resolutions ----"

echo "---- begin Usage data ----"
sudo tshark -r $output_dir/$dumpfile -z ip_hosts,tree -q | tail +7 | awk '{print $1,$2,$4}' | head -n -2 > $output_dir/usage_data.txt
cat $output_dir/usage_data.txt
echo "---- end Usage data ----"
# echo "---- uploading to DB... ----"
# python3 ./tshark_db_upload.py
# echo "---- done uploading to db ----"
echo "program finished"
