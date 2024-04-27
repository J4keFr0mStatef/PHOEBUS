<?php
$env = parse_ini_file('/etc/phoebus/.env');
$token = $env['ML_Token'];
echo $token;
?>