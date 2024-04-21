import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone, timedelta
from connected_clients import connected_clients

# Constants
# Directories on the Raspberry Pi
pi_dhcp_data_directory = "/etc/phoebus/"
pi_dhcp_data_file = "/etc/phoebus/dhcp.leases"

# Directories within the project repository
ap_data_directory = "../APSetup/Scripts/TestData/"
ap_data_file = "../APSetup/Scripts/TestData/modified_test_dhcp_data.txt"

# Dynamic Variables
Testing = False
DEBUG = True

# Check if the script is being run on the Raspberry Pi
if not Testing:
    ap_data_directory = pi_dhcp_data_directory
    ap_data_file = pi_dhcp_data_file

# Database variables
token = "xkbWpVaw8_iOBi97aRSK-ILyLS-Yux2ifbG-qt6Q9VKw0TZeWUa8K0ngndro7Cf2xYy2Cm1V4Dtol6RXf6NYMA=="
org = "PHOEBUS"
url = "http://localhost:8086"
bucket = "connected_clients"

# Create the InfluxDB client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Get the data from the dhcp.leases file
data = connected_clients(ap_data_file)

# Delete current data from the bucket
delete_api = client.delete_api()
delete_api.delete("1970-01-01T00:00:00Z", datetime.now(timezone.utc) + timedelta(days=30), '_measurement="Connected-Clients"', bucket=bucket, org=org)

# Write the data to the InfluxDB bucket
write_api = client.write_api(write_options=SYNCHRONOUS)
for entry in data:
    if entry == "Total Connected":
        continue

    else:
        if DEBUG:
            print(f"IP: {entry}")
            print(f"MAC Address: {data[entry]['MAC Address']}")
            print(f"Hostname: {data[entry]['Hostname']}")
            print(f"Timestamp: {datetime.fromtimestamp(int(data[entry]['Timestamp']), timezone.utc)}")

        p = influxdb_client.Point("Connected-Clients")
        p.field("IP", entry)
        p.field("MAC Address", data[entry]['MAC Address'])
        p.field("Hostname", data[entry]['Hostname'])
        p.time(datetime.fromtimestamp(int(data[entry]['Timestamp']), timezone.utc), write_precision="ns")
        write_api.write(bucket=bucket, org=org, record=p)
