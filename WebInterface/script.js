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

function createChartNT() {
    // Grab html element to place chart inside
    const ntChart = document.getElementById('networkTraffic');

    // Generate random data
    let randDataIn = [...Array(10)].map(e=>~~(Math.random()*51));
    let randDataOut = [...Array(10)].map(e=>~~(Math.random()*51));
    // Generate dummy labels
    let labels = [...Array(10).keys()].map(i=>'May '+(i+1));

    // Create data object for chart
    let data = {
        labels: labels,
        datasets: [{
            label: 'Network Traffic Out (MB)',
            data: randDataIn
        },{
            label: 'Network Traffic In (MB)',
            data: randDataOut
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

    // Update chart continually
    updateChartNT(chartObj);
}

createChartNT();