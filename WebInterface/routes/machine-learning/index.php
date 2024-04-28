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

    <!-- Info button descriptions -->
    <div id="Source-IP" class="overlay" onclick="infoOff('Source-IP')">
        <div class="overlay-text">
        An IP Address is given to each device on your network to allow services within and outside your network to reach them. <br>
        This is the IP address of the device that initiated the connection.
        </div>
    </div>

    <div id="Source-Port" class="overlay" onclick="infoOff('Source-Port')">
        <div class="overlay-text">
        A port is a communication endpoint that allows a device to send and receive data. <br>
        Think of it as a mailbox, where the IP address is the street address and the port is the mailbox number. <br>
        This is the Port of the device that initiated the connection
        </div>
    </div>

    <div id="Destination-IP" class="overlay" onclick="infoOff('MAC-info')">
        <div class="overlay-text">
        An IP Address is given to each device on your network to allow services within and outside your network to reach them. <br>
        This is the IP address of the device that the connection was made to.
        </div>
    </div>

    <div id="Destination-Port" class="overlay" onclick="infoOff('Destination-Port')">
        <div class="overlay-text">
        A port is a communication endpoint that allows a device to send and receive data. <br>
        Think of it as a mailbox, where the IP address is the street address and the port is the mailbox number. <br>
        This is the Port of the device that the connection was made to.
        </div>
    </div>

    <div id="Session-Duration" class="overlay" onclick="infoOff('Session-Duration')">
        <div class="overlay-text">
        A session is a period of time where a connection is open between two devices. <br>
        Each session is tested by the machine learning model to determine if it is malicious or benign. <br>
        This is the duration of the session in seconds.
        </div>
    </div>

    <div id="Number-Of-Packets" class="overlay" onclick="infoOff('Number-Of-Packets')">
        <div class="overlay-text">
        A packet is a unit of data that is sent between devices. <br>
        A session is made up of multiple packets. <br>
        This is the number of packets that were sent during the session.
        </div>
    </div>
    
    <div id="Session-Timestamp" class="overlay" onclick="infoOff('Session-Timestamp')">
        <div class="overlay-text">
        A timestamp is a record of the date and time that an event occurred. <br>
        This is the date and time that the machine learning model completed its prediction for the session.
        </div>
    </div>


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
                            <th>Session Timestamp
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Session-Timestamp')" />
                            </th>
                            <th>Source IP
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Source-IP')" />
                            </th>
                            <th>Source Port
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Source-Port')" />
                            </th>
                            <th>Destination IP
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Destination-IP')" />
                            </th>
                            <th>Destination Port
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Destination-Port')" />
                            </th>
                            <th>Session Duration
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Session-Duration')" />
                            </th>
                            <th># of Packets
                                <input class="info" type="image" src="/images/info.png" alt="info" onclick="infoOn('Number-Of-Packets')" />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
        
    <script src="switch.js"></script>
    <script src="populateML.js"></script>
    <script>
        // Create thrg, token, query_tcp_endpoints).then(data e connected clients table
        const MLtoken = <?php echo $token?>;
        var Jdata = query(org,1).then(populateML(Jdata, MLtoken, MLheaderLabels));
    </script>
</body>
</html>