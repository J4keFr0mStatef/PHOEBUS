############################
# Installation of InfluxDB #

# Update your package lists
sudo apt-get update

# Install InfluxDB server
wget https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_arm64.deb
sudo dpkg -i influxdb2_2.7.6-1_arm64.deb

# Start the InfluxDB service
sudo service influxdb start

# Install the InfluxDB CLI
wget https://download.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-arm64.tar.gz
tar xvzf ./influxdb2-client-2.7.5-linux-arm64.tar.gz
sudo cp ./influx /usr/local/bin/

# Remove the downloaded files
sudo rm influxdb2_2.7.6-1_arm64.deb
sudo rm influxdb2-client-2.7.5-linux-arm64.tar.gz

############################
#      Configuration       #

# Setup InfluxDB
influx setup -u PhoebusAdmin \
             -p "um~N:AgdY=r*bq3kS'x72@" \
             -t 0D5m1NEx3LGnX2NAZd2s64u6J7XOIuNDlz3K4bSwMUiIQS-NTmCeJcC_kLv6W2Alynn_7TkPvRTr3AftZadyMw== \
             -o PHOEBUS \
             -b Bucket_Main \
             -r 24h -f



############################
#    Creating the Buckets  #

#ML buckets
influx bucket create -n ML_malicious -o PHOEBUS -r 30d
influx bucket create -n ML_benign -o PHOEBUS -r 1h

#t_shark bucket
influx bucket create -n tshark_analytics -o PHOEBUS -r 1h

#interface buckets
influx bucket create -n hourly_interface_data -o PHOEBUS -r 24h
influx bucket create -n fiveminute_interface_data -o PHOEBUS -r 1h
influx bucket create -n daily_interface_data -o PHOEBUS -r 30d
influx bucket create -n monthly_interface_data -o PHOEBUS -r 365d
influx bucket create -n connected_clients -o PHOEBUS -r 1h

#create the token
Token=$(influx auth create --org PHOEBUS --all-access)

#store the token to a .env file
echo "INFLUXDB_TOKEN=$Token" > /etc/phoebus/.env