<?php
$env = parse_ini_file('/etc/phoebus/.env');
$token = $env['INFLUXDB_TOKEN'];
echo $token;
?>