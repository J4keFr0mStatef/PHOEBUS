function updateChart(chart, rawData, type) {
    newData = getData(rawData, type)
    chart.data = newData;
    chart.update();
}

function getData(rawData, type) {
    let eth0Data = [];
    let wlan0Data = [];
    let wlan1Data = [];
    let labels = [];
    for (var i = 0; i < rawData.data.length - 2; i++) {
        if (rawData.data[i]["interface"] == "eth0") {
            eth0Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
            labels.push(rawData.data[i][type]);
        } else if (rawData.data[i]["interface"] == "wlan0") {
            wlan0Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
        } else if (rawData.data[i]["interface"] == "wlan1") {
            wlan1Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
        }
    }

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

    return data

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
    
    console.log(chartObj);

    return chartObj;
}

function populateTable(data, id, headerLabels) {

    var table = document.getElementById(id).getElementsByTagName('tbody')[0];
    
    for (var i = 0; i < data.data.length - 2; i++) {
        var row = table.insertRow(i);
        for (var j = 0; j < headerLabels.length; j++) {
            var cell = row.insertCell(j);
            cell.innerHTML = data.data[i][headerLabels[j]];
        }
    }
}