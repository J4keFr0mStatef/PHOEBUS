import influxdb_client, time
from influxdb_client.client.write_api import SYNCHRONOUS

# Function to convert bytes to a human readable format
def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)

    return '{0:.2f}'.format(B / MB)


token = "aBS4lFVpEsfAu-wpAUZeuLBMBR6UJSJadTexlCQVjAOHRnK6eM_GgFWdXdECffpdn1C01Rcjff4xN6oAI-wr8A=="
org = "PHOEBUS"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()

# Query to get the hourly data
hourly_query = """import "influxdata/influxdb/schema"
    from(bucket: "hourly_data")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
        |> filter(fn: (r) => r["Timeframe"] == "hour")
        |> filter(fn: (r) => r["interface"] == "eth0" or r["interface"] == "wlan0" or r["interface"] == "wlan1")
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
        |> schema.fieldsAsCols()
        |> yield(name: "mean")"""

# Query to get the daily data
daily_query = """import "influxdata/influxdb/schema"
from(bucket: "daily_data")
  |> range(start: -30d)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> filter(fn: (r) => r["Timeframe"] == "day")
  |> filter(fn: (r) => r["interface"] == "eth0" or r["interface"] == "wlan0" or r["interface"] == "wlan1")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")"""

# Query to get the monthly data
monthly_query = """import "influxdata/influxdb/schema"
from(bucket: "monthly_data")
  |> range(start: -1y)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> filter(fn: (r) => r["Timeframe"] == "month")
  |> filter(fn: (r) => r["interface"] == "eth0" or r["interface"] == "wlan0" or r["interface"] == "wlan1")
  |> aggregateWindow(every: 30d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")"""

# Query the hourly data
tables = query_api.query(hourly_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Timeframe: {record['Timeframe']}")
    print(f"Hour: {record['hour']}")
    print(f"RX: {humanbytes(record['rx_bytes'])}")
    print(f"TX: {humanbytes(record['tx_bytes'])}")
    print()

# Query the daily data
tables = query_api.query(daily_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Timeframe: {record['Timeframe']}")
    print(f"Day: {record['day']}")
    print(f"RX: {humanbytes(record['rx_bytes'])}")
    print(f"TX: {humanbytes(record['tx_bytes'])}")
    print()

# Query the monthly data
tables = query_api.query(monthly_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Timeframe: {record['Timeframe']}")
    print(f"Month: {record['month']}")
    print(f"RX: {humanbytes(record['rx_bytes'])}")
    print(f"TX: {humanbytes(record['tx_bytes'])}")
    print()