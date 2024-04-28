var viewMalicious = true;

document.getElementById("switch-mal-ben").addEventListener("click", function() {
    viewMalicious = !viewMalicious;
    this.textContent = viewMalicious ? 'Switch to benign sessions' : 'Switch to malicious sessions';
    
    //also change the text contents of the header in the same div as the button
    var header = document.getElementById("machineLearningHeader");
    header.textContent = viewMalicious ? 'Malicious Sessions' : 'Benign Sessions';

    //query the data again, repopulate the table
    query(org, viewMalicious).then(data => {updateTable(data, MLtableID,MLheaderLabels)});

});