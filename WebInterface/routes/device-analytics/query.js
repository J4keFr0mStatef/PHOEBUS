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

const query_tcp_endpoints = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "tcp_endpoint")
  |> schema.fieldsAsCols()`;