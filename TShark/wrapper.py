import json

# Read the text from the file
with open('tshark_outputs/open_ports.txt', 'r') as file:
    ports_text = file.read()

# Split the ports into a list
ports_list = ports_text.split()

# Create a dictionary to store the ports
ports_dict = {'open_ports': ports_list}

# Write the dictionary to a JSON file
with open('open_ports.json', 'w') as file:
    json.dump(ports_dict, file)