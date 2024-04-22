<!DOCTYPE html>

<?php
    // DEBUG FILE LOCATION
    //$env = parse_ini_file('.\\setupVars.conf');
    $env = parse_ini_file('/etc/phoebus/setupVars.conf');
    $dns1 = $env['DNS1'];
    $dns2 = $env['DNS2'];

    //$domain = $env['DOMAIN'];
    $dhcp_auth = $env['DHCP_AUTHORITATIVE'];
    $dhcp_seq = $env['DHCP_SEQUENTIAL'];

    // interfaces
    // eth0
    $eth0_start = $env['ETH0_START'];
    $eth0_end = $env['ETH0_END'];
    $eth0_mask = $env['ETH0_MASK'];
    $eth0_router = $env['ETH0_ROUTER'];
    $eth0_mode = $env['ETH0_MODE'];

    // wlan0
    $wlan0_start = $env['WLAN0_START'];
    $wlan0_end = $env['WLAN0_END'];
    $wlan0_mask = $env['WLAN0_MASK'];
    $wlan0_router = $env['WLAN0_ROUTER'];
    $wlan0_mode = $env['WLAN0_MODE'];
    $wlan0_ssid = $env['WLAN0_SSID'];
    $wlan0_auth = $env['WLAN0_AUTHENTICATION'];
    $wlan0_passwd = $env['WLAN0_PASS'];

    // wlan1
    $wlan1_start = $env['WLAN1_START'];
    $wlan1_end = $env['WLAN1_END'];
    $wlan1_mask = $env['WLAN1_MASK'];
    $wlan1_router = $env['WLAN1_ROUTER'];
    $wlan1_mode = $env['WLAN1_MODE'];
    $wlan1_ssid = $env['WLAN1_SSID'];
    $wlan1_auth = $env['WLAN1_AUTHENTICATION'];
    $wlan1_passwd = $env['WLAN1_PASS'];

?>

<script>
    function redirect(page) {
        window.location.replace(page);
    };
</script>

