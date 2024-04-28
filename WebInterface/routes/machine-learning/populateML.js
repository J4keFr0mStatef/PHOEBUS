
const MLtableID = "machineLearningTable";
const MLheaderLabels = ['_time', 'source_ip', 'source_port','destination_ip', 'destination_port','flow_duration', 'number_of_packets'];



function updateTable(data) {
    //wipe the table
    //populate the table again
    
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