import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

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

# Query to get the connected client data from the database
query_api = client.query_api()
clients_query = """import "influxdata/influxdb/schema"
from(bucket: "connected_clients")
  |> range(start: -12h, stop: 12h)
  |> filter(fn: (r) => r["_measurement"] == "Connected-Clients")
  |> aggregateWindow(every: 30s, fn: last, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "last")"""

# Get the data from the query
tables = query_api.query(clients_query, org="PHOEBUS")
for table in tables:
  for record in table.records:
    print(f"IP Address: {record['IP']}")
    print(f"MAC Address: {record['MAC Address']}")
    print(f"Hostname: {record['Hostname']}")
    print(f"Timestamp: {record['_time']}")
    print()