from ap_scan import parse_data, scan_aps, clean_data, table_output
import os, subprocess, sys
import maskpass

# Function to connect to a provided access point
def connect(data, pi_wpa_directory="/etc/wpa_supplicant/", pi_wpa_template_dir="/etc/phoebus/wpa_supplicant/"):
    
    # Set the filename to the SSID of the access point
    filename = f"{data['SSID']}.conf"
    out_file = pi_wpa_directory + filename

    with open(out_file, "w") as config_file:
        try:

            ## Check if the access point is using WPA-PSK, WPA-Enterprise, or Open
            # If the access point is using WPA-PSK, ask the user for the password
            if data['Authentication'] == "PSK":
                while True:
                    invalid_chars = ["\"", "\\", "\n", "\t", "]", "\'", "[", "{", "}", "|", "(", ")", ";", ":"]
                    password = maskpass.askpass(prompt="Enter the password: ", mask="*")

                    # Generic password validation
                    if len(password) < 1:
                        print("Invalid password. Please try again.")
                    elif any(char in password for char in invalid_chars):
                        print("Invalid password. Please try again.")
                    else:
                        break
                
                # Write the WPA-PSK configuration to the file
                with open(pi_wpa_template_dir + "wpa_psk_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid=\"" in line:
                            output += f"\tssid=\"{data['SSID']}\"\n"
                        elif "key_mgmt" in line:
                            output += f"\tkey_mgmt=WPA-PSK\n"
                        elif "psk" in line:
                            output += f"\tpsk=\"{password}\"\n"
                        else:
                            output += line
                
                    template.close()
                    
                config_file.write(output)

            # If the access point is using WPA-Enterprise, ask the user for the username and password
            elif data['Authentication'] == "IEEE 802.1X":
                invalid_chars = ["\"", "\\", "\n", "\t", "]", "\'", "[", "{", "}", "|", "(", ")", ";", ":"]
                while True:
                    username = input("Enter the username: ")

                    # Generic username validation
                    if len(username) < 1:
                        print("Invalid username. Please try again.")
                    elif any(char in username for char in invalid_chars):
                        print("Invalid username. Please try again.")
                    else:
                        break

                while True:
                    password = maskpass.askpass(prompt="Enter the password: ", mask="*")

                    # Generic password validation
                    if len(password) < 1:
                        print("Invalid password. Please try again.")
                    elif any(char in password for char in invalid_chars):
                        print("Invalid password. Please try again.")
                    else:
                        break
                
                # Write the WPA-Enterprise configuration to the file
                with open(pi_wpa_template_dir + "wpa_enterprise_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid=\"" in line:
                            output += f"\tssid=\"{data['SSID']}\"\n"
                        elif "key_mgmt" in line:
                            output += f"\tkey_mgmt=WPA-EAP\n"
                        elif "identity" in line:
                            output += f"\tidentity=\"{username}\"\n"
                        elif "password" in line:
                            output += f"\tpassword=\"{password}\"\n"
                        else:
                            output += line

                    template.close()

                config_file.write(output)

            # If the access point is open, write the open network configuration to the file
            else:
                with open(pi_wpa_template_dir + "open_network_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid=\"" in line:
                            output += f"\tssid=\"{data['SSID']}\"\n"
                        else:
                            output += line

                    template.close()

                config_file.write(output)

            config_file.close()
            
            # Return the filename of the configuration file
            return out_file

        # If the user presses Ctrl+C, close the file and remove the configuration file
        except KeyboardInterrupt:
            config_file.close()
            os.remove(out_file)
            print("\nExiting...")
            exit()

# Function to update the interfaces file with the new access point configuration
def update_interfaces(filename, interface, DEBUG=False):

    # Get the list of network interfaces
    interfaces = subprocess.run("ls /sys/class/net", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

    path = "/etc/network/interfaces.d/"

    # If the interface exists, create a new configuration file for it
    if interface in interfaces:
        with open(path + interface, "w") as file:
            file.write(f"auto {interface}\n")
            file.write(f"iface {interface} inet dhcp\n")
            file.write(f"\twpa-conf {filename}\n")

    # Update the network interface by bringing it down and then up again
    ifdown = subprocess.run(f"sudo ifdown {interface}", shell=True, stderr=subprocess.PIPE)
    restart_wpa = subprocess.run("sudo systemctl restart wpa_supplicant.service", shell=True, stderr=subprocess.PIPE)
    ifup = subprocess.run(f"sudo ifup {interface}", shell=True, stderr=subprocess.PIPE)

    # Keep track of any errors that occur when bringing the interface up
    ifup_error = ifup.stderr.decode("utf-8")

    # If the interface fails to come up, print an error message and remove the configuration file
    if "failed to bring up" in ifup_error or "No DHCPOFFERS received" in ifup_error: 
        print("Incorrect Password")
        os.remove(path + interface)
        return False
    
    # If the interface comes up successfully, return True
    else:
        print(ifup_error)
        return True
    
def main():

    ## Constants
    # Directories on the Raspberry Pi
    pi_wpa_directory = "/etc/wpa_supplicant/"
    pi_wpa_template_dir = "/etc/phoebus/wpa_supplicant/"
    pi_ap_data_file = "/etc/phoebus/data/ap_scan/scan_results.txt"

    # Directories within the project repository
    wpa_directory = "../../Files/RaspberryPi/etc/wpa_supplicant/"
    ap_data_file = "../TestData/AP_Scan/apartment_scan.txt"
    wpa_template_dir = "../../Files/RaspberryPi/etc/wpa_supplicant/"

    ## Dynamic variables
    Testing = False
    DEBUG = False
    interface = None

    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python3 ap_connect.py -i <interface> [-d]")
        print("Example: python3 ap_connect.py -i wlan0")
        print()
        print(f"{'Options:':<17} {'Description':<20}")
        print(f"{'-h, --help':<17} {'Display this help message'}")
        print(f"{'-i, --interface':<17} {'Specify the interface to scan'}")
        print(f"{'-d, --debug':<17} {'Enable debug mode'}")
        sys.exit(1)
    
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] in ['-d', '--debug']:
                DEBUG = True
            elif sys.argv[i] in ['-i', '--interface']:
                try:
                    interface = sys.argv[i+1]
                except IndexError:
                    print("Please specify a valid network interface")
                    sys.exit(1)
            elif sys.argv[i-1] in ['-i', '--interface']:
                continue
            else:
                print("Invalid Option")
                sys.exit(1)

        if interface is None and not DEBUG:
            print("Please specify a network interface")
            sys.exit(1)

    # If DEBUG is set to True, disable JSON and table output
    if DEBUG:
        print(f"Debug: {DEBUG}")
        if not Testing:
            print(f"Interface: {interface}")
        print()

    # Check if the script is being run on the Raspberry Pi
    if not Testing:
        wpa_directory = pi_wpa_directory
        ap_data_file = pi_ap_data_file
        wpa_template_dir = pi_wpa_template_dir

        # Get the list of network interfaces
        interfaces = subprocess.run("ls /sys/class/net", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

        # Check if the specified interface is valid
        if interface not in interfaces:
            print(f"Invalid interface: {interface}")
            print("Please specify a valid network interface")
            exit()
        
        else:
            scan_aps(interface, ap_data_file, DEBUG)

    # Get the data from the access point scan
    data = clean_data(parse_data(ap_data_file))

    if len(data) == 0:
        print("Interface is busy. Please try again...")
        sys.exit(1)

    # Output the data in a table
    table_output(data)

    # Ask the user to choose an access point to connect to
    picked_ap = False
    while True:
        try:

            # If the user has not picked an access point, ask them to choose one
            if not picked_ap: 
                ap_num = int(input("\nChoose an Access Point to connect to: ")) - 1
                picked_ap = True
            
            # If the chosen access point is negative, print an error message
            if ap_num < 0:
                print("Invalid Access Point")
                picked_ap = False

            # If the chosen access point is valid, connect to it
            else:
                key = list(data.keys())[ap_num]
                ap = data[key]

                # Connect to the access point
                out_file = connect(ap, wpa_directory, wpa_template_dir)
                print(f"\nConnecting to {ap['SSID']}")

                # Try to update the interfaces file
                if not Testing:
                    connected = update_interfaces(out_file, interface, DEBUG)

                    # If the connection was successful, print a success message and exit
                    if connected:
                        print(f"Connected!")
                        exit()
                
                else:
                    print("Testing...")
                    exit()

        # If the user enters an invalid access point, print an error message
        # If the user presses Ctrl+C, print an exit message and exit
        except (IndexError, ValueError, KeyboardInterrupt) as e:
            if type(e) == KeyboardInterrupt:
                print("\nExiting...")
                exit()
            else:
                print("Invalid Access Point")
                picked_ap = False

if __name__ == "__main__":
    main()

