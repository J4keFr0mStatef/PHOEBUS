from ap_scan import get_aps, clean_data, table_output
import os
import json

directory = "../../Files/etc/wpa_supplicant/"
ap_data_file = "../TestData/AP_Scan/test_data.txt"

def connect(data):
    conf_file = directory + f"{data['SSID']}.conf"
    with open(conf_file, "w") as f:
        try:
            if data['Authentication'] == "PSK":
                while True:
                    invalid_chars = ["\"", "\\", "\n", "\t", "]", "\'", "[", "{", "}", "|", "(", ")", ";", ":"]
                    password = input("Enter the password: ")
                    if len(password) < 1:
                        print("Invalid password. Please try again.")
                    elif any(char in password for char in invalid_chars):
                        print("Invalid password. Please try again.")
                    else:
                        break

                # read wpa_psk_template in as json
                with open(directory + "wpa_psk_template.conf", "r") as template:
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
                invalid_chars = ["\"", "\\", "\n", "\t", "]", "\'", "[", "{", "}", "|", "(", ")", ";", ":"]
                while True:
                    username = input("Enter the username: ")
                    if len(username) < 1:
                        print("Invalid username. Please try again.")
                    elif any(char in username for char in invalid_chars):
                        print("Invalid username. Please try again.")
                    else:
                        break
                while True:
                    password = input("Enter the password: ")
                    if len(password) < 1:
                        print("Invalid password. Please try again.")
                    elif any(char in password for char in invalid_chars):
                        print("Invalid password. Please try again.")
                    else:
                        break

                # read wpa_eap_template in as json
                with open(directory + "wpa_enterprise_template.conf", "r") as template:
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

            else:
                with open(directory + "open_network_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid" in line:
                            output += f"\tssid=\"{data['SSID']}\"\n"
                        else:
                            output += line

                    template.close()

                f.write(output)

            f.close()
        except KeyboardInterrupt:
            f.close()
            os.remove(conf_file)
            print("\nExiting...")
            exit()
    
data = clean_data(get_aps(ap_data_file))

table_output(data)

while True:
    try: 
        ap_num = int(input("\nChoose an Access Point to connect to: ")) - 1

        if ap_num < 0:
            print("Invalid Access Point")
            continue
        else:
            key = list(data.keys())[ap_num]
            ap = data[key]
            print(f"\nConnecting to {ap['SSID']}")
            connect(ap)
            print(f"Connected to {ap['SSID']}")
            exit()

    except (IndexError, ValueError):
        print("Invalid Access Point")

