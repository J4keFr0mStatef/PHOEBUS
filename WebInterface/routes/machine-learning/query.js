const org = "PHOEBUS";

function query(org, viewMalicious) {

    var query_data = `
    from(bucket: "${viewMalicious ? 'ML_malicious' : 'ML_benign'}")
      |> range(start: -30m)
      |> filter(fn: (r) => r["_measurement"] == "session")
      |> filter(fn: (r) => r["_field"] == "flow_duration" or r["_field"] == "number_of_packets")
      |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> group(columns:[])`;

    const options = {
        method: 'POST',
        body: query_data,
        headers: {
          'Content-Type': 'application/vnd.flux',
          'Authorization': `Token ${MLtoken}`,
          'Accept': 'application/csv'
        }
    }

    var data = fetch(`http://${location.host}:8086/api/v2/query?org=${org}`, options)
    .then(response => response.text())
    .then(text => {Papa.parse(text, { header: true }) })
    .then(val => console.log(val));

    return data;
  }