<html>
<head>
    <title>Router Login</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <h1>Admin Homepage</h1>

    <div class="container">
        <h2>Router Configuration Settings</h2>
        <form action="request.php" method="post">
            <hr>
            <p>DNS 1: </p><input type="text" id="dns1" name="dns1" value="<?php echo $dns1; ?>"></br>
            <p>DNS 2: </p><input type="text" id="dns2" name="dns2" value="<?php echo $dns2; ?>"></br>
            <hr>
            <!-- <p>Domain: </p><input type="text" id="domain" name="domain" value="<?php echo $domain; ?>"></br> -->
            <p>Authoritative DHCP Server: </p>
                <input type="radio" id="dhcp_auth_on" name="dhcp_auth" value="on" <?php if ($dhcp_auth == 1) { ?> checked <?php } ?>>
                <label for="dhcp_auth_on">On</label>
                <input type="radio" id="dhcp_auth_off" name="dhcp_auth" value="off" <?php if ($dhcp_auth != 1) { ?> checked <?php } ?>>
                <label for="dhcp_auth_off">Off</label>
                </br>
            <p>DHCP Sequential IPs: </p>
                <input type="radio" id="dhcp_seq_on" name="dhcp_seq" value="on" <?php if ($dhcp_seq == 1) { ?> checked <?php } ?>>
                <label for="dhcp_seq_on">On</label>
                <input type="radio" id="dhcp_seq_off" name="dhcp_seq" value="off" <?php if ($dhcp_seq != 1) { ?> checked <?php } ?>>
                <label for="dhcp_seq_off">Off</label>
                </br>
            <hr>
            <h2>Ethernet Interface</h2>
            <p>Start Address: </p><input type="text" id="eth0_start" name="eth0_start" value="<?php echo $eth0_start; ?>"></br>
            <p>End Address: </p><input type="text" id="eth0_end" name="eth0_end" value="<?php echo $eth0_end; ?>"></br>
            <p>Mask: </p><input type="text" id="eth0_mask" name="eth0_mask" value="<?php echo $eth0_mask; ?>"></br>
            <p>Router: </p><input type="text" id="eth0_router" name="eth0_router" value="<?php echo $eth0_router; ?>"></br>
            <p>Mode: </p>
                <input type="radio" id="eth0_wan_on" name="eth0_mode" value="on" <?php if ($eth0_mode == 1) { ?> checked <?php } ?>>
                <label for="eth0_wan_on">wan</label>
                <input type="radio" id="eth0_wan_off" name="eth0_mode" value="off" <?php if ($eth0_mode != 1) { ?> checked <?php } ?>>
                <label for="eth0_wan_off">lan</label>
                </br>
            <hr>
            <h2>Wireless Interface 1</h2>
            <p>Start Address: </p><input type="text" id="wlan0_start" name="wlan0_start" value="<?php echo $wlan0_start; ?>"></br>
            <p>End Address: </p><input type="text" id="wlan0_end" name="wlan0_end" value="<?php echo $wlan0_end; ?>"></br>
            <p>Mask: </p><input type="text" id="wlan0_mask" name="wlan0_mask" value="<?php echo $wlan0_mask; ?>"></br>
            <p>Router: </p><input type="text" id="wlan0_router" name="wlan0_router" value="<?php echo $wlan0_router; ?>"></br>
            <p>Mode: </p>
                <input type="radio" id="wlan0_wan_on" name="wlan0_mode" value="on" <?php if ($wlan0_mode == 1) { ?> checked <?php } ?>>
                <label for="wlan0_wan_on">wan</label>
                <input type="radio" id="wlan0_wan_off" name="wlan0_mode" value="off" <?php if ($wlan0_mode != 1) { ?> checked <?php } ?>>
                <label for="wlan0_wan_off">lan</label>
                </br>
            <p>SSID: </p><input type="text" id="wlan0_ssid" name="wlan0_ssid" value="<?php echo $wlan0_ssid; ?>"></br>
            <p>Authentication Method: </p><input type="text" id="wlan0_auth_method" name="wlan0_auth_method" value="<?php echo $wlan0_auth; ?>"></br>
            <p>Password: </p><input type="text" id="wlan0_passwd" name="wlan0_passwd" value="<?php echo $wlan0_passwd; ?>"></br>
            <hr>
            <h2>Wireless Interface 2</h2>
            <p>Start Address: </p><input type="text" id="wlan1_start" name="wlan1_start" value="<?php echo $wlan1_start; ?>"></br>
            <p>End Address: </p><input type="text" id="wlan1_end" name="wlan1_end" value="<?php echo $wlan1_end; ?>"></br>
            <p>Mask: </p><input type="text" id="wlan1_mask" name="wlan1_mask" value="<?php echo $wlan1_mask; ?>"></br>
            <p>Router: </p><input type="text" id="wlan1_router" name="wlan1_router" value="<?php echo $wlan1_router; ?>"></br>
            <p>Mode: </p>
                <input type="radio" id="wlan1_wan_on" name="wlan1_mode" value="on" <?php if ($wlan1_mode == 1) { ?> checked <?php } ?>>
                <label for="wlan1_wan_on">wan</label>
                <input type="radio" id="wlan1_wan_off" name="wlan1_mode" value="off" <?php if ($wlan1_mode != 1) { ?> checked <?php } ?>>
                <label for="wlan1_wan_off">lan</label>
                </br>
            <p>SSID: </p><input type="text" id="wlan1_ssid" name="wlan1_ssid" value="<?php echo $wlan1_ssid; ?>"></br>
            <p>Authentication Method: </p><input type="text" id="wlan1_auth_method" name="wlan1_auth_method" value="<?php echo $wlan1_auth; ?>"></br>
            <p>Password: </p><input type="text" id="wlan1_passwd" name="wlan1_passwd" value="<?php echo $wlan1_passwd; ?>"></br>
            <hr>
            <input type="submit" value="Save Changes">
        </form>
        <button onclick="redirect('/index.php')">Go back to Home</button>
    </div>
</body>
</html>