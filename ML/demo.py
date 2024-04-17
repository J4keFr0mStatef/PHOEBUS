from PacketReader import SessionTracker
from scapy.all import sniff, TCP, IP
import pickle
import sklearn
import pandas as pd
import time
import os


STARTTIME = str(time.time())
DEBUG = True

print('Demo starting')

# unpickle model.pkl
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

print('Model loaded')

#define a callback function for the session tracker
def predict(features, packets):
    for key, value in features.items():
                print(f"{key}: {value}")

    print("---------------------------------\n")

    #predict the class of the connection
    features.pop("num_packets")
    prediction = model.predict(pd.DataFrame([features]))

    if prediction == 1:
        prediction = "Malicious"
    elif prediction == 0:
        prediction = "Benign"
    else:
        prediction = "Unknown"

    print(f"Prediction: {prediction}")
    print("\n\n")

#store the features and packets in a file for debugging
def storePredict(features, packets):
    if not os.path.exists('exclude'):
        os.makedirs('exclude')

    with open(f'{os.path.join("exclude",STARTTIME)}.txt', 'a') as f:
    
        for key, value in features.items():
            f.write(f"{key}: {value} \n")

        f.write("---------------------------------\n\n")

        #predict the class of the connection
        features.pop("num_packets")
        prediction = model.predict(pd.DataFrame([features]))

        if prediction == 1:
            prediction = "Malicious"
        elif prediction == 0:
            prediction = "Benign"
        else:
            prediction = "Unknown"

        f.write(f"Prediction: {prediction}\n")
        
        f.write("---------------------------------\n\n")
        
        #print out the packets
        
        for p in range(len(packets)):
            f.write(f'Packet #{p}: ts:{packets[p].time}src:{packets[p][IP].src} dst:{packets[p][IP].dst} srcp:{packets[p][IP].sport} dstp:{packets[p][IP].dport} flags:{packets[p][TCP].flags} \n')
        
        f.write(f"\n\n\n")

#instantiating the session tracker
if DEBUG:
     cbfunct = storePredict
else:
     cbfunct = predict

tracker = SessionTracker(cbfunct)

print('Sniffing starting...\n\n')

#start sniffing packets
sniff(iface="enp0s3",filter="tcp", prn=lambda x: tracker.add_packet(x))
