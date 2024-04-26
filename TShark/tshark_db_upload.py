import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ.get('INFLUXDB_TOKEN')
org = "PHOEBUS"
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "tshark_analysis" 
write_api = client.write_api(write_options=SYNCHRONOUS)

# Read IP addresses from ip_dst.txt
with open('tshark_outputs/ip_dst_nslookup.txt', 'r') as ip_file:
    ip_addresses = ip_file.read().splitlines()

# Read open ports from open_ports.txt
with open('tshark_outputs/open_ports.txt', 'r') as port_file:
    open_ports = port_file.read().splitlines()

with open('tshark_outputs/bad_ports.txt', 'r') as bad_port_file:
    bad_ports = bad_port_file.read().splitlines()

# Read tcp endpoints from stripped_tcp_endpoint_analytics.txt
with open('tshark_outputs/stripped_tcp_endpoint_analytics.txt', 'r') as tcp_file:
    tcp_endpoints = tcp_file.read().splitlines()
    tcp_endpoints.pop() # remove useless last line

# Split the tcp endpoints and data into dictionaries
for i in range(len(tcp_endpoints)):
    tcp_endpoints[i] = tcp_endpoints[i].split(' ')
    tcp_endpoints[i] = {
        "src_ip": tcp_endpoints[i][0],
        "src_port": tcp_endpoints[i][1],
        "num_packets": tcp_endpoints[i][2],
        "transmitted": tcp_endpoints[i][3],
        "received": tcp_endpoints[i][4],
    }

# Read useragent warnings from useragentCheck.txt
with open('tshark_outputs/useragentCheck.txt', 'r') as useragent_file:
    useragent_warnings = useragent_file.read().splitlines()

# Create data points for IP addresses
ip_points = []
for ip in ip_addresses:
    point = Point("ip_address")\
        .field("value", ip)
    #ip_points.append(point)
    write_api.write(bucket=bucket, record=point)


# Create data points for open ports
port_points = []
for port in open_ports:
    # tag ports as privileged, commonly abused, or potentially normal
    if port in bad_ports:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "commonly_abused")
        #port_points.append(point)
    elif int(port) <= 1024:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "privileged")
        #port_points.append(point)
    else:
        point = Point("open_port")\
            .field("value", port)\
            .tag("status", "potentially_normal")
        #port_points.append(point)
        
    # upload the port to the database
    write_api.write(bucket=bucket, record=point)


# Create data points for tcp endpoints
tcp_points = []
for endpoint in tcp_endpoints:
    point = Point("tcp_endpoint")\
        .field("src_ip", endpoint["src_ip"])\
        .field("src_port", endpoint["src_port"])\
        .field("num_packets", endpoint["num_packets"])\
        .field("transmitted", endpoint["transmitted"])\
        .field("received", endpoint["received"])
    #tcp_points.append(point)
    write_api.write(bucket=bucket, record=point)

# Create data points for useragent warnings
useragent_points = []
for warning in useragent_warnings:
    point = Point("useragent_warning")\
        .field("value", warning)
    #useragent_points.append(point)
    write_api.write(bucket=bucket, record=point)

