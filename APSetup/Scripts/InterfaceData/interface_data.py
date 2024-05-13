import json

def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576

    return '{0:.2f}'.format(B / MB)

data = json.load(open('../TestData/InterfaceData/vnstat_data.json'))

output = {}

for interface in data['interfaces']:
    output[interface['name']] = {}
    for entry in interface['traffic']['hour']:
        output[interface['name']][entry['time']['hour']] = {
            'rx': humanbytes(entry['rx']),
            'tx': humanbytes(entry['tx'])
        }

print(output)
json.dump(output, open('../TestData/InterfaceData/vnstat_data_cleaned.json', 'w'), indent=4)