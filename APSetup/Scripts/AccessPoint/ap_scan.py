import subprocess, time
import json

def get_aps(filename):
    data = {}
    with open(filename, 'r') as file:
        encryption = False
        for line in file:
            if "Address" in line:
                encryption = False
                mac = line.split()[4]
                data[mac] = {}
                data[mac]['SSID'] = ""
            if "ESSID" in line:
                ssid = line.split("\"")[1]
                data[mac]['SSID'] = ssid
            if "Frequency" in line:
                freq = line.split(':')[1].split()[0]
                data[mac]['Frequency'] = freq
            if "Channel:" in line:
                channel = line.split(':')[1].split("\n")[0]
                data[mac]['Channel'] = channel
            if "Quality" in line:
                quality = line.split()[0].split('=')[1].split('/')[0]
                data[mac]['Quality'] = quality

                signal = line.split()[2].split('=')[1]
                data[mac]['Signal'] = signal
            if "Encryption key:on" in line:
                encryption = True
                data[mac]['Encryption'] = ""
                data[mac]['Authentication'] = ""
            if "Encryption key:off" in line:
                encryption = False
                data[mac]['Encryption'] = "None"
                data[mac]['Authentication'] = "None"
            if "IE: IEEE" in line and encryption:
                if "WPA2" in line:
                    data[mac]['Encryption'] = "WPA2"
                elif "WPA" in line:
                    data[mac]['Encryption'] = "WPA"
                elif "WEP" in line:
                    data[mac]['Encryption'] = "WEP"
                else:
                    data[mac]['Encryption'] = "None"
            if "Authentication Suites" in line and encryption:
                if "PSK" in line:
                    data[mac]['Authentication'] = "PSK"
                elif "802.1x" in line:
                    data[mac]['Authentication'] = "802.1x"
                else:
                    data[mac]['Authentication'] = "None"
    
    return data

def clean_data(data):
    bad_macs = []
    for mac in data:
        if data[mac]['SSID'] == "":
            bad_macs.append(mac)
    for mac in bad_macs:
        data.pop(mac)
    return data

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

def to_json(data, out_file):
    with open(out_file, 'w') as file:
        json.dump(data, file, indent=4)

def scan_aps(interface, out_file, DEBUG=False):
    remove_file = subprocess.run(f"sudo rm /etc/network/interfaces.d/{interface}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ifdown = subprocess.run(f"sudo ip link set {interface} down", shell=True, stdout=subprocess.PIPE)
    ifup = subprocess.run(f"sudo ip link set {interface} up", shell=True, stdout=subprocess.PIPE)

    if DEBUG:
        print("Waiting for resources...")
    time.sleep(3)

    if DEBUG:
        print("Scanning for nearby access points...")

    proc = subprocess.run(f"sudo iwlist {interface} scan > {out_file}", shell=True)


def main():

    DEBUG = False
    JSON_OUTPUT = True
    TABLE_OUTPUT = False

    pi_ap_data_directory = "/etc/phoebus/data/AP_Scan/"
    pi_ap_data_file = "/etc/phoebus/data/AP_Scan/ap_scan_data.txt"
    pi_out_file = "/etc/phoebus/data/AP_Scan/ap_scan.json"

    project_ap_data_directory = "../TestData/AP_Scan/ap_scan_data.txt"
    project_ap_data_file = "../TestData/AP_Scan/ap_scan_data.txt"
    project_out_file = "../TestData/AP_Scan/ap_scan.json"

    interface = "wlan0"

    scan_aps(interface, pi_ap_data_file, DEBUG)

    data = get_aps(pi_ap_data_file)

    if TABLE_OUTPUT and not JSON_OUTPUT and not DEBUG:
        table_output(data)
    elif JSON_OUTPUT and not TABLE_OUTPUT and not DEBUG:
        to_json(clean_data(data), pi_out_file)
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
    else:
        print("Usage: python ap_scan.py [interface] [output file]")

if __name__ == "__main__":
    main() 