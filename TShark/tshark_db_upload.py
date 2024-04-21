import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ.get('INFLUXDB_TOKEN')
org = "PHOEBUS"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "tshark" 

write_api = client.write_api(write_options=SYNCHRONOUS)

# Read IP addresses from ip_dst.txt
with open('tshark_outputs/ip_dst.txt', 'r') as ip_file:
    ip_addresses = ip_file.read().splitlines()

# Read open ports from open_ports.txt
with open('tshark_outputs/open_ports.txt', 'r') as port_file:
    open_ports = port_file.read().splitlines()

# Create data points for IP addresses
ip_points = []
for ip in ip_addresses:
    point = Point("ip_address").field("value", ip)
    ip_points.append(point)

# Create data points for open ports
port_points = []
for port in open_ports:
    point = Point("open_port")\
        .field("value", port)\
        
    port_points.append(point)

# Write data points to the database
write_api.write(bucket=bucket, record=ip_points)
write_api.write(bucket=bucket, record=port_points)
