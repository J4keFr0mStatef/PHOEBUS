from PacketReader import SessionTracker
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write.point import Point
from scapy.all import sniff
import pickle
import pandas as pd
import logging
import os

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
            "prediction" : bool(prediction),
            "flow_duration" : float(features["flow duration"]),
            "number_of_packets" : int(features["num_packets"])
        }   
    }

    point = Point.from_dict(datadict)
    bucket = "ML_data"
    org = "PHOEBUS"
    
    write_api.write(bucket=bucket, org=org, record=point)

def predict(features, packets, write_api):
    '''
    Predicts the class of the session and calls the logging and writing functions
    '''

    #predict the class of the connection
    num_packets = features.pop("num_packets")
    prediction = model.predict(pd.DataFrame([features]))
    features["num_packets"] = num_packets

    logSession(features, prediction)

    #only write to the database if the prediction is malicious
    if(prediction == 1):
        writeDB(features, prediction, write_api)

##############
# Main script

#setup logging
logging.basicConfig(level=logging.INFO)
logging.info('MLwriter service starting')

#unpickle model.pkl
with open('/home/admin/SeniorDesign/ML/model.pkl', 'rb') as file:
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
    tracker = SessionTracker(lambda features, packets, metadata: predict(features, packets, metadata, write_api))

    #start sniffing packets
    logging.info('Sniffing starting...')
    sniff(iface="eth0",filter="tcp", prn=lambda x: tracker.add_packet(x))
