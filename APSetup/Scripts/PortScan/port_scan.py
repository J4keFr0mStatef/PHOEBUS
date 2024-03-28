import nmap
import json
from APSetup.Scripts.ConnectedClients.connected_clients import connected_clients, is_client_connected

test = nmap.PortScanner()

filename = '../TestData/DHCP/test_dhcp_data.txt'
output = '../TestData/port_scan.json'

ips = list(connected_clients(filename).keys())
output = {}
# for ip in ips:
#     if is_client_connected(ip):
#         data = test.scan(ip, '1-1024')
#         sorted_data = {}
#         for host in data['scan']:
#             sorted_data[host] = data['scan'][host]
#         output.update(sorted_data)
data = test.scan("localhost", '1-1024')
sorted_data = {}
for host in data['scan']:
    sorted_data[host] = data['scan'][host]
output.update(sorted_data)

print(output)

json.dump(sorted_data, open(output, 'w'), indent=4)  