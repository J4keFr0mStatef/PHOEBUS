import subprocess, time
import json

# Function to parse the data from the access point scan
def parse_data(data_file):
    
    # Open the raw ap data file and read the information
    with open(data_file, 'r') as file:
        data = file.read()
    
    file.close()

    # Store the AP information in a dictionary
    ap_dict = {}
    
    # Variable to store the current MAC address
    current_ap_mac = None

    # Variable to check if the AP is using encryption
    encryption = False

    # Parse the data from the access point scan
    for line in data.split('\n'):

        # Check for the MAC address of the access point
        if line.startswith('BSS '):
            current_ap_mac = line.split()[1].split("(")[0]
            
            # Set the encryption flag to false since a new AP has been found
            encryption = False

            # Create a new dictionary entry for the AP
            ap_dict[current_ap_mac] = {}
            ap_dict[current_ap_mac]['SSID'] = ""
            ap_dict[current_ap_mac]['Encryption'] = "None"
            ap_dict[current_ap_mac]['Authentication'] = "Open"

        # Check for the SSID of the access point
        if "SSID: " in line:
            ssid = line.split(": ")[1]
            ap_dict[current_ap_mac]['SSID'] = ssid

        # Check for the frequency of the access point
        if "freq: " in line:
            ap_dict[current_ap_mac]['Frequency'] = str(float(int(line.split("freq: ")[1].split()[0])/1000))

        # Check for the channel of the access point
        if "DS Parameter set:" in line:
             ap_dict[current_ap_mac]['Channel'] = str(int(line.split(": channel ")[1]))

        if "* primary channel: " in line:
             ap_dict[current_ap_mac]['Channel'] = str(int(line.split("* primary channel: ")[1]))

        # Check for the signal strength of the access point
        if "signal: " in line:
            ap_dict[current_ap_mac]['Signal'] = str(float(line.split("signal: ")[1].split()[0]))
        
        # Check if the access point is using encryption
        # If the AP is using encryption, set the encryption flag to true
        if "RSN:" in line:
            encryption = True
            ap_dict[current_ap_mac]['Encryption'] = "" 
            ap_dict[current_ap_mac]['Authentication'] = ""
        
        # If the AP is using encryption, check for the encryption type
        if " Pairwise ciphers: " in line and encryption:
            ap_dict[current_ap_mac]['Encryption'] = line.split(": ")[1]
        
        # If the AP is using encryption, check for the authentication suite
        if "Authentication suites: " in line and encryption:
            ap_dict[current_ap_mac]['Authentication'] = line.split(": ")[1]

    # Return the dictionary containing the access point information
    return ap_dict

# Function to clean the data by removing any access points with missing SSIDs or duplicate SSIDs 
def clean_data(data):
    bad_macs = []
    ssids = []
    for mac in data:
        if data[mac]['SSID'] == "":
            bad_macs.append(mac)
        elif data[mac]['SSID'] in ssids:
            bad_macs.append(mac)
        else:
            ssids.append(data[mac]['SSID'])
    for mac in bad_macs:
        data.pop(mac)
    return data

# Function to output the access point information in a table format
def table_output(data):
    print("{:>3} {:<20} {:<25} {:<15} {:<10} {:<15} {:<10}".format("#", 'MAC Address', 'SSID', 'Frequency', 'Channel', 'Signal', 'Authentication'))
    print("="*115)
    for mac in data:
        number = list(data.keys()).index(mac) + 1
        ssid = data[mac]['SSID'] if len(data[mac]['SSID']) < 23 else data[mac]['SSID'][:18] + "..." + data[mac]['SSID'][-3:]
        freq = data[mac]['Frequency'] + " GHz"
        channel = data[mac]['Channel']
        signal = data[mac]['Signal'] + " dBm"
        auth = data[mac]['Authentication']
        print("{:>3} {:<20} {:<25} {:<15} {:<10} {:<15} {:<10}".format(number, mac, ssid, freq, channel, signal, auth))

# Function to output the access point information to a JSON file
def to_json(data, out_file):
    with open(out_file, 'w') as file:
        json.dump(data, file, indent=4)

# Function to scan for nearby access points
def scan_aps(interface, out_file, DEBUG=False):

    # Remove any existing configuration files for the interface
    remove_file = subprocess.run(f"sudo rm /etc/network/interfaces.d/{interface}*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the interface ready for scanning
    # Bring the interface down and then back up
    ifdown = subprocess.run(f"sudo ip link set {interface} down", shell=True, stdout=subprocess.PIPE)
    ifup = subprocess.run(f"sudo ip link set {interface} up", shell=True, stdout=subprocess.PIPE)

    # Wait for the interface to be ready
    if DEBUG:
        print("Waiting for resources...")
    time.sleep(4)

    # Begin scanning for nearby access points
    if DEBUG:
        print("Scanning for nearby access points...")
    proc = subprocess.run(f"sudo iwlist {interface} scan > {out_file}", shell=True)


def main():

    # Constants
    # Directories on the Raspberry Pi
    pi_ap_data_directory = "/etc/phoebus/data/ap_Scan/"
    pi_ap_data_file = "/etc/phoebus/data/ap_Scan/ap_scan_data.txt"
    pi_out_file = "/etc/phoebus/data/ap_Scan/ap_scan.json"

    # Directories within the project repository
    ap_data_directory = "../TestData/ap_Scan/"
    ap_data_file = "../TestData/AP_Scan/new_data.txt"
    out_file = "../TestData/AP_Scan/ap_scan.json"

    # Dynamic variables
    Testing = True
    DEBUG = True
    JSON_OUTPUT = True
    TABLE_OUTPUT = False
    interface = "wlan0"

    # If DEBUG is set to True, disable JSON and table output
    if DEBUG:
        JSON_OUTPUT = False
        TABLE_OUTPUT = False

    # Check if the script is being run on the Raspberry Pi
    if not Testing:
        ap_data_directory = pi_ap_data_directory
        ap_data_file = pi_ap_data_file
        out_file = pi_out_file

        scan_aps(interface, ap_data_file, DEBUG)
    
    # Get the data from the access point scan
    data = parse_data(ap_data_file)

    # Output the data in the desired format
    if TABLE_OUTPUT and not JSON_OUTPUT and not DEBUG:
        table_output(data)

    elif JSON_OUTPUT and not TABLE_OUTPUT and not DEBUG:
        to_json(clean_data(data), out_file)

    # If DEBUG is set to True, output the data in both table and JSON format
    elif DEBUG and not TABLE_OUTPUT and not JSON_OUTPUT:
        print("Table Output")
        print("Raw Data:")
        table_output(data)
        print()
        print("Cleaned Data:")
        table_output(clean_data(data))
        print()
        print("JSON Output")
        print("Raw Data:")
        print(data)
        print()
        print("Cleaned Data:")
        print(clean_data(data))
    
    # If neither TABLE_OUTPUT nor JSON_OUTPUT is set to True, print an error message
    else:
        print("Invalid Output Format")
        print("Please set either TABLE_OUTPUT or JSON_OUTPUT to True")

if __name__ == "__main__":
    main()
