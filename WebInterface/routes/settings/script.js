function infoOn(ID) {
    document.getElementById(ID).style.display = "block";
};
function infoOff(ID) {
    document.getElementById(ID).style.display = "none";
};

function resetSettings() {
    document.getElementById("dns1").value = "1.1.1.1";
    document.getElementById("dns2").value = "8.8.8.8";
    document.getElementById("dhcp_auth_on").checked = true;
    document.getElementById("dhcp_seq_on").checked = true;

    document.getElementById("eth0_start").value = "192.168.1.5";
    document.getElementById("eth0_end").value = "192.168.1.254";
    document.getElementById("eth0_mask").value = "255.255.255.0";
    document.getElementById("eth0_router").value = "192.168.1.1";
    document.getElementById("eth0_wan_off").checked = true;

    document.getElementById("wlan0_start").value = "10.0.0.5";
    document.getElementById("wlan0_end").value = "10.0.0.254";
    document.getElementById("wlan0_mask").value = "255.255.255.0";
    document.getElementById("wlan0_router").value = "10.0.0.1";
    document.getElementById("wlan0_wan_on").checked = true;
    document.getElementById("wlan0_ssid").value = "Phoebus";
    document.getElementById("wlan0_auth_method").value = "PSK";
    document.getElementById("wlan0_passwd").value = "password123";

    document.getElementById("wlan1_start").value = "10.0.1.5";
    document.getElementById("wlan1_end").value = "10.0.1.254";
    document.getElementById("wlan1_mask").value = "255.255.255.0";
    document.getElementById("wlan1_router").value = "10.0.1.1";
    document.getElementById("wlan1_wan_off").checked = true;
    document.getElementById("wlan1_ssid").value = "Phoebus";
    document.getElementById("wlan1_auth_method").value = "PSK";
    document.getElementById("wlan1_passwd").value = "password123";
};