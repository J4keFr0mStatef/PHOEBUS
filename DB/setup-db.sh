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

# Create a new InfluxDB user
influx user create -n PhoebusAdmin -p "um~N:AgdY=r*bq3kS'x72@" -o PHOEBUS

############################
#    Creating the Buckets  #

#ML buckets
influx bucket create -n ML_malicious -o PHOEBUS -r 30d
influx bucket create -n ML_benign -o PHOEBUS -r 30m

#t_shark bucket
influx bucket create -n tshark_analytics -o PHOEBUS -r 1h

#interface buckets
influx bucket create -n hourly_interface_data -o PHOEBUS -r 1h
influx bucket create -n fiveminute_interface_data -o PHOEBUS -r 5m
influx bucket create -n daily_interface_data -o PHOEBUS -r 1d
influx bucket create -n monthly_interface_data -o PHOEBUS -r 30d
influx bucket create -n connected_clients -o PHOEBUS -r 1h

############################
#   Creating the Tokens    #

TsharkToken=$(influx auth create -o PHOEBUS --read-bucket tshark_analytics --write-bucket tshark_analytics)

IfaceToken=$(influx auth create -o PHOEBUS \
        --read-bucket hourly_interface_data --write-bucket hourly_interface_data \
        --read-bucket fiveminute_interface_data --write-bucket fiveminute_interface_data \
        --read-bucket daily_interface_data --write-bucket daily_interface_data \
        --read-bucket monthly_interface_data --write-bucket monthly_interface_data \
        --read-bucket connected_clients --write-bucket connected_clients)

MLToken=$(influx auth create -o PHOEBUS \
        --read-bucket ML_malicious --write-bucket ML_malicious \
        --read-bucket ML_benign --write-bucket ML_benign)

############################
#    Write the Tokens      #

# Write the tokens to the .env file
echo "Tshark_Token=$TsharkToken" > /etc/phoebus/.env
echo "Iface_Token=$IfaceToken" >> /etc/phoebus/.env
echo "ML_Token=$MLToken" >> /etc/phoebus/.env
