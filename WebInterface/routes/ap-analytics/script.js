function updateChart(chart, rawData, type) {
    newData = getData(rawData, type);
    chart.data = newData;
    
    newConfig = getConfig(type, newData);

    chart.options = newConfig.options;
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
            if (type == "minute") {
                if (parseInt(rawData.data[i]['minute']) < 10) {
                    labels.push(((parseInt(rawData.data[i]['hour']) + 18) % 24) + ":0" + rawData.data[i]['minute']);
                } else {
                    labels.push(((parseInt(rawData.data[i]['hour']) + 18) % 24) + ":" + rawData.data[i][type]);
                }
            } else if (type == "hour") {
                labels.push((parseInt(rawData.data[i][type]) + 18) % 24);
            }
            else {
                labels.push(rawData.data[i][type]);
            }
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

function getConfig(type, data) {

    if (type == "minute") {
        var config = {
            type: 'line',
            data: data,
            options: {
                    scales: {
                            x: {
                            title: {
                                    display: true,
                                    text: "Time (min)"
                            }
                            },
                            y: {
                            title: {
                                    display: true,
                                    text: "Data Transfered (MiB)"
                            }
                            }
                    }
            },
        };
    } else if (type == "hour") {

        var config = {
            type: 'line',
            data: data,
            options: {
                    scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: "Time (hr)"
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: "Data Transfered (MiB)"
                                }
                            }
                    }
            },
        };
    } else if (type == "day") {

        var config = {
            type: 'line',
            data: data,
            options: {
                    scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: "Day"
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: "Data Transfered (MiB)"
                                }
                            }
                    }
            },
        };
    } else if (type == "month") {
        var config = {
            type: 'line',
            data: data,
            options: {
                    scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: "Month"
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: "Data Transfered (MiB)"
                                }
                            }
                    }
            },
        };
    }

    return config;
}

function createChartNT(rawData, type) {
    // Grab html element to place chart inside
    const ntChart = document.getElementById('networkTraffic');

    // Loop through data
    let eth0Data = [];
    let wlan0Data = [];
    let wlan1Data = [];
    let labels = [];
    for (var i = 0; i < rawData.data.length - 2; i++) {
        if (rawData.data[i]["interface"] == "eth0") {
            eth0Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
            if (type == "minute") {
                if (parseInt(rawData.data[i]['minute']) < 10) {
                    labels.push(((parseInt(rawData.data[i]['hour']) + 18) % 24) + ":0" + rawData.data[i]['minute']);
                } else {
                    labels.push(((parseInt(rawData.data[i]['hour']) + 18) % 24) + ":" + rawData.data[i][type]);
                }
            } else if (type == "hour") {
                labels.push((parseInt(rawData.data[i][type]) + 18) % 24);
            }
            else {
                labels.push(rawData.data[i][type]);
            }
        } else if (rawData.data[i]["interface"] == "wlan0") {
            wlan0Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
        } else if (rawData.data[i]["interface"] == "wlan1") {
            wlan1Data.push(rawData.data[i]["total_bytes"] / (1024 * 1024));
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
        options: {
                scales: {
                        x: {
                          title: {
                                display: true,
                                text: "Time (min)"
                          }
                        },
                        y: {
                          title: {
                                display: true,
                                text: "Data Transfered (MiB)"
                          }
                        }
                }
        },
    };

    // Generate chart within html element
    let chartObj = new Chart(ntChart, config);
    
    console.log(chartObj);

    return chartObj;
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