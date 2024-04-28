<!DOCTYPE html>
<?php
$env = parse_ini_file('/etc/phoebus/.env');
$token = $env['INFLUXDB_TOKEN'];
?>
<html>
<head>
    <title>Device Analytics</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<script>
    function redirect(page) {
        window.location.replace(page);
    };
    function infoOn(ID) {
        document.getElementById(ID).style.display = "block";
    };
    function infoOff(ID) {
        document.getElementById(ID).style.display = "none";
    };
</script>

<body>
    <script src="papaparse.min.js"></script>
    <script src="query.js"></script>

    <h1>Machine Learning</h1>
    <div class="container">
        <p>This is the machine learning page! Here you can see the data that has been returned by the random forest classification model.</p>
        <button class="home" onclick="redirect('/routes/ap-analytics/index.html')">Go to Home</button>
    </div>


    <div class="container">
        <div id="machineLearning">
            <div id="machineLearningHeader">
                <h2>Malicious Sessions
                    <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Sessions')" />
                </h2>
                <script src="switch.js"></script>
                <button id="switch-mal-ben">Switch to Benign Sessions</button>
            </div>
            <div class="tableFixHead">
                <table id="machineLearningTable">
                    <thead>
                        <tr>
                            <th>Source IP
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('source_ip')" />
                            </th>
                            <th>Source Port
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('source_port')" />
                            </th>
                            <th>Destination IP
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('destination_ip')" />
                            </th>
                            <th>Destination Port
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('destination_port')" />
                            </th>
                            <th>Flow Duration
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('flow_duration')" />
                            </th>
                            <th># of Packets
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('number_of_packets')" />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
        
    <script src="script.js"></script>
    <script>
        // Create thrg, token, query_tcp_endpoints).then(data e connected clients table
        const token = <?php echo $token?>;
        query(,);
    </script>
</body>
</html>