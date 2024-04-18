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
url = "http://10.0.1.1:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()

# Query to get the fiveminute data
fiveminute_query = """import "influxdata/influxdb/schema"
    from(bucket: "fiveminute_interface_data")
        |> range(start: -1h)
        |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
        |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
        |> schema.fieldsAsCols()
        |> yield(name: "mean")"""

# Query to get the hourly data
hourly_query = """import "influxdata/influxdb/schema"
    from(bucket: "hourly_interface_data")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> schema.fieldsAsCols()
        |> yield(name: "mean")"""

# Query to get the daily data
daily_query = """import "influxdata/influxdb/schema"
from(bucket: "daily_interface_data")
  |> range(start: -30d)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")"""

# Query to get the monthly data
monthly_query = """import "influxdata/influxdb/schema"
from(bucket: "monthly_interface_data")
  |> range(start: -1y)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> aggregateWindow(every: 30d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")"""

# Query the hourly data
tables = query_api.query(fiveminute_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Minute: {record['minute']}")
    print(f"Total MBs: {humanbytes(record['total_bytes'])}")
    print()

# Query the hourly data
tables = query_api.query(hourly_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Hour: {record['hour']}")
    print(f"Total MBs: {humanbytes(record['total_bytes'])}")
    print()

# Query the daily data
tables = query_api.query(daily_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Day: {record['day']}")
    print(f"Total MBs: {humanbytes(record['total_bytes'])}")
    print()

# Query the monthly data
tables = query_api.query(monthly_query, org="PHOEBUS")

# Loop through the tables and records to print the data
for table in tables:
  for record in table.records:
    print(f"Interface: {record['interface']}")
    print(f"Month: {record['month']}")
    print(f"Total MBs: {humanbytes(record['total_bytes'])}")
    print()