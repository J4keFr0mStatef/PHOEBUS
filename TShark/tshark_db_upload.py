import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
# token = os.environ.get('INFLUXDB_TOKEN')
token = "0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw=="
org = "PHOEBUS"
url = "http://10.0.1.1:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "tshark_analytics" 
write_api = client.write_api(write_options=SYNCHRONOUS)

##### ------ READ DATA FILES ------ #####
# Read IP addresses from ip_dst.txt
with open('tshark_outputs/hosts.txt', 'r') as ip_file:
    ip_addresses = ip_file.read().splitlines()
    ip_addresses = list(filter(None, ip_addresses)) # remove empty strings
    ip_addresses.pop() # remove useless last lines
    ip_addresses.pop()

for i in range(len(ip_addresses)):
    ip_addresses[i] = ip_addresses[i].split('\t')
    ip_addresses[i] = {
        "ip": ip_addresses[i][0],
        "host": ip_addresses[i][1]
    }

# Read open ports from open_ports.txt
with open('tshark_outputs/open_ports.txt', 'r') as port_file:
    open_ports = port_file.read().splitlines()
    open_ports = list(filter(None, open_ports)) # remove empty strings

with open('tshark_outputs/bad_ports.txt', 'r') as bad_port_file:
    bad_ports = bad_port_file.read().splitlines()
    bad_ports = list(filter(None, bad_ports)) # remove empty strings

# Read tcp endpoints from stripped_tcp_endpoint_analytics.txt
with open('tshark_outputs/stripped_tcp_endpoint_analytics.txt', 'r') as tcp_file:
    tcp_endpoints = tcp_file.read().splitlines()
    tcp_endpoints.pop() # remove useless last line

# Split the tcp endpoints and data into dictionaries
for i in range(len(tcp_endpoints)):
    tcp_endpoints[i] = tcp_endpoints[i].split(' ')
    tcp_endpoints[i] = {
        "src ip": tcp_endpoints[i][0],
        "src port": tcp_endpoints[i][1],
        "num packets": tcp_endpoints[i][2],
        "transmitted": tcp_endpoints[i][3],
        "received": tcp_endpoints[i][4],
    }

# Read useragent warnings from useragentCheck.txt
with open('tshark_outputs/useragentCheck.txt', 'r') as useragent_file:
    useragent_warnings = useragent_file.read().splitlines()
    useragent_warnings = list(filter(None, useragent_warnings)) # remove empty strings

##### ------ UPLOAD DATA TO INFLUXDB ------ #####
# Create data points for IP addresses
for ip in ip_addresses:
    ip = Point("ip_address")\
        .field("value", ip["ip"])\
        .field("host", ip["host"])
    write_api.write(bucket=bucket, record=ip)

# Create data points for open ports
for port in open_ports:
    # tag ports as privileged, commonly abused, or potentially normal
    if port in bad_ports:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "warning")
        #port_points.append(point)
    elif int(port) <= 1024:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "privileged")
        #port_points.append(point)
    else:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "normal")
        
    # upload the port to the database
    write_api.write(bucket=bucket, record=point)


# Create data points for tcp endpoints
for endpoint in tcp_endpoints:
    point = Point("tcp_endpoint")\
        .field("src ip", endpoint["src ip"])\
        .field("src port", endpoint["src port"])\
        .field("num packets", endpoint["num packets"])\
        .field("transmitted", endpoint["transmitted"])\
        .field("received", endpoint["received"])
    write_api.write(bucket=bucket, record=point)

# Create data points for useragent warnings
for warning in useragent_warnings:
    point = Point("useragent_warning")\
        .field("value", warning)
    write_api.write(bucket=bucket, record=point)

