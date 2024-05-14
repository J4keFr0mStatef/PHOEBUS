import subprocess, sys, json

# Function to determine if client is connected
def is_client_connected(ip_address):
    try:
        result = subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        return result.returncode == 0
    except Exception as e:
        return False

# Function to create a list of connected clients
def connected_clients(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            timestamp, mac, ip_address, hostname, _ = line.split()
            if hostname == '*':
                hostname = 'N/A'
            data[ip_address] = {
                'Timestamp': timestamp,
                'MAC Address': mac,
                'Hostname': hostname
            }
        sorted_ips = sorted(data.keys(), key=lambda x: list(map(int, x.split('.'))))

        num_connected = len(data.keys())
        
        sorted_data = {}
        sorted_data["Total Connected"] = num_connected
        for ip in sorted_ips:
            sorted_data[ip] = data[ip]

    return sorted_data

# Function to create a table of connected clients
def table_output(data):
    print("{:<12} {:<18} {:<15} {:<20}".format('Timestamp', 'MAC Address', 'IP Address', 'Hostname'))
    print("="*68)
    for ip in data:
        if ip == "Total Connected":
            continue
        else:
            timestamp = data[ip]['Timestamp']
            mac = data[ip]['MAC Address']
            hostname = data[ip]['Hostname']
            print("{:<12} {:<18} {:<15} {:<20}".format(timestamp, mac, ip, hostname))

def to_json(data, out_file):
    with open(out_file, "w") as file:
        json.dump(data, file, indent=4)

def main():

    # Constants
    # Directories on the Raspberry Pi
    pi_dhcp_data_directory = "/etc/phoebus/"
    pi_dhcp_data_file = "/etc/phoebus/dhcp.leases"
    pi_out_file = "/etc/phoebus/data/connected_clients/connected_clients.json"

    # Directories within the project repository
    ap_data_directory = "../TestData/DHCP/"
    ap_data_file = "../TestData/DHCP/test_dhcp_data.txt"
    out_file = "../TestData/DHCP/connected_clients.json"

    # Dynamic Variables
    Testing = False
    DEBUG = False
    JSON_OUTPUT = False
    TABLE_OUTPUT = False 

    # Check for command line arguments
    # If no arguments are provided, or -h is provided, display the help message
    if len(sys.argv) < 1 or '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python3 connected_clients.py [-d] [-j] [-t]")
        print("Example: python3 connected_clients.py -j")
        print()
        print(f"{'Options:':<17} {'Description':<20}")
        print(f"{'-h, --help':<17} {'Display this help message'}")
        print(f"{'-d, --debug':<17} {'Enable debug mode'}")
        print(f"{'-j, --json':<17} {'Output data in JSON format'}")
        print(f"{'-t, --table':<17} {'Output data in table format'}")
        sys.exit(1)
    
    # Otherwise parse the command line arguments
    else:
        for i in range(1, len(sys.argv)):

            # If the argument is -d, -j, or -t, set the corresponding variable to True
            if sys.argv[i] in ['-d', '--debug']:
                DEBUG = True
            elif sys.argv[i] in ['-j', '--json']:
                JSON_OUTPUT = True
            elif sys.argv[i] in ['-t', '--table']:
                TABLE_OUTPUT = True

            # If the argument is not recognized, display an error message and exit
            else:
                print("Invalid Option")
                sys.exit(1)

    # If DEBUG is set to True, disable JSON and table output
    if DEBUG:
        JSON_OUTPUT = False
        TABLE_OUTPUT = False

        print(f"Debug: {DEBUG}")
        print(f"JSON Output: {JSON_OUTPUT}")
        print(f"Table Output: {TABLE_OUTPUT}")
        print()

    # Check if the output format is valid
    elif not JSON_OUTPUT and not TABLE_OUTPUT:
        print("Invalid Output Format")
        print("Please set either -j or -t to output the data in JSON or table format, respectively.")
        sys.exit(1)

    elif JSON_OUTPUT and TABLE_OUTPUT:
        print("Invalid Output Format")
        print("Please set either -j or -t to output the data in JSON or table format, respectively.")
        sys.exit(1)

    # Check if the script is being run on the Raspberry Pi
    if not Testing:
        ap_data_directory = pi_dhcp_data_directory
        ap_data_file = pi_dhcp_data_file
        out_file = pi_out_file

    data = connected_clients(ap_data_file)

    if TABLE_OUTPUT and not JSON_OUTPUT and not DEBUG:
        table_output(data)
    if JSON_OUTPUT and not TABLE_OUTPUT and not DEBUG:
        to_json(data, out_file)
    if DEBUG and not TABLE_OUTPUT and not JSON_OUTPUT:
        print("Table Output")
        table_output(data)
        print()
        print("JSON Output")
        print(data)

if __name__ == "__main__":
    main()