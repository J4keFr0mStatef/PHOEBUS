<?php
    // DEBUG FILE LOCATION
    //$outputFile = fopen('.\\setupVars.conf','w');
    
    $outputFile = fopen('/etc/phoebus/setupVars.conf','w');

    // Function to write to config file with proper formatting
    function writeConfigText($varName,$postName,$conf) {
        $temp = $_POST[$postName];
        fwrite($conf, "$varName=$temp\n");
    }
    function writeConfigRadio($varName,$postName,$conf) {
        $temp = $_POST[$postName];
        if ($temp == "on") {
            fwrite($conf, "$varName=True\n");
        } else {
            fwrite($conf, "$varName=False\n");
        }
    }

    // Put all sent data into config file
    // 'fwrite' used for hardcoding values, functions used for user input
    fwrite($outputFile, "IFACE1=eth0\n");
    fwrite($outputFile, "IFACE2=wlan0\n");
    fwrite($outputFile, "IFACE3=wlan1\n");
    writeConfigText("DNS1","dns1",$outputFile);
    writeConfigText("DNS2","dns2",$outputFile);
    writeConfigRadio("DHCP_AUTHORITATIVE","dhcp_auth",$outputFile);
    writeConfigRadio("DHCP_SEQUENTIAL","dhcp_seq",$outputFile);
    fwrite($outputFile, "DOMAIN=phoebus\n");
    fwrite($outputFile, "ETH0_SUBNET=eth0\n");
    writeConfigText("ETH0_START","eth0_start",$outputFile);
    writeConfigText("ETH0_END","eth0_end",$outputFile);
    writeConfigText("ETH0_MASK","eth0_mask",$outputFile);
    writeConfigText("ETH0_ROUTER","eth0_router",$outputFile);
    fwrite($outputFile, "ETH0_LEASE=12h\n");
    writeConfigRadio("ETH0_MODE","eth0_mode",$outputFile);
    fwrite($outputFile, "WLAN0_SUBNET=wlan0\n");
    writeConfigText("WLAN0_START","wlan0_start",$outputFile);
    writeConfigText("WLAN0_END","wlan0_end",$outputFile);
    writeConfigText("WLAN0_MASK","wlan0_mask",$outputFile);
    writeConfigText("WLAN0_ROUTER","wlan0_router",$outputFile);
    fwrite($outputFile, "WLAN0_LEASE=12h\n");
    writeConfigRadio("WLAN0_MODE","wlan0_mode",$outputFile);
    writeConfigText("WLAN0_SSID","wlan0_ssid",$outputFile);
    writeConfigText("WLAN0_AUTHENTICATION","wlan0_auth_method",$outputFile);
    writeConfigText("WLAN0_PASS","wlan0_passwd",$outputFile);
    fwrite($outputFile, "WLAN1_SUBNET=wlan1\n");
    writeConfigText("WLAN1_START","wlan1_start",$outputFile);
    writeConfigText("WLAN1_END","wlan1_end",$outputFile);
    writeConfigText("WLAN1_MASK","wlan1_mask",$outputFile);
    writeConfigText("WLAN1_ROUTER","wlan1_router",$outputFile);
    fwrite($outputFile, "WLAN1_LEASE=12h\n");
    writeConfigRadio("WLAN1_MODE","wlan1_mode",$outputFile);
    writeConfigText("WLAN1_SSID","wlan1_ssid",$outputFile);
    writeConfigText("WLAN1_AUTHENTICATION","wlan1_auth_method",$outputFile);
    writeConfigText("WLAN1_PASS","wlan1_passwd",$outputFile);

    // Close config file
    fclose($outputFile);

    // Run config update script UPDATE ON PI TO FULL PATH
    exec('sudo python3 /var/www/html/update_configs.py');

    // Redirect back to home page
    header("Location: index.php");