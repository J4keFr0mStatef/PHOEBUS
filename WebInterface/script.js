function addData(chart, label, newData) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        if (newData.hasOwnProperty(dataset.label)) {
            dataset.data.push(newData[dataset.label]);
        }
    });
    chart.update();
}

function removeOldestData(chart) {
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
    chart.update();
}

// Update chart with new random value
function updateChartNT(chart) {
    addData(chart, 'May 10', {'Network Traffic Out (MB)':~~(Math.random()*51), 'Network Traffic In (MB)':~~(Math.random()*51)});
    removeOldestData(chart);
    setTimeout(function(){updateChartNT(chart)},10000);
}

function createChartNT(info, type) {
    // Grab html element to place chart inside
    const ntChart = document.getElementById('networkTraffic');

    // Loop through data
    let eth0Data = [];
    let wlan0Data = [];
    let wlan1Data = [];
    let labels = [];
    for (var i = 0; i < info.data.length - 2; i++) {
        if (info.data[i]["interface"] == "eth0") {
            eth0Data.push(info.data[i]["total_bytes"] / (1024 * 1024));
            labels.push(info.data[i][type]);
        } else if (info.data[i]["interface"] == "wlan0") {
            wlan0Data.push(info.data[i]["total_bytes"] / (1024 * 1024));
        } else if (info.data[i]["interface"] == "wlan1") {
            wlan1Data.push(info.data[i]["total_bytes"] / (1024 * 1024));
        }
    }

    // Create data object for chart
    let data = {
        labels: labels,
        datasets: [{
            label: 'Eth0 Data (MB)',
            data: eth0Data
        },{
            label: 'Wlan0 Data (MB)',
            data: wlan0Data
        },{
            label: 'Wlan1 Data (MB)',
            data: wlan1Data
        }]
    };

    // Set config for chart
    let config = {
        type: 'line',
        data: data,
        options: {},
    };

    // Generate chart within html element
    let chartObj = new Chart(ntChart, config);
}

function populateTable(data) {

    var devicesTable = document.getElementById("devicesTable");
    
    for (var i = 0; i < data.data.length - 2; i++) {
        var row = devicesTable.insertRow(i + 1);
        var cell = row.insertCell(0);
        cell.innerHTML = data.data[i]["IP"];
        cell = row.insertCell(1);
        cell.innerHTML = data.data[i]["MAC Address"];
        cell = row.insertCell(2);
        cell.innerHTML = data.data[i]["Hostname"];
    }
}