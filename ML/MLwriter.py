from PacketReader import SessionTracker
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write.point import Point
from scapy.all import sniff
import pickle
import pandas as pd
import logging
import os

INTERFACE = "wlan0"

def logSession(features, prediction):
    '''
    Logs the output of the model and the features of the session
    '''
    #convert the prediction to a string
    if prediction == 1:
        prediction = "Malicious"
    elif prediction == 0:
        prediction = "Benign"
    else:
        prediction = "Unknown"

    #build info string
    info_str = f'Prediction: {prediction}\n'
    for key, value in features.items():
                info_str += f"{key}: {value}\n"

    #log the output
    logging.info(info_str)

def writeDB(features, prediction, metadata, write_api):
    '''
    Writes the features and prediction to the InfluxDB
    '''

    #create a new point
    datadict = {
        "measurement" : "session",
        "tags" : {
            "source_ip": str(metadata["src_ip"]),
            "destination_ip": str(metadata["dest_ip"]),
            "source_port": int(metadata["src_port"]),
            "destination_port": int(metadata["dest_port"])
        },
        "fields" : {
            "flow_duration" : float(features["flow duration"]),
            "number_of_packets" : float(features["num_packets"])
        }   
    }

    point = Point.from_dict(datadict)

    if(prediction == 1):
         bucket = "ML_malicious"
    else:
         bucket = "ML_benign"

    org = "PHOEBUS"
    
    write_api.write(bucket=bucket, org=org, record=point)

def predict(features, metadata, write_api):
    '''
    Predicts the class of the session and calls the logging and writing functions
    '''

    #predict the class of the connection
    num_packets = features.pop("num_packets")
    prediction = model.predict(pd.DataFrame([features]))
    features["num_packets"] = num_packets

    #log the output
    logSession(features, prediction)

    #write to the database
    writeDB(features, prediction, metadata, write_api)

##############
# Main script

#setup logging
logging.basicConfig(level=logging.INFO)
logging.info('MLwriter service starting')

#unpickle model.pkl
with open('/etc/phoebus/ML/model.pkl', 'rb') as file:
    model = pickle.load(file)
logging.info('Model loaded')

#connect to InfluxDB
token = os.environ.get("INFLUXDB_TOKEN")
org = "PHOEBUS"
url = "http://localhost:8086"

with InfluxDBClient(url=url, token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    logging.info('Connected to InfluxDB')

    #create the session tracker, passing write_api back to the predict function
    tracker = SessionTracker(lambda features, packets, metadata: predict(features, metadata, write_api))

    #start sniffing packets
    logging.info(f'Sniffing starting on interface {INTERFACE}...')
    sniff(iface=INTERFACE,filter="tcp", prn=lambda x: tracker.add_packet(x))
