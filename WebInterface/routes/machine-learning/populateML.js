const MLtableID = "machineLearningTable";
const MLheaderLabels = ['_time', 'source_ip', 'source_port','destination_ip', 'destination_port','flow_duration', 'number_of_packets'];


function updateTable(data, id, headerLabels) {
    //wipe the table
    var table = document.getElementById(id).getElementsByTagName('tbody')[0];
    table.innerHTML = '';
    //populate the table again
    populateTable(data, id, headerLabels);
}

function populateTable(data, id, headerLabels) {

    //sort the data first
    data.data.sort((a,b) => Date.parse(b["_time"]) - Date.parse(a["_time"]));

    var table = document.getElementById(id).getElementsByTagName('tbody')[0];
    


    for (var i = 0; i < data.data.length - 2; i++) {
        var row = table.insertRow(i);
        for (var j = 0; j < headerLabels.length; j++) {
            var cell = row.insertCell(j);
            cell.innerHTML = data.data[i][headerLabels[j]];
        }
    }
}