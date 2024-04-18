import influxdb_client, time, json
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone, timedelta

token = "aBS4lFVpEsfAu-wpAUZeuLBMBR6UJSJadTexlCQVjAOHRnK6eM_GgFWdXdECffpdn1C01Rcjff4xN6oAI-wr8A=="
org = "PHOEBUS"
url = "http://10.0.1.1:8086"


# File needs to be changed to the path of the vnstat_data.json file
# file = "../APSetup/Scripts/TestData/InterfaceData/vnstat_data.json"
file = "vnstat_data.json"

# Buckets for hourly, daily, and monthly data
fiveminute_bucket = "fiveminute_interface_data"
hourly_bucket = "hourly_interface_data"
daily_bucket = "daily_interface_data"
monthly_bucket = "monthly_interface_data"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

# Load the data from the file
data = json.load(open(file, "r"))

# Get the current time and the time frames for yesterday, thirty days ago, and one year ago
current_time = datetime.now()
current_utc_time = datetime.now(timezone.utc)
one_hour_ago = current_utc_time - timedelta(hours=1)
yesterday = current_utc_time - timedelta(days=1)
thirty_days_ago = current_utc_time - timedelta(days=30)
one_year_ago = current_utc_time - timedelta(days=365)

print(f"UTC: {current_utc_time}")
print(f"Local: {current_time}")
print(f"One hour ago: {one_hour_ago}")
print(f"Yesterday: {yesterday}")
print(f"30 Days ago: {thirty_days_ago}")
print(f"One Year Ago {one_year_ago}")
print()

# Loop through each interface in the data
for interface in data['interfaces']:

    # Loop through each entry in the hourly data
    for entry in interface['traffic']['fiveminute']:

        # Check if the timestamp is older than yesterday
        if entry['timestamp'] < one_hour_ago.timestamp():
            continue

        # If the timestamp is not older than yesterday, write the data to the hourly bucket
        else:

            # Create a new point
            p = influxdb_client.Point("Interface-Data")
            p.tag("interface", interface['name'])
            p.time(datetime.fromtimestamp(entry['timestamp'], timezone.utc), write_precision="ns")
            p.field("minute", entry['time']['minute'])
            p.field("total_bytes", float(entry['rx']) + float(entry['tx']))

            # Write the point to the hourly bucket
            write_api.write(bucket=fiveminute_bucket, org=org, record=p)

    # Loop through each entry in the hourly data
    for entry in interface['traffic']['hour']:

        # Check if the timestamp is older than yesterday
        if entry['timestamp'] < yesterday.timestamp():
            continue

        # If the timestamp is not older than yesterday, write the data to the hourly bucket
        else:

            # Create a new point
            p = influxdb_client.Point("Interface-Data")
            p.tag("interface", interface['name'])
            p.time(datetime.fromtimestamp(entry['timestamp'], timezone.utc), write_precision="ns")
            p.field("hour", entry['time']['hour'])
            p.field("total_bytes", float(entry['rx']) + float(entry['tx']))

            # Write the point to the hourly bucket
            write_api.write(bucket=hourly_bucket, org=org, record=p)
    
    # Loop through each entry in the daily data
    for entry in interface['traffic']['day']:

        # Check if the timestamp is older than thirty days ago
        if entry['timestamp'] < thirty_days_ago.timestamp():
            continue

        # If the timestamp is not older than thirty days ago, write the data to the daily bucket
        else:

            # Create a new point
            p = influxdb_client.Point("Interface-Data")
            p.tag("interface", interface['name'])
            p.time(datetime.fromtimestamp(entry['timestamp'], timezone.utc), write_precision="ns")
            p.field("day", entry['date']['day'])
            p.field("total_bytes", float(entry['rx']) + float(entry['tx']))

            # Write the point to the daily bucket
            write_api.write(bucket=daily_bucket, org=org, record=p)

    # Loop through each entry in the monthly data
    for entry in interface['traffic']['month']:

        # Check if the timestamp is older than one year ago
        if entry['timestamp'] < one_year_ago.timestamp():
            continue

        # If the timestamp is not older than one year ago, write the data to the monthly bucket
        else:

            # Create a new point
            p = influxdb_client.Point("Interface-Data")
            p.tag("interface", interface['name'])
            p.time(datetime.fromtimestamp(entry['timestamp'], timezone.utc), write_precision="ns")
            p.field("month", entry['date']['month'])
            p.field("total_bytes", float(entry['rx']) + float(entry['tx']))

            # Write the point to the monthly bucket
            write_api.write(bucket=monthly_bucket, org=org, record=p)

