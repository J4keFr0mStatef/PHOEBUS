function query(org, token, query_data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `http://phoebus:8086/api/v2/query?org=${org}`);
    xhr.setRequestHeader("Authorization", `Token ${token}`);
    xhr.setRequestHeader("Content-Type", "application/vnd.flux")
    xhr.setRequestHeader("Accept", "application/csv")

    xhr.onload = () => {
        console.log(xhr.responseText);
    };
    xhr.send(query_data);
}

const org = "PHOEBUS";
const token = "aBS4lFVpEsfAu-wpAUZeuLBMBR6UJSJadTexlCQVjAOHRnK6eM_GgFWdXdECffpdn1C01Rcjff4xN6oAI-wr8A==";
const query_data = `import "influxdata/influxdb/schema"
    from(bucket: "hourly_data")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "Interface-Data")
        |> filter(fn: (r) => r["Timeframe"] == "hour")
        |> filter(fn: (r) => r["interface"] == "eth0" or r["interface"] == "wlan0" or r["interface"] == "wlan1")
        |> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
        |> schema.fieldsAsCols()
        |> yield(name: "mean")`;

query(org, token, query_data);