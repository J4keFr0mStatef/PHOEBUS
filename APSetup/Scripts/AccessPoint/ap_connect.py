from ap_scan import get_aps, clean_data, table_output
import os, subprocess
import json

pi_wpa_directory = "/etc/wpa_supplicant/"
pi_wpa_template_dir = "/etc/phoebus/data/wpa_supplicant/"
pi_ap_data_file = "/etc/phoebus/data/AP_Scan/data.txt"

project_directory = "../../Files/etc/wpa_supplicant/"
ap_data_file = "../TestData/AP_Scan/test_data.txt"

def connect(data):
    filename = f"{data['SSID']}.conf"
    out_file = pi_wpa_directory + filename

    with open(out_file, "w") as f:
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

                with open(pi_wpa_template_dir + "wpa_psk_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid=\"" in line:
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

                with open(pi_wpa_template_dir + "wpa_enterprise_template.conf", "r") as template:
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
                with open(pi_wpa_template_dir + "open_network_template.conf", "r") as template:
                    output = ""
                    for line in template:
                        if "ssid=\"" in line:
                            output += f"\tssid=\"{data['SSID']}\"\n"
                        else:
                            output += line

                    template.close()

                f.write(output)

            f.close()

            return out_file

        except KeyboardInterrupt:
            f.close()
            os.remove(out_file)
            print("\nExiting...")
            exit()

def update_interfaces(filename):
    interfaces = subprocess.run("ls /sys/class/net", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

    path = "/etc/network/interfaces.d/"

    if "wlan0" in interfaces:
        with open(path + "wlan0", "w") as file:
            file.write("auto wlan0\n")
            file.write("iface wlan0 inet dhcp\n")
            file.write(f"\twpa-conf {filename}\n")

    ifdown = subprocess.run("sudo ifdown wlan0", shell=True, stderr=subprocess.PIPE)
    ifup = subprocess.run("sudo ifup wlan0", shell=True, stderr=subprocess.PIPE)

    ifup_error = ifup.stderr.decode("utf-8")

    if "failed to bring up" in ifup_error:
        print("Invalid password")
        return False
    else:
        print(ifup_error)
        return True
    
def main():
    data = clean_data(get_aps(ap_data_file))

    table_output(data)

    picked_ap = False
    while True:
        try:
            if not picked_ap: 
                ap_num = int(input("\nChoose an Access Point to connect to: ")) - 1
                picked_ap = True
                
            if ap_num < 0:
                print("Invalid Access Point")
                picked_ap = False

            else:
                key = list(data.keys())[ap_num]
                ap = data[key]
                out_file = connect(ap)
                print(f"\nConnecting to {ap['SSID']}")
                connected = update_interfaces(out_file)

                if connected:
                    print(f"Connected!")
                    exit()

        except (IndexError, ValueError):
            print("Invalid Access Point")
            picked_ap = False

if __name__ == "__main__":
    main()

