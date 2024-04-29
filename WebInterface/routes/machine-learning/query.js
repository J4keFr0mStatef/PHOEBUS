const org = "PHOEBUS";
const MLtoken = "0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw==";

function query(org, viewMalicious) {

    if (viewMalicious == 1) {
      var query_data = `from(bucket: "ML_malicious")
      |> range(start: -30m)
      |> filter(fn: (r) => r["_measurement"] == "session")
      |> filter(fn: (r) => r["_field"] == "flow_duration" or r["_field"] == "number_of_packets")
      |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> group(columns:[])
      |> yield()`;
    } else {
      var query_data = `from(bucket: "ML_benign")
      |> range(start: -30m)
      |> filter(fn: (r) => r["_measurement"] == "session")
      |> filter(fn: (r) => r["_field"] == "flow_duration" or r["_field"] == "number_of_packets")
      |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> group(columns:[])
      |> yield()`
    }

    const options = {
        method: 'POST',
        body: query_data,
        headers: {
          'Content-Type': 'application/vnd.flux',
          'Authorization': `Token ${MLtoken}`,
          'Accept': 'application/csv'
        }
    }

    var data = fetch(`http://10.0.1.1:8086/api/v2/query?org=${org}`, options)
    .then(response => response.text())
    .then(text => {return Papa.parse(text, { header: true }) })
    
    data.then(val => console.log(val));

    return data;
  }