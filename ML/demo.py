from PacketReader import SessionTracker
from scapy.all import sniff, TCP, IP
import pickle
import sklearn
import pandas as pd

print('Demo starting')

# unpickle model.pkl
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

print('Model loaded')

#define a callback function for the session tracker
def predict(features):
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

#instantiating the session tracker
tracker = SessionTracker(predict)

print('Sniffing starting...\n\n')

#start sniffing packets
sniff(iface="eth0",filter="tcp", prn=lambda x: tracker.add_packet(x))
