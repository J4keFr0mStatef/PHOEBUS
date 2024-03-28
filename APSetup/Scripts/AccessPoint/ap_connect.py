from APSetup.Scripts.AccessPoint.ap_scan import get_aps, clean_data, table_output
import json

filename = "TestData/AP_Scan/test_data.txt"

def connect(data):
    with open(f"{data['SSID']}.conf", "w") as f:
        if data['Authentication'] == "PSK":
            password = input("Enter the password: ")

            # read wpa_psk_template in as json
            with open("../Files/etc/wpa_supplicant/wpa_psk_template.conf", "r") as template:
                output = ""
                for line in template:
                    if "ssid" in line:
                        output += f"\tssid=\"{data['SSID']}\"\n"
                    elif "key_mgmt" in line:
                        output += f"\tkey_mgmt=WPA-PSK\n"
                    elif "psk" in line:
                        output += f"\tpsk=\"{password}\"\n"
                    else:
                        output += line
            
                template.close()
                
            f.write(output)

        elif data['Authentication'] == "802.1x":

            username = input("Enter the username: ")
            password = input("Enter the password: ")

            # read wpa_eap_template in as json
            with open("../Files/etc/wpa_supplicant/wpa_enterprise_template.conf", "r") as template:
                output = ""
                for line in template:
                    if "ssid=\"" in line:
                        output += f"\tssid=\"{data['SSID']}\"\n"
                    elif "key_mgmt" in line:
                        output += f"\tkey_mgmt=WPA-EAP\n"
                    elif "identity" in line:
                        output += f"\tidentity=\"{username}\"\n"
                    elif "password" in line:
                        output += f"\tpassword=\"{password}\"\n"
                    else:
                        output += line

                template.close()

            f.write(output)

        f.close()
    


data = clean_data(get_aps(filename))

table_output(data)

ap_num = int(input("\nChoose an Access Point to connect to: ")) - 1 
key = list(data.keys())[ap_num]
ap = data[key]

print(f"\nConnecting to {ap['SSID']}")

connect(ap)

