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

    var data = fetch(`http://192.168.1.1:8086/api/v2/query?org=${org}`, options)
        .then(response => response.text())
        .then(text => { return Papa.parse(text, { header: true }) });

    data.then(val => console.log(val));

    return data;
}

const org = "PHOEBUS";
const token = "0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw==";

const query_tcp_endpoints = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "tcp_endpoint")
  |> schema.fieldsAsCols()`;

const query_host_info = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "ip_address")
  |> schema.fieldsAsCols()`;
  
const query_ports_info = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -10m)
  |> filter(fn: (r) => r["_measurement"] == "open_port")
  |> filter(fn: (r) => r["status"] == "normal" or r["status"] == "privileged" or r["status"] == "warning")
  |> schema.fieldsAsCols()
  |> group()`;

const query_user_agent_info = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "useragent_warning")
  |> schema.fieldsAsCols()`;