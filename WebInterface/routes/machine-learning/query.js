
var token;
const org = "PHOEBUS";
const query_malicious_ML = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "tcp_endpoint")
  |> schema.fieldsAsCols()`;

const query_benign_ML = `import "influxdata/influxdb/schema"
from(bucket: "tshark_analytics")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "tcp_endpoint")
  |> schema.fieldsAsCols()`;


function getToken() {
  if(!token) {
    fetch('get-ML-Token.php')
      .then(response => response.text())
      .then(t => {
        token = t;
        return token;
      });
  } else {
    return Promise.resolve(token);
  }
}

function query(org, query_type) {
  return getToken().then(token => {
    var query_data;
    if(query_type === "malicious") {
      var query_data = query_malicious_ML;
    }else{
      var query_data = query_benign_ML;
    }

    const options = {
        method: 'POST',
        body: query_data,
        headers: {
          'Content-Type': 'application/vnd.flux',
          'Authorization': `Token ${token}`,
          'Accept': 'application/csv'
        }
    }

  return fetch(`http://${location.host}:8086/api/v2/query?org=${org}`, options)
    .then(response => response.text())
    .then(text => { return Papa.parse(text, { header: true }) });
  });
};