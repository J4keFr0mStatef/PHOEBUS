function query(org, token, query_data) {

    const options = {
        method: 'POST',
        body: query_data,
        headers: {
          'Content-Type': 'application/vnd.flux',
          'Authorization': `Token ${token}`,
          'Accept': 'application/csv'
        }
    }

    var data = fetch(`http://${location.host}:8086/api/v2/query?org=${org}`, options)
        .then(response => response.text())
        .then(text => { return Papa.parse(text, { header: true }) });

    data.then(val => console.log(val));

    return data;
}

const org = "PHOEBUS";
const token = "0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw==";

// Query for Five Minute Traffic
const query_fiveminute_traffic = `import "influxdata/influxdb/schema"
from(bucket: "fiveminute_interface_data")
    |> range(start: -1h)
    |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
    |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
    |> schema.fieldsAsCols()
    |> yield(name: "mean")`

// Query for Hourly Traffic
const query_hourly_traffic = `import "influxdata/influxdb/schema"
from(bucket: "hourly_interface_data")
    |> range(start: -24h)
    |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
    |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
    |> schema.fieldsAsCols()
    |> yield(name: "mean")`;

// Query for Daily Traffic
const query_daily_traffic = `import "influxdata/influxdb/schema"
from(bucket: "daily_interface_data")
  |> range(start: -30d)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")`

// Query for Monthly Traffic
const query_monthly_traffic = `import "influxdata/influxdb/schema"
from(bucket: "monthly_interface_data")
  |> range(start: -1y)
  |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
  |> aggregateWindow(every: 30d, fn: mean, createEmpty: false)
  |> schema.fieldsAsCols()
  |> yield(name: "mean")`

// Query for Connected Clients
const query_connected_clients = `import "influxdata/influxdb/schema"
import "sampledata"
from(bucket: "connected_clients")
  |> range(start: -12h, stop: 12h)
  |> filter(fn: (r) => r["_measurement"] == "Connected-Clients")
  |> aggregateWindow(every: 30s, fn: last, createEmpty: false)
  |> schema.fieldsAsCols()
  |> sort(columns: ["IP"])
  |> yield(name: "first")`;

const query_tcp_endpoint = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -30m)
  |> filter(fn: (r) => r["_measurement"] == "tcp_endpoint")
  |> schema.fieldsAsCols()`;