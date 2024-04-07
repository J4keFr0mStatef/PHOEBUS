import subprocess, time
import json

# Function to sort nearby access points that have been scanned
def get_aps(filename):

    # Store the AP information in a dictionary
    data = {}

    # Open the raw ap data file and parse the information
    with open(filename, 'r') as file:

        # Variable to check if the AP is using encryption
        encryption = False

        for line in file:

            # Check for the MAC address of the access point
            if "Address" in line:

                # Set the encryption flag to false since a new AP has been found
                encryption = False
                mac = line.split()[4]

                # Create a new dictionary entry for the AP
                data[mac] = {}
                data[mac]['SSID'] = ""

            # Check for the SSID of the access point
            if "ESSID" in line:
                ssid = line.split("\"")[1]
                data[mac]['SSID'] = ssid

            # Check for the frequency of the access point
            if "Frequency" in line:
                freq = line.split(':')[1].split()[0]
                data[mac]['Frequency'] = freq
            
            # Check for the channel of the access point
            if "Channel:" in line:
                channel = line.split(':')[1].split("\n")[0]
                data[mac]['Channel'] = channel

            # Check for the quality and signal strength of the access point
            if "Quality" in line:
                quality = line.split()[0].split('=')[1].split('/')[0]
                data[mac]['Quality'] = quality

                signal = line.split()[2].split('=')[1]
                data[mac]['Signal'] = signal
            
            # Check if the access point is using encryption
            # If the AP is using encryption, set the encryption flag to true
            if "Encryption key:on" in line:
                encryption = True
                data[mac]['Encryption'] = ""
                data[mac]['Authentication'] = ""

            # If the AP is not using encryption, set the encryption and authentication type to none
            if "Encryption key:off" in line:
                encryption = False
                data[mac]['Encryption'] = "None"
                data[mac]['Authentication'] = "None"

            # Check for the encryption type and authentication suite of the access point
            if "IE: IEEE" in line and encryption:

                # If the access point is using WPA2, WPA, or WEP, set the encryption type accordingly
                if "WPA2" in line:
                    data[mac]['Encryption'] = "WPA2"
                elif "WPA" in line:
                    data[mac]['Encryption'] = "WPA"
                elif "WEP" in line:
                    data[mac]['Encryption'] = "WEP"
                
                # Otherwise, set the encryption type to none
                else:
                    data[mac]['Encryption'] = "None"
            
            # Check for the authentication suite of the access point
            if "Authentication Suites" in line and encryption:

                # If the access point is using PSK or 802.1x, set the authentication suite accordingly
                if "PSK" in line:
                    data[mac]['Authentication'] = "PSK"
                elif "802.1x" in line:
                    data[mac]['Authentication'] = "802.1x"

                # Otherwise, set the authentication suite to none
                else:
                    data[mac]['Authentication'] = "None"
    
    # Return the dictionary of AP information
    return data

# Function to clean the data by removing any access points that do not have an SSID
def clean_data(data):
    bad_macs = []
    for mac in data:
        if data[mac]['SSID'] == "":
            bad_macs.append(mac)
    for mac in bad_macs:
        data.pop(mac)
    return data

# Function to output the access point information in a table format
def table_output(data):
    print("{:<2} {:<20} {:<25} {:<15} {:<10} {:<10} {:<15}".format("#", 'MAC Address', 'SSID', 'Frequency', 'Channel', 'Quality', 'Signal'))
    print("="*115)
    for mac in data:
        number = list(data.keys()).index(mac) + 1
        ssid = data[mac]['SSID'] if len(data[mac]['SSID']) < 23 else data[mac]['SSID'][:18] + "..." + data[mac]['SSID'][-3:]
        freq = data[mac]['Frequency'] + " GHz"
        channel = data[mac]['Channel']
        quality = data[mac]['Quality']
        signal = data[mac]['Signal'] + " dBm"
        print("{:<2} {:<20} {:<25} {:<15} {:<10} {:<10} {:<15}".format(number, mac, ssid, freq, channel, quality, signal))

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
    ap_data_file = "../TestData/AP_Scan/ap_scan_data.txt"
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
    data = get_aps(ap_data_file)

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