from scapy.all import sniff, TCP, IP
from collections import defaultdict
import time
import numpy as np
from os import environ

class SessionTracker:
    '''
    SessionTracker is a class that is used to track sessions of packets and extract their features.
    It was designed to take live packet captures from scapy.all.sniff and process them to be able to 
    use their features for machine learning. The features to be extracted was decided from the dataset
    used in the paper "Machine learning for encrypted malicious traffic detection: Approaches, datasets 
    and comparative study" by Zihao Wang, Kar Wai Fok, and Vrizlynn L.L. Thing.
    '''

    def __init__(self, cb=None):
        '''
        The constructor for the SessionTracker class. One dictionary is created to store the raw packets of 
        each session, and another dictionary is created to store the sessions that are waiting to be processed. 
        The constructor also allows for a callback function to be assigned to be passed to self.write_session.
        '''

        self.raw_sessions = defaultdict(list)
        self.callback = cb
        self.processQueue = {}

    def checkQueue(self):
        '''
        Check the session queue for each session_id and processes the session if the queue is full
        This is an attempt to catch both the server and client's FIN packets, and include them in the session
        '''

        toDelete = []
        for session_id in self.processQueue.keys():
            latest_ts = max([p.time for p in self.raw_sessions[session_id]])
            #60 second timeout
            if(time.time() - latest_ts > 60):
                self.process_session(session_id)
                toDelete.append(session_id)
        
        #after iterating
        for s in toDelete:
            del self.raw_sessions[s]
            del self.processQueue[s]

    def add_packet(self, packet):
        '''
        Adds a packet to the session tracker and processes the session if the connection is closed
        This is the method that is intended to be called by scapy.all.sniff.
        '''

        #determine the session_id
        session_id = self.assemble_session_id(packet)

        #check if this is a new session
        if "S" in packet[TCP].flags and session_id not in self.raw_sessions.keys():
            #create a new session
            self.raw_sessions[session_id] = [packet]

        #if the connection is being closed
        elif 'F' in packet[TCP].flags or 'R' in packet[TCP].flags:

            #ensure that the script wasn't ran right before the connection was closed
            if(session_id in self.raw_sessions.keys() and "S" in [p[TCP].flags for p in self.raw_sessions[session_id]]):
                
                #add the packet to the session
                self.raw_sessions[session_id].append(packet)
                
                #check to see if the packet belongs to a session that's already queued
                if not session_id in self.processQueue.keys():

                    #add the session to the process queue
                    self.processQueue[session_id] = 0

        #otherwise add the packet to the session
        else:
            self.raw_sessions[session_id].append(packet)

        self.checkQueue()

    def assemble_session_id(self, packet):
        '''
        Assembles a session_id from a packet. The session_id is a tuple of the form (src_ip, src_port, dest_ip, dest_port)
        This method ensures that the session_id is the same regardless of the direction of the traffic, so that the session
        can be uniquely identified and all of it's packets can be grouped together.
        '''

        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dest_port = packet[TCP].dport

        if src_ip < dest_ip or (src_ip == dest_ip and src_port < dest_port):
            return (src_ip, src_port, dest_ip, dest_port)
        else:
            return (dest_ip, dest_port, src_ip, src_port)

    def process_session(self, session_id):
        '''
        Processes a session once it has been considered terminated by self.checkQueue.
        This method extracts features from the session and sends them to self.write_session.

        The features extracted for the machine learning model are as follows:

            1. Mean TCP window size value
            2. Source port
            3. Max interval of arrival time of forward traffic
            4. Max interval of arrival time of backward traffic
            5. Flow duration
            6. Standard deviation of the interval of arrival time of backward traffic
            7. Total length of forward payload
            8. Standard deviation of the length of IP packets
            9. Max time difference between packets per session
           10. Standard deviation of the length of forward packets
           11. Max length of TCP payload
           12. Mean time to live
           13. Standard deviation of time to live
           14. Duration of forward traffic

        Additional metadata is also extracted from the session:

            1. Source IP
            2. Destination IP
            3. Source port
            4. Destination port
            5. Number of packets in the session
        '''

        #ensure that the packets in the session are sorted by time
        self.raw_sessions[session_id].sort(key=lambda x: x.time)

        if(len(self.raw_sessions[session_id]) != 0):

            #truncate the session to only include the first 15 packets
            if(len(self.raw_sessions[session_id]) > 15):
                all_packets = self.raw_sessions[session_id][:15]
            else:
                all_packets = self.raw_sessions[session_id]

            #check for known benign session types
            flags = [p[TCP].flags for p in all_packets]
            if flags == ['S', 'SA', 'R']:
                return


            #separate the forward and backward traffic
            src_ip = all_packets[0][IP].src
            dest_ip = all_packets[0][IP].dst

            forward_packets = [p for p in all_packets if p[IP].src == src_ip and p[IP].dst == dest_ip] 
            backward_packets = [p for p in all_packets if p[IP].src == dest_ip and p[IP].dst == src_ip]
            

        else:
            print(f"No packets in this session {session_id}")

        #Source_port
        source_port = all_packets[0][TCP].sport
        dest_port = all_packets[0][TCP].sport

        #forward packet feature logic
        if len(forward_packets) == 0 :
            max_interval_forward = 0
            forward_payload_len = 0
            duration_forward = 0
            std_forward_pkt_len = 0

        elif len(forward_packets) == 1 :
            max_interval_forward = 0
            forward_payload_len = len(forward_packets[0][TCP].payload)
            duration_forward = 0
            std_forward_pkt_len = 0
        else:
            #max_Interval_of_arrival_time_of_forward_traffic
            max_interval_forward = max([forward_packets[i+1].time - forward_packets[i].time for i in range(len(forward_packets)-1)])

            #Total_length_of_forward_payload
            forward_payload_len = sum([len(packet[TCP].payload) for packet in forward_packets])

            #duration_forward
            duration_forward = forward_packets[-1].time - forward_packets[0].time

            #std_forward_pkt_length
            std_forward_pkt_len = np.std([len(packet) for packet in forward_packets])


        #backward packet feature logic
        if len(backward_packets) <= 1 :
            max_interval_backwards = 0
            std_interval_backwards = 0
        else:
            #max_Interval_of_arrival_time_of_backward_traffic
            max_interval_backwards = max([backward_packets[i+1].time - backward_packets[i].time for i in range(len(backward_packets)-1)])

            #std_Interval_of_arrival_time_of_backward_traffic
            std_interval_backwards = np.std([backward_packets[i+1].time - backward_packets[i].time for i in range(len(backward_packets)-1)])


        #all packet feature logic
        if len(all_packets) == 0 :
            mean_window = 0
            flow_duration = 0
            std_ip_len = 0
            max_time_diff = 0
            max_tcp_payload_len = 0
            mean_ttl = 0
            std_ttl = 0

        elif len(all_packets) == 1 :
            mean_window = all_packets[0][TCP].window
            flow_duration = 0
            std_ip_len = 0
            max_time_diff = 0
            max_tcp_payload_len = len(all_packets[0][TCP].payload)
            mean_ttl = all_packets[0][IP].ttl
            std_ttl = 0

        else:
            #mean_TCP_windows_size_value
            mean_window = sum([packet[TCP].window for packet in all_packets])/len(all_packets)

            #flow duration
            flow_duration = all_packets[-1].time - all_packets[0].time

            #std_Length_of_IP_packets
            std_ip_len = np.std([len(packet[IP]) for packet in all_packets])

            #max_Time_difference_between_packets_per_session
            max_time_diff = max([all_packets[i+1].time - all_packets[i].time for i in range(len(all_packets)-1)])

            #max_Length_of_TCP_payload
            max_tcp_payload_len = max([len(packet[TCP].payload) for packet in all_packets])

            #mean_time_to_live
            mean_ttl = sum([packet[IP].ttl for packet in all_packets])/len(all_packets)

            #std_time_to_live
            std_ttl = np.std([packet[IP].ttl for packet in all_packets])

        #package the features into a dictionary
        features = {
            "mean_TCP_windows_size_value": mean_window,
            "Source_port": source_port,
            "max_Interval_of_arrival_time_of_forward_traffic": max_interval_forward,
            "max_Interval_of_arrival_time_of_backward_traffic": max_interval_backwards,
            "flow duration": flow_duration,
            "std_Interval_of_arrival_time_of_backward_traffic": std_interval_backwards,
            "Total_length_of_forward_payload": forward_payload_len,
            "std_Length_of_IP_packets": std_ip_len,
            "max_Time_difference_between_packets_per_session": max_time_diff,
            "std_forward_pkt_length": std_forward_pkt_len,
            "max_Length_of_TCP_payload": max_tcp_payload_len,
            "mean_time_to_live": mean_ttl,
            "std_time_to_live": std_ttl,
            "duration_forward": duration_forward,
            "num_packets": len(all_packets)
        }

        metadata = {
            "src_ip": src_ip,
            "dest_ip": dest_ip,
            "src_port": source_port,
            "dest_port": dest_port
        }

        self.write_session(features, all_packets, metadata)
        if(flow_duration == 0):
            print(all_packets)

    def write_session(self, features, packets, metadata):
        '''
        Takes the features, packets, and metadata of a session that has been extracted from
        self.process_session and sends them to the callback function if one has been assigned.
        Otherwise, prints the features to the console.
        '''

        if(self.callback):
            self.callback(features, packets, metadata)
        else:
            for key, value in features.items():
                print(f"{key}: {value}")
            print("\n\n")

if(__name__ == "__main__"):
    #instantiating the session tracker
    tracker = SessionTracker()
    print("Should start displaying flows now")

    #start sniffing packets
    sniff(iface="wlan0", filter="tcp", prn=lambda x: tracker.add_packet(x))
