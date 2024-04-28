var viewMalicious = true;

document.getElementById("switch-mal-ben").addEventListener("click", function() {
    viewMalicious = !viewMalicious;
    this.textContent = viewMalicious ? 'Switch to benign sessions' : 'Switch to malicious sessions';
    
    //also change the text contents of the header in the same div as the button
    var header = document.getElementById("machineLearningHeader");
    header.textContent = viewMalicious ? 'Malicious Sessions' : 'Benign Sessions';

    var Jdata = query(org,1);
    //call the function to update the chart
    updateTable(Jdata, MLtableID, ['_time', 'flow_duration', 'number_of_packets'])
    //call the function to update the table
    //query...
});