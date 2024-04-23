import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "PHOEBUS"
#url = "http://localhost:8086"
url = "http://raspberrypi:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="get-started"

write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="PHOEBUS", record=point)
  time.sleep(1) # separate points by 1 second
