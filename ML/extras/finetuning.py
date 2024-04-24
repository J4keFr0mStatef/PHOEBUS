from PacketReader import SessionTracker
from scapy.all import sniff, TCP, IP
import pickle
import pandas as pd
import time
import os

os.chdir('..')
STARTTIME = str(time.time()).replace('.', '')

FEATURES = [
    "mean_TCP_windows_size_value",
    "Source_port",
    "max_Interval_of_arrival_time_of_forward_traffic",
    "max_Interval_of_arrival_time_of_backward_traffic",
    "flow duration",
    "std_Interval_of_arrival_time_of_backward_traffic",
    "Total_length_of_forward_payload",
    "std_Length_of_IP_packets",
    "max_Time_difference_between_packets_per_session",
    "std_forward_pkt_length",
    "max_Length_of_TCP_payload",
    "mean_time_to_live",
    "std_time_to_live",
    "duration_forward"
]

#collects data from scapy and stores it into a csv file
def collect(features):
    if not os.path.exists('exclude'):
        os.makedirs('exclude')

    #create a csv file for the data if it doesn't exist
    if not os.path.exists(f'exclude/finetuning_data{STARTTIME}.csv'):
        with open(f'exclude/finetuning_data{STARTTIME}.csv', 'w') as f:
            #write the features as the header
            f.write(','.join(FEATURES) + '\n')

        print('File created')

    #write the features to the csv file
    with open(f'exclude/finetuning_data{STARTTIME}.csv', 'a+') as f:
        f.write(','.join([str(features[feat]) for feat in FEATURES]) + '\n')

        #print the row number written
        f.seek(0)
        print(f'Row {len(f.readlines())-1} written')

#instantiating the session tracker
tracker = SessionTracker(lambda features, packets, metadata : collect(features))

print('Sniffing starting...')

sniff(iface="enp0s3", filter="tcp", prn=lambda x: tracker.add_packet(x))