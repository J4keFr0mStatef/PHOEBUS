import subprocess

gui_config_file = "example.conf"
# phoebus_dns_file = "../APSetup/dnsmasq.d/phoebus-dns.conf"
# phoebus_dhcp_file = "../APSetup/dnsmasq.d/phoebus-dhcp.conf"

phoebus_dns_file = "dns.conf"
phoebus_dhcp_file = "dhcp.conf"
phoebus_hostapd_file = "hostapd.conf"
phoebus_interface_directory = "./"

# gui_config_file = r"/etc/phoebus/setupVars.conf"
# phoebus_dns_file = r"/etc/dnsmasq.d/phoebus-dns.conf"
# phoebus_dhcp_file = r"/etc/dnsmasq.d/phoebus-dhcp.conf"
# phoebus_hostapd_file = r"/etc/hostapd/hostapd.conf"
# phoebus_interface_directory = r"/etc/network/interfaces.d/"

### Function to write data to the dns and dhcp files
# data: dictionary containing the data to be written
# type: the syntax that dnsmasq uses for its config file
# file: the output file that the data will be written to 
def write_data(data, type, file=""):

    # Functionality for the type: Domain 
    if type == "domain":
        with open(file, 'a') as f:
            f.write(f"{type}={data}\n")
            f.write(f"local=/{data}/\n")
            f.close()

    # Functionality for the type: dhcp-range (creates the subnet)
    elif type == "dhcp-range":
        with open(file, 'a') as f:
            for interface in data:
                if data[interface]['mode'] == "True":
                    continue
                else:
                    output = f"{type}={interface},{data[interface]['subnet']['start']},{data[interface]['subnet']['end']},{data[interface]['subnet']['mask']},{data[interface]['subnet']['lease']}\n"
                    output += f"dhcp-option={interface},3,{data[interface]['subnet']['router']}"
                    f.write(f"{output}\n")
            f.close()

    # Functionality for the boolean options
    elif type == "dhcp-option":
        with open(file, 'a') as f:
            for key in data:
                if data[key] == "True":
                    if key == "DHCP_AUTHORITATIVE":
                        output = "dhcp-authoritative"
                    elif key == "DHCP_SEQUENTIAL":
                        output = "dhcp-sequential-ip"
                    f.write(f"{output}\n")
                else:
                    f.write("")
            f.close()
            
    elif type == "access-point":
        with open(file, 'w') as f:
            for interface in data:
                if interface == "eth0":
                    continue
                elif data[interface]['mode'] == "True":
                    continue
                else:
                    output = f"interface={interface}\n"
                    output += f"ssid={data[interface]['ap']['ssid']}\n"
                    output += "driver=nl80211\nhw_mode=a\nchannel=36\ncountry_code=US\n"
                    output += "ieee80211d=1\nieee80211n=1\nieee80211ac=1\nwmm_enabled=1\n"
                    output += "macaddr_acl=0\nignore_broadcast_ssid=0\n"

                    if data[interface]['ap']['auth'] == "PSK":
                        output += f"auth_algs=1\nwpa=2\nwpa_key_mgmt=WPA-PSK\nrsn_pairwise=CCMP\nwpa_pairwise=CCMP\n"
                        output += f"wpa_passphrase={data[interface]['ap']['pass']}\n"
                    elif data[interface]['ap']['auth'] == "Open":
                        output += f"wpa=0\n"
                    
                    f.write(f"{output}\n")

            f.close()
        
    elif type == "interface-data":
        for interface in data:
            if data[interface]['mode'] == "True":
                text = ""
                with open(file + interface, 'r') as f:
                    text = f.read()
                    f.close()
                
                with open(file + interface, 'w') as f:
                    output = f"auto {interface}\n"
                    output += f"iface {interface} inet dhcp\n"
                    for line in text.split("\n"):
                        if "wpa-conf" in line:
                            output += f"{line}"
                        else:
                            continue

                    f.write(f"{output}\n")
                    f.close()

            else:
                with open(file + interface, 'w') as f:
                    output = f"auto {interface}\n"
                    output += f"iface {interface} inet static\n"
                    output += f"\taddress {data[interface]['subnet']['router']}\n"
                    output += f"\tnetmask {data[interface]['subnet']['mask']}\n"
                    
                    f.write(f"{output}\n")
                    f.close()
                
    elif type == "interface":
        with open(file, 'a') as f:
            for interface in data:
                output = f"interface={interface}"
                f.write(f"{output}\n")
            f.close()
    
    # For any other type use the format: type=data
    else:
        for key in data:
            with open(file, 'a') as f:
                output = f"{type}={data[key]}"
                f.write(f"{output}\n")
            f.close()


### Function to erase data from the dns and dhcp files
# file: the file to be erased
# option: specifies if the dns or dhcp data should be rewritten to the file
# otherwise the entire file will be erased
def erase_data(file, option=None):

    with open(file, 'w') as f:
        # If the option is dhcp, write the unchangeable dhcp options back to the file.
        if option == "dhcp":
            f.write("dhcp-leasefile=/etc/phoebus/dhcp.leases\n")
    
        # If the option is dns, write the unchangeable dns options back to the file.
        elif option == "dns":
            output = "localise-queries\nno-resolv\ndomain-needed\nexpand-hosts\nbogus-priv\n"
            output += "log-queries\nlog-async\nlog-facility=/var/log/phoebus/phoebus.log\n"
            output += "addn-hosts=/etc/phoebus/local.list\naddn-hosts=/etc/phoebus/custom.list\n"
            output += "dhcp-ignore-names=set:hostname-ignore\ndhcp-name-match=set:hostname-ignore,wpad\n"
            output += "dhcp-name-match=set:hostname-ignore,localhost\ncache-size=10000\n"
            f.write(output)
        
        elif option == "access-point":
            output = "driver=nl80211\nhw_mode=a\nchannel=36\ncountry_code=US\n"
            output += "ieee80211d=1\nieee80211n=1\nieee80211ac=1\nwmm_enabled=1\n"
            output += "macaddr_acl=0\nignore_broadcast_ssid=0\n"
            f.write(output)

        # If the option is none, erase the entire file
        else:
            f.write("")

        f.close()

### Function to get the data from the config file
# config_file: the file to get the data from
def get_data(config_file):

    interface_data = {}
    dns_servers = {}
    dhcp_options = {}
    domain_name = None

    # Open the config file in read mode
    with open(config_file, "r") as f:

        # variables to check if a subnet has been initialized
        is_subnet = False
        subnet_name = None
        interface = None

        for line in f:
            key = line.split('=')[0]
            value = line.split('=')[1].strip("\n")

            if "IFACE" in key:
                interface_data[value] = {}
            
            if "DNS" in key:
                dns_servers[key] = value
            
            if "DHCP_" in key:
                dhcp_options[key] = value
            
            if "_SUBNET" in key:
                subnet_name = value
                interface_data[subnet_name]['subnet'] = {}
                is_subnet = True

            if "_START" in key and is_subnet:
                interface_data[subnet_name]["subnet"]['start'] = value

            if "_END" in key and is_subnet:
                interface_data[subnet_name]["subnet"]['end'] = value
            
            if "_MASK" in key and is_subnet:
                interface_data[subnet_name]["subnet"]['mask'] = value

            if "_ROUTER" in key and is_subnet:
                interface_data[subnet_name]["subnet"]['router'] = value
            
            if "_LEASE" in key and is_subnet:
                interface_data[subnet_name]["subnet"]['lease'] = value
                is_subnet = False

            if "_MODE" in key:
                interface_data[subnet_name]['mode'] = value

            if "DOMAIN" in key:
                domain_name = value

            if "_SSID" in key:
                interface = key.split("_")[0].lower()
                interface_data[interface]["ap"] = {}
                interface_data[interface]["ap"]["ssid"] = value
            
            if "_AUTHENTICATION" in key:
                interface_data[interface]["ap"]["auth"] = value
            
            if "_PASS" in key:
                interface_data[interface]["ap"]["pass"] = value
            
        f.close()

    return interface_data, dns_servers, dhcp_options, domain_name

# Get data from the config file
interface_data, dns_servers, dhcp_options, domain_name = get_data(gui_config_file)

interfaces = [interface for interface in interface_data]

# Write data to dns file
erase_data(phoebus_dns_file, "dns")
write_data(interfaces, "interface" , phoebus_dns_file)
write_data(dns_servers, "server", phoebus_dns_file)

# Write data to dhcp file
erase_data(phoebus_dhcp_file, "dhcp")
write_data(dhcp_options, "dhcp-option", phoebus_dhcp_file)
write_data(domain_name, "domain", phoebus_dhcp_file)
write_data(interface_data, "dhcp-range", phoebus_dhcp_file)

# # Write data to hostapd file
write_data(interface_data, "access-point", phoebus_hostapd_file)

# # Write data to the interface file
write_data(interface_data, "interface-data", phoebus_interface_directory)

# Restart the necessary services
# dnsmasq = subprocess.run(f"sudo systemctl restart dnsmasq.service", shell=True, stderr=subprocess.PIPE)
# print(dnsmasq.stderr)

# hostapd = subprocess.run(f"sudo systemctl restart hostapd.service", shell=True, stderr=subprocess.PIPE)
# print(hostapd.stderr)

# networking = subprocess.run(f"sudo systemctl restart networking.service", shell=True, stderr=subprocess.PIPE)
# print(networking.stderr)

# ifdown = subprocess.run(f"sudo ifdown eth0", shell=True, stderr=subprocess.PIPE)
# ifup = subprocess.run(f"sudo ifup eth0", shell=True, stderr=subprocess.PIPE)

# print(ifdown.stderr)
# print(ifup.stderr